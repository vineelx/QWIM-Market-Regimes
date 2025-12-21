#!/usr/bin/env python3
'''
mutiple_time_series_with_dynamic_weights.py

Program runs and generates 5 inputs for QWIM dashboard in the folder
.../regime_results/inputs
This should be copied to shiny dashboard inputs folder
.../QWIM/QWIM-Market-Regimes-master/Viz-QWIM
Then start the program
.../QWIM/QWIM-Market-Regimes-master/Viz-QWIM/src/dashboard/main_App.py

These can be changed using variables 
OUTPUT_DIR
OUTPUT_DIR_INPUTS
OUTPUT_DIR_INPUTS_DATA_PROCESSED
OUTPUT_DIR_INPUTS_DATA_RAW

In browser open the dashboard url http://127.0.0.1:8080

The tickers can be changed with the global varialble DEFAULT_TICKERS
Ticker SPY is used as default
The values are downloaded from Yahoo Finance
Tickers are downloaded on a monthly basis from start date

Monthly period and regime calculated for every 6 months (window p = candidates[0])
DEFAULT_WINDOW_CANDIDATES = [6, 12, 24, 36]

'''
from __future__ import annotations

import os
import logging
import random
import warnings
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import seaborn as sns

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.manifold import SpectralEmbedding
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from scipy.sparse.csgraph import connected_components
import torch
import torch.nn as nn
import torch.nn.functional as F
from lifelines import CoxTimeVaryingFitter

import yfinance as yf



# ---------- configuration ----------
warnings.filterwarnings("ignore", message="Graph is not fully connected, spectral embedding may not work as expected.")
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

sns.set_style("whitegrid")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("regime_pipeline_all_plots")

SEED = 42
torch.manual_seed(SEED)
torch.cuda.manual_seed_all(SEED)

DEFAULT_WINDOW_CANDIDATES = [6, 12, 24, 36]  # monthly windows
SIM_THRESHOLD_MERGE = 0.50
EMBED_DIM = 16
GAE_EPOCHS = 120
GAE_LR = 1e-2

OUTPUT_DIR = "regime_results"
OUTPUT_DIR_INPUTS = "regime_results/inputs"
OUTPUT_DIR_INPUTS_DATA_PROCESSED = "regime_results/inputs/data_processed"
OUTPUT_DIR_INPUTS_DATA_RAW = "regime_results/inputs/data_raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR_INPUTS, exist_ok=True)
os.makedirs(OUTPUT_DIR_INPUTS_DATA_PROCESSED, exist_ok=True)
os.makedirs(OUTPUT_DIR_INPUTS_DATA_RAW, exist_ok=True)

DEFAULT_TICKERS = [
    "SPY","QQQ","IWM","DIA",
    "XLK","XLF","XLV","XLE","XLI","XLU",
    "EFA","EEM",
    "TLT","IEF","HYG","LQD",
    "GLD","SLV","DBC","VNQ"
]
'''
DEFAULT_TICKERS = [
    "AAPL","MSFT","NVDA","AMD", "SPY"
]

'''

# ---------- data download / save helpers ----------
def download_monthly_prices(tickers, start, end):
    logger.info("Downloading price data for %d tickers from yfinance", len(tickers))
    df = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)["Close"]    
    df.index = pd.to_datetime(df.index)
    monthly = df.resample("M").last()
    cols = [t for t in tickers if t in monthly.columns]
    monthly = monthly[cols]
    logger.info("Downloaded monthly prices: %d rows x %d cols", len(monthly), len(monthly.columns))
    return monthly

def read_prices_csv(path):
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    return df

def save_data_etfs(prices, OUTPUT_DIR, filename):    
    out_path = os.path.join(OUTPUT_DIR, filename)
    prices.to_csv(out_path)
    logger.info("Saved %s (%d rows x %d cols)", out_path, len(prices), len(prices.columns))
    return out_path

def get_asset_prices(tickers, start, prices_csv):
    if prices_csv and os.path.exists(prices_csv):
        return read_prices_csv(prices_csv)
    return download_monthly_prices(tickers, start, None)

def get_asset_returns_from_prices(prices):
    returns = prices.pct_change().dropna(how="all")    
    returns_matrix = returns.T.values  # (N, T)
    dates = returns.index
    tickers_aligned = list(returns.columns)
    return returns_matrix, dates, tickers_aligned

# ---------- graph construction ----------
def build_similarity_graph(window_matrix, top_k):
    n_series = window_matrix.shape[0]
    means = np.nanmean(window_matrix, axis=1)
    stds = np.nanstd(window_matrix, axis=1)
    node_features = np.vstack([means, stds]).T
    sim = cosine_similarity(np.nan_to_num(window_matrix))
    np.fill_diagonal(sim, 0.0)
    sim[sim < 0] = 0.0
    k = min(top_k, max(1, n_series - 1))
    adj = np.zeros_like(sim)
    for i in range(n_series):
        idx = np.argsort(sim[i])[-k:]
        adj[i, idx] = sim[i, idx]
    adj = np.maximum(adj, adj.T)
    return adj, node_features

# ---------- GAE (lightweight) ----------
class SimpleGAEEncoder(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int):
        super().__init__()
        self.lin1 = nn.Linear(in_dim, hidden_dim)
        self.lin2 = nn.Linear(hidden_dim, out_dim)
    def forward(self, x):
        h = F.relu(self.lin1(x))
        z = self.lin2(h)
        return z

class SimpleGAE(nn.Module):
    def __init__(self, in_dim: int, hidden_dim: int, out_dim: int):
        super().__init__()
        self.encoder = SimpleGAEEncoder(in_dim, hidden_dim, out_dim)
    def forward(self, x):
        z = self.encoder(x)
        recon = torch.sigmoid(z @ z.t())
        return recon, z

def learn_embeddings_gae(node_features, adj, dim, epochs: int = GAE_EPOCHS, lr: float = GAE_LR):
    device = torch.device("cpu")
    x = torch.tensor(node_features, dtype=torch.float32, device=device)
    adj_t = torch.tensor(adj, dtype=torch.float32, device=device)
    n, f = node_features.shape
    model = SimpleGAE(in_dim=f, hidden_dim=max(8, dim), out_dim=dim).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    bce = nn.BCELoss()
    target = adj_t
    model.train()
    for epoch in range(epochs):
        opt.zero_grad()
        recon, z = model(x)
        loss = bce(recon, target)
        loss.backward()
        opt.step()
    model.eval()
    with torch.no_grad():
        y, z = model(x)
    return z.cpu().numpy()

# ---------- mapping grid ----------
def build_mapping_grid(returns_matrix, p, sim_threshold_merge, embed_dim):
    n_series, n_times = returns_matrix.shape
    n_windows = n_times // p
    local_clusters_per_window = []
    centroids_list: List[np.ndarray] = []
    centroid_keys: List[Tuple[int,int]] = []
    missing_per_window: List[List[int]] = []
    features_map: Dict[Tuple[int,int], np.ndarray] = {}

    for j in range(n_windows):
        window_matrix = returns_matrix[:, j * p : (j + 1) * p]
        missing = [i for i in range(n_series) if np.isnan(window_matrix[i]).any()]
        missing_per_window.append(missing)
        valid = [i for i in range(n_series) if i not in missing]
        if not valid:
            local_clusters_per_window.append({})
            continue
        submatrix = window_matrix[valid]
        adj, node_feats = build_similarity_graph(submatrix,10)
        embeddings = learn_embeddings_gae(node_feats, adj, dim=embed_dim)
        km = KMeans(n_clusters=min(max(1, embeddings.shape[0] // 5), 6),random_state=SEED).fit(embeddings) 
        labels = km.labels_    
        
        #labels = cluster_embeddings(emb)
        grouped: Dict[int, List[int]] = {}
        for local_idx, lab in enumerate(labels):
            grouped.setdefault(int(lab), []).append(valid[local_idx])
        for lab, series_list in grouped.items():
            member_idx = [valid.index(s) for s in series_list]
            centroid = embeddings[member_idx].mean(axis=0)
            centroids_list.append(centroid)
            centroid_keys.append((j, lab))
            features_map[(j, lab)] = centroid
        local_clusters_per_window.append(grouped)

    if len(centroids_list) == 0:
        grid = []
        for j in range(n_windows):
            grid.append({"regimes": {}, "missing": missing_per_window[j]})
        return grid, features_map, 0, n_windows

    centroids_arr = np.vstack(centroids_list)
    scaler = StandardScaler()
    centroids_norm = scaler.fit_transform(centroids_arr)
    pairwise_sim = cosine_similarity(centroids_norm)
    pairwise_dist = 1.0 - pairwise_sim
    condensed = squareform(pairwise_dist, checks=False)
    Z = linkage(condensed, method="single")
    dist_thresh = 1.0 - sim_threshold_merge
    labels_global = fcluster(Z, t=dist_thresh, criterion="distance") - 1
    centroid_to_global: Dict[Tuple[int,int], int] = {}
    for key, g in zip(centroid_keys, labels_global):
        centroid_to_global[key] = int(g)

    grid: List[Dict[str, Any]] = []
    for j in range(n_windows):
        regimes: Dict[int, List[int]] = {}
        grouped = local_clusters_per_window[j]
        for local_lab, series_list in grouped.items():
            gid = centroid_to_global.get((j, local_lab))
            if gid is None:
                continue
            regimes.setdefault(gid, []).extend(series_list)
        grid.append({"regimes": regimes, "missing": missing_per_window[j]})
    n_global = int(labels_global.max() + 1)
    return grid, features_map, n_global, n_windows

# ---------- build trajectories ----------
def build_trajectories(grid, n_series):
    n_windows = len(grid)
    trajectories = [[-1] * n_windows for i in range(n_series)]
    for j, cell in enumerate(grid):
        for gid, series_list in cell.get("regimes", {}).items():
            for s in series_list:
                if 0 <= s < n_series:
                    trajectories[s][j] = int(gid)
        for s in cell.get("missing", []):
            if 0 <= s < n_series:
                trajectories[s][j] = -2
    return trajectories

# ---------- plotting helpers ----------
def grid_to_matrix(grid, n_series: int):
    n_windows = len(grid)
    M = np.full((n_series, n_windows), -1, dtype=int)
    for j, cell in enumerate(grid):
        for gid, series_list in cell["regimes"].items():
            for s in series_list:
                M[s, j] = gid
        for s in cell.get("missing", []):
            M[s, j] = -2
    return M

def plot_mapping_grid_heatmap_verbose(grid, tickers, OUTPUT_DIR):
    M = grid_to_matrix(grid, len(tickers))
    vals = np.unique(M[M >= 0])
    if vals.size == 0:
        logger.info("No regimes to plot (all missing or unassigned).")
        return ""
    mapping = {v: i for i, v in enumerate(vals)}
    M_mapped = np.full_like(M, fill_value=np.nan, dtype=float)
    for orig, mapped in mapping.items():
        M_mapped[M == orig] = mapped
    mask = (M < 0)
    n_colors = max(3, len(vals))
    cmap = sns.color_palette("tab20", n_colors=n_colors)
    cmap = mcolors.ListedColormap(cmap)
    plt.figure(figsize=(14, max(4, len(tickers) * 0.15)))
    ax = sns.heatmap(M_mapped, cmap=cmap, mask=mask, cbar=True,
                     linewidths=0.1, linecolor="gray", xticklabels=False, yticklabels=tickers,
                     vmin=0, vmax=n_colors-1)
    cbar = ax.collections[0].colorbar
    cbar.set_ticks(np.arange(0.5, n_colors, 1))
    cbar.set_ticklabels([str(v) for v in vals])
    plt.title("Mapping Grid Heatmap (masked missing/unassigned)")
    plt.xlabel("Window index")
    plt.ylabel("Ticker")
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "mapping_grid_heatmap_verbose.png")
    plt.savefig(path, dpi=150)
    plt.close()
    logger.info("Saved verbose heatmap to %s", path)
    return path

def plot_regime_trajectories(grid, tickers, window_dates, OUTPUT_DIR):
    # Basic validation
    if not isinstance(grid, list) or len(grid) == 0:
        raise ValueError("grid must be a non-empty list of window cells")
    if not isinstance(tickers, (list, tuple)) or len(tickers) == 0:
        raise ValueError("tickers must be a non-empty list of ticker names")

    # Build matrix M (n_series x n_windows)
    M = grid_to_matrix(grid, len(tickers))
    n_series, n_windows = M.shape

    # Ensure tickers label length matches rows; pad/truncate safely
    if len(tickers) != n_series:
        logger.warning("tickers length (%d) does not match grid rows (%d). Adjusting labels.", len(tickers), n_series)
        if len(tickers) > n_series:
            y_labels = tickers[:n_series]
        else:
            y_labels = tickers + [f"t{i}" for i in range(len(tickers), n_series)]
    else:
        y_labels = tickers

    # Prepare x axis values and determine whether to use dates
    use_dates = False
    x = list(range(n_windows))
    x_dates = None
    if window_dates is not None:
        try:
            x_dates = pd.to_datetime(window_dates)
            if len(x_dates) == n_windows:
                use_dates = True
                x = x_dates
            else:
                logger.warning("window_dates length (%d) != number of windows (%d); falling back to integer indices.",
                               len(x_dates), n_windows)
        except Exception:
            logger.warning("window_dates could not be parsed as datetimes; falling back to integer indices.")

    # Plot
    plt.figure(figsize=(14, max(4, n_series * 0.12)))
    ax = plt.gca()

    for i in range(n_series):
        y = M[i]
        # mask missing/unassigned so lines don't connect across gaps
        y_plot = np.where(y >= 0, y, np.nan)
        ax.plot(x, y_plot, marker="o", linewidth=1.25, label=y_labels[i], alpha=0.9)

    ax.set_title("Ticker Regime Trajectories Over Time")
    ax.set_xlabel("Year" if use_dates else "Window index")
    ax.set_ylabel("Regime ID")

    # Y ticks: show regime ids present (sorted)
    present_regs = np.unique(M[M >= 0])
    if present_regs.size > 0:
        yticks = present_regs.tolist()
        ax.set_yticks(yticks)
        ax.set_yticklabels([str(int(r)) for r in yticks])

    # X axis formatting: show years only when using dates
    if use_dates:
        # Major ticks: years only; Minor ticks: months (no labels)
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))   # years only
        ax.xaxis.set_minor_locator(mdates.MonthLocator())
        # Hide minor tick labels to avoid clutter
        ax.xaxis.set_minor_formatter(mdates.DateFormatter(""))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha="center")
        plt.setp(ax.xaxis.get_minorticklabels(), rotation=45, ha="right", fontsize=7)
        ax.tick_params(axis="x", which="major", length=8)
        ax.tick_params(axis="x", which="minor", length=4)
    else:
        # If we have no dates but can infer years from a provided window_dates list (mismatch case),
        # label a subset of integer ticks with year strings to keep the x-axis readable.
        if window_dates is not None:
            try:
                inferred = pd.to_datetime(window_dates)
                years = [d.year for d in inferred[:n_windows]]
                # choose tick positions to avoid overcrowding
                step = max(1, n_windows // 10)
                ticks = list(range(0, n_windows, step))
                ax.set_xticks(ticks)
                ax.set_xticklabels([str(years[i]) for i in ticks], rotation=45)
            except Exception:
                ax.set_xticks(range(n_windows))
                ax.set_xticklabels([str(i) for i in range(n_windows)], rotation=45)
        else:
            ax.set_xticks(range(n_windows))
            ax.set_xticklabels([str(i) for i in range(n_windows)], rotation=45)

    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), ncol=1, fontsize=8)
    plt.tight_layout()

    path = os.path.join(OUTPUT_DIR, "regime_trajectories.png")
    plt.savefig(path, dpi=150)
    plt.close()
    logger.info("Saved regime trajectories to %s", path)
    return path
# ---------- mean/variance/sharpe plotting ----------
def plot_mean_variance_and_sharpe(returns_matrix, tickers, OUTPUT_DIR):    
    df_stats = compute_returns_stats(returns_matrix, tickers, "monthly", 0.0)
    # mean-variance scatter
    plt.figure(figsize=(8,6))
    plt.scatter(df_stats["ann_std"], df_stats["ann_mean"], s=40, alpha=0.85)
    for i,t in enumerate(df_stats.index):
        plt.text(df_stats["ann_std"].iloc[i], df_stats["ann_mean"].iloc[i], t, fontsize=8)
        plt.scatter([df_stats["ann_std"].mean()], [df_stats["ann_mean"].mean()], color="red", s=80, label="Avg")
        plt.xlabel("Annualized Std Dev"); plt.ylabel("Annualized Mean Return"); plt.title("Mean-Variance Scatter")
        plt.tight_layout()
        mv_path = os.path.join(OUTPUT_DIR,"mean_variance_scatter.png")
        plt.savefig(mv_path, dpi=150)
        plt.close()        
    return mv_path

# ---------- mean/variance/sharpe ----------
def annualization_factor_from_freq(freq: str = "monthly"):
    if freq == "weekly":
        return 52
    if freq == "daily":
        return 252
    return 12

def compute_returns_stats(returns_matrix, tickers, freq, risk_free_rate):
    if returns_matrix is None or returns_matrix.size == 0:
        return pd.DataFrame(columns=["ticker","mean_return","var_return","ann_mean","ann_std","sharpe"]).set_index("ticker")
    n_series, n_times = returns_matrix.shape
    af = annualization_factor_from_freq(freq)
    rows = []
    for i, t in enumerate(tickers):
        series = np.asarray(returns_matrix[i], dtype=float)
        valid = ~np.isnan(series)
        if valid.sum() == 0:
            rows.append({"ticker": t, "mean_return": np.nan, "var_return": np.nan, "ann_mean": np.nan, "ann_std": np.nan, "sharpe": np.nan})
            continue
        mean_r = float(np.nanmean(series))
        var_r = float(np.nanvar(series, ddof=1))
        ann_mean = mean_r * af
        ann_std = float(np.nanstd(series, ddof=1) * np.sqrt(af))
        rf = float(risk_free_rate)
        sharpe = (ann_mean - rf) / ann_std if ann_std > 0 else np.nan
        rows.append({"ticker": t, "mean_return": mean_r, "var_return": var_r, "ann_mean": ann_mean, "ann_std": ann_std, "sharpe": sharpe})
    df = pd.DataFrame(rows).set_index("ticker")
    return df

def save_mean_variance_tables(returns_matrix, tickers, OUTPUT_DIR, freq, risk_free_rate, weights):    
    df_stats = compute_returns_stats(returns_matrix, tickers, freq=freq, risk_free_rate=risk_free_rate)
    mv_path = os.path.join(OUTPUT_DIR, "mean_variance_table.csv")
    df_stats.to_csv(mv_path)
    if weights is None:
        w = np.ones(len(tickers)) / max(1, len(tickers))
    else:
        w = np.asarray(weights, dtype=float)
        if w.size != len(tickers):
            raise ValueError("weights length must match tickers length")
    port_stats = compute_portfolio_stats(w, returns_matrix, freq=freq, risk_free_rate=risk_free_rate)
    df_port = pd.DataFrame([port_stats], index=["portfolio"])
    port_path = os.path.join(OUTPUT_DIR, "portfolio_stats.csv")
    df_port.to_csv(port_path)
    logger.info("Saved mean/variance and portfolio stats to %s and %s", mv_path, port_path)
    return {"mean_variance_csv": mv_path, "portfolio_csv": port_path}

def compute_portfolio_stats(weights, returns_matrix, freq, risk_free_rate):
    if returns_matrix is None or returns_matrix.size == 0:
        return {"mean_return": np.nan, "var_return": np.nan, "ann_mean": np.nan, "ann_std": np.nan, "sharpe": np.nan}
    w = np.asarray(weights, dtype=float)
    if w.ndim != 1:
        raise ValueError("weights must be 1D array")
    if w.sum() == 0:
        raise ValueError("weights sum to zero")
    w = w / w.sum()
    R = np.asarray(returns_matrix, dtype=float)
    n_series, n_times = R.shape
    port_returns = np.full(n_times, np.nan)
    for t in range(n_times):
        col = R[:, t]
        valid = ~np.isnan(col)
        if valid.sum() == 0:
            port_returns[t] = np.nan
            continue
        w_valid = w[valid]
        w_valid = w_valid / w_valid.sum()
        port_returns[t] = float(np.dot(w_valid, col[valid]))
    mean_r = float(np.nanmean(port_returns))
    var_r = float(np.nanvar(port_returns, ddof=1))
    af = annualization_factor_from_freq(freq)
    ann_mean = mean_r * af
    ann_std = float(np.nanstd(port_returns, ddof=1) * np.sqrt(af))
    rf = float(risk_free_rate)
    sharpe = (ann_mean - rf) / ann_std if ann_std > 0 else np.nan
    return {"mean_return": mean_r, "var_return": var_r, "ann_mean": ann_mean, "ann_std": ann_std, "sharpe": sharpe}

# ---------- portfolio & benchmark value computation ----------
def compute_portfolio_values(prices, weights_df, start_value):
    tickers = [c for c in prices.columns if c in weights_df.columns]
    if len(tickers) == 0:
        raise ValueError("No overlapping tickers between prices and weights")
    combined_index = weights_df.index.union(prices.index)
    weights_ff = weights_df.reindex(combined_index).ffill().reindex(prices.index).fillna(0.0)[tickers]
    returns = prices[tickers].pct_change().fillna(0.0)
    port_rets = (weights_ff.values * returns.values).sum(axis=1)
    port_values = pd.Series(start_value * (1.0 + pd.Series(port_rets, index=prices.index)).cumprod(), index=prices.index, name="Value")
    contrib_period = pd.DataFrame(weights_ff.values * returns.values, index=prices.index, columns=[f"period_contrib_{t}" for t in tickers])
    out_df = pd.concat([port_values, contrib_period], axis=1)
    out_df.index.name = "Date"
    return out_df

def compute_benchmark_values(prices, benchmark_ticker, start_value):
    if benchmark_ticker not in prices.columns:
        raise ValueError(f"{benchmark_ticker} not found in prices columns")
    bench_ret = prices[benchmark_ticker].pct_change().fillna(0.0)
    bench_values = pd.Series(start_value * (1.0 + bench_ret).cumprod(), index=prices.index, name=f"Value")
    bench_df = bench_values.to_frame()
    bench_df.index.name = "Date"
    return bench_df

# ---------- regime-based weighting ----------
def regime_based_weights_from_trajectories(trajectories, tickers, window_dates, spy_ticker, base_weight, aligned_multiplier):
    idx_map = {t: i for i, t in enumerate(tickers)}
    if spy_ticker not in idx_map:
        raise ValueError("SPY must be in tickers to use regime-based alignment")
    spy_idx = idx_map[spy_ticker]
    spy_traj = np.array(trajectories[spy_idx], dtype=int)
    n_windows = spy_traj.shape[0]
    if len(window_dates) != n_windows:
        index = list(range(n_windows))
    else:
        index = window_dates
    rows = []
    for j in range(n_windows):
        spy_reg = spy_traj[j]
        row = {}
        for t in tickers:
            traj = np.array(trajectories[idx_map[t]], dtype=int)
            reg = traj[j]
            if reg >= 0 and reg == spy_reg and spy_reg >= 0:
                row[t] = base_weight * aligned_multiplier
            else:
                row[t] = base_weight
        total = sum(row.values())
        if total <= 0:
            n = len(tickers)
            row = {t: 1.0 / n for t in tickers}
        else:
            row = {t: v / total for t, v in row.items()}
        rows.append(row)
    df = pd.DataFrame(rows, index=index, columns=tickers)
    df.index.name = "Date"
    return df

# ---------- lifelines / cox / transition helpers ----------
def build_time_varying_table_for_cox(grid, features_map, n_global):
    rows = []
    n_windows = len(grid)
    for gid in range(n_global):
        present_windows = [j for j, cell in enumerate(grid) if gid in cell.get("regimes", {}) and len(cell["regimes"][gid]) > 0]
        if not present_windows:
            continue
        for idx, j in enumerate(present_windows):
            candidates = [v for (w, _), v in features_map.items() if w == j]
            cov = np.vstack(candidates).mean(axis=0) if candidates else np.zeros(EMBED_DIM)
            event = 1 if (j == present_windows[-1]) else 0
            row = {"regime_id": int(gid), "start": int(j), "stop": int(j + 1), "event": int(event)}
            for k in range(len(cov)):
                row[f"f_{k}"] = float(cov[k])
            rows.append(row)
    if not rows:
        return pd.DataFrame()
    tv_df = pd.DataFrame(rows)
    return tv_df

def fit_time_dependent_cox_safe(tv_df, pca_dim: int = 6, penalizer_grid=[0.1, 1.0, 10.0]):            
    feat_cols = [c for c in tv_df.columns if c.startswith("f_")]    
    X = tv_df[feat_cols].astype(float).copy()
    var = X.var(axis=0)
    nonconst = var[var > 1e-12].index.tolist()    
    X = X[nonconst]
    if X.shape[1] > pca_dim:
        scaler = StandardScaler()
        Xs = scaler.fit_transform(X)
        pca = PCA(n_components=min(pca_dim, Xs.shape[1]))
        Xred = pca.fit_transform(Xs)
        for i in range(Xred.shape[1]):
            tv_df[f"pc_{i}"] = Xred[:, i]
        cov_cols = [f"pc_{i}" for i in range(Xred.shape[1])]
    else:
        scaler = StandardScaler()
        Xs = scaler.fit_transform(X)
        for i, col in enumerate(X.columns):
            tv_df[f"std_{i}"] = Xs[:, i]
        cov_cols = [f"std_{i}" for i in range(Xs.shape[1])]    
    for penalizer in penalizer_grid:
        try:
            ctv = CoxTimeVaryingFitter(penalizer=penalizer)
            formula = " + ".join(cov_cols)
            ctv.fit(tv_df, id_col="regime_id", start_col="start", stop_col="stop", event_col="event", show_progress=False, formula=formula)
            logger.info("Cox fitted with penalizer=%s", penalizer)
            return ctv
        except Exception as e:
            logger.debug("Cox fit failed with penalizer=%s: %s", penalizer, e)
            continue
    eps = 1e-8
    for col in cov_cols:
        tv_df[col] = tv_df[col] + np.random.normal(scale=eps, size=len(tv_df))
    try:
        ctv = CoxTimeVaryingFitter(penalizer=1.0)
        formula = " + ".join(cov_cols)
        ctv.fit(tv_df, id_col="regime_id", start_col="start", stop_col="stop", event_col="event", show_progress=False, formula=formula)
        logger.info("Cox fitted after tiny noise.")
        return ctv
    except Exception as e:
        logger.info("Cox fitting ultimately failed; skipping Cox. (%s)", e)
        return None

def build_transition_dataset(grid, features_map, n_global):
    rows = []
    n_windows = len(grid)
    missing_id = n_global
    for j in range(n_windows - 1):
        cell = grid[j]
        next_cell = grid[j + 1]
        cur_map = {}
        for gid, series_list in cell["regimes"].items():
            for s in series_list:
                cur_map[s] = gid
        for s in cell["missing"]:
            cur_map[s] = missing_id
        next_map = {}
        for gid, series_list in next_cell["regimes"].items():
            for s in series_list:
                next_map[s] = gid
        for s in next_cell["missing"]:
            next_map[s] = missing_id
        all_series = set(list(cur_map.keys()) + list(next_map.keys()))
        for s in all_series:
            cur = cur_map.get(s, missing_id)
            nxt = next_map.get(s, missing_id)
            candidates = [(k, v) for k, v in features_map.items() if k[0] == j]
            cov = np.vstack([v for _, v in candidates]).mean(axis=0) if candidates else np.zeros(EMBED_DIM)
            row = {"start_window": int(j), "series": int(s), "cur_regime": int(cur), "next_regime": int(nxt)}
            for k in range(len(cov)):
                row[f"f_{k}"] = float(cov[k])
            rows.append(row)
    if len(rows) == 0:
        return pd.DataFrame()
    return pd.DataFrame(rows)

def fit_transition_model(trans_df, n_global):
    if trans_df.empty:
        return None
    feat_cols = [c for c in trans_df.columns if c.startswith("f_")]
    X = trans_df[feat_cols].values
    y = trans_df["next_regime"].values
    try:
        clf = LogisticRegression(multi_class="multinomial", solver="lbfgs", max_iter=1000)
        clf.fit(X, y)
        return clf
    except Exception as e:
        logger.debug("Transition model fitting failed: %s", e)
        return None

def predict_regime_next_for_series(series_idx, current_window, grid, features_map, cox_model, trans_model, n_global):
    n_windows = len(grid)
    missing_id = n_global
    cell = grid[current_window]
    cur = None
    for gid, series_list in cell["regimes"].items():
        if series_idx in series_list:
            cur = gid
            break
    if cur is None:
        cur = missing_id if series_idx in cell["missing"] else -1
    candidates = [(k, v) for k, v in features_map.items() if k[0] == current_window]
    cov = np.vstack([v for _, v in candidates]).mean(axis=0) if candidates else np.zeros(EMBED_DIM)
    probs: Dict[int, float] = {}
    if trans_model is not None:
        feat = cov.reshape(1, -1)
        try:
            pred_proba = trans_model.predict_proba(feat)[0]
            classes = trans_model.classes_
            for cls, p in zip(classes, pred_proba):
                probs[int(cls)] = float(p)
        except Exception:
            for gid in range(n_global + 1):
                probs[gid] = 1.0 / (n_global + 1)
    else:
        if cox_model is not None:
            try:
                for gid in range(n_global):
                    row = {"regime_id": gid, "start": current_window, "stop": current_window + 1, "event": 0}
                    for k in range(EMBED_DIM):
                        row[f"f_{k}"] = float(cov[k])
                    sf = cox_model.predict_survival_function(pd.DataFrame([row]), times=[current_window + 1])
                    probs[gid] = float(sf.iloc[-1, 0]) if not sf.empty else 0.0
            except Exception:
                for gid in range(n_global):
                    probs[gid] = 1.0 / max(1, n_global)
        else:
            for gid in range(n_global + 1):
                probs[gid] = 1.0 / (n_global + 1)
    pred = max(probs.items(), key=lambda x: x[1])[0]
    return int(pred), probs

# ---------- main ----------
def main(tickers, start, candidates, embed_dim, prices_csv, weights_csv, risk_free_rate, portfolio_start_value, benchmark_ticker):
    # Prices: download or read and save data_ETFs.csv
    prices = get_asset_prices(tickers, start, prices_csv)
    # QWIM Dashboard
    save_data_etfs(prices, OUTPUT_DIR=OUTPUT_DIR_INPUTS_DATA_RAW, filename="data_ETFs.csv")
    prices.to_csv(os.path.join(OUTPUT_DIR_INPUTS_DATA_RAW, "data_timeseries.csv"))

    # Returns matrix
    returns_matrix, dates, tickers_aligned = get_asset_returns_from_prices(prices)
    n_series, n_times = returns_matrix.shape
    logger.info("Loaded %d series and %d return time points", n_series, n_times)

    # Save mean/variance table
    save_mean_variance_tables(returns_matrix, tickers_aligned, OUTPUT_DIR=OUTPUT_DIR, freq="monthly", risk_free_rate=risk_free_rate, weights=None)    

    # Select window p
    p = candidates[0]
    logger.info("Selected window p = %d", p)

    # Build mapping grid
    grid, features_map, n_global, n_windows = build_mapping_grid(returns_matrix, p, sim_threshold_merge=SIM_THRESHOLD_MERGE, embed_dim=embed_dim)
    logger.info("Built mapping grid: %d windows, %d global regimes", n_windows, n_global)

    # Trajectories
    trajectories = build_trajectories(grid, n_series)

    # Plot mapping grid and trajectories (verbose)
    plot_mapping_grid_heatmap_verbose(grid, tickers_aligned, OUTPUT_DIR=OUTPUT_DIR)
    # Validate and (re)build window_dates_market to match grid
    M = grid_to_matrix(grid, len(tickers_aligned))
    n_windows = M.shape[1]        
    window_dates_market = [dates[min(j * p, len(dates) - 1)] for j in range(n_windows)]
    plot_regime_trajectories(grid, tickers_aligned, window_dates_market, OUTPUT_DIR=OUTPUT_DIR)    

    # Time-varying Cox and transition model
    tv_df = build_time_varying_table_for_cox(grid, features_map, n_global)    
    cox_model = fit_time_dependent_cox_safe(tv_df)
    trans_df = build_transition_dataset(grid, features_map, n_global)
    trans_model = fit_transition_model(trans_df, n_global)

    # Forecasts
    forecasts = {}
    if n_windows >= 2:
        cur_window = n_windows - 2
        for s_idx in range(n_series):
            pred, probs = predict_regime_next_for_series(s_idx, cur_window, grid, features_map, cox_model, trans_model, n_global)
            forecasts[tickers_aligned[s_idx]] = {"predicted_regime": int(pred), "probs": probs}

    # Map windows to dates (first date of each window)
    window_dates = []
    for j in range(n_windows):
        start_idx = j * p
        if start_idx < len(dates):
            window_dates.append(dates[start_idx])
        else:
            window_dates.append(dates[-1])

    # Regime-based weights and save
    df_regime_weights = regime_based_weights_from_trajectories(trajectories, tickers_aligned, window_dates, spy_ticker=benchmark_ticker, base_weight=0.02, aligned_multiplier=2.0)    
    # QWIM Dashboard file name 
    regime_weights_path = os.path.join(OUTPUT_DIR_INPUTS_DATA_RAW, "my_portfolio_weights_ETFs.csv")
    df_regime_weights.to_csv(regime_weights_path)
    logger.info("Saved regime-based weights to %s", regime_weights_path)

    #Compute portfolio and benchmark values
    portfolio_values_df = compute_portfolio_values(prices, df_regime_weights, start_value=portfolio_start_value)

    # Save full detailed file for debugging (keep all columns for reference)
    portfolio_values_path = os.path.join(OUTPUT_DIR, "my_portfolio_values_detailed.csv")
    portfolio_values_df.to_csv(portfolio_values_path, index=True)
    logger.info("Saved portfolio detailed values to %s", portfolio_values_path)
        
    # QWIM Dashboard Create and save the compact two-column file (Date + Value)
    compact_df = portfolio_values_df[["Value"]].copy()        
    compact_df.index = pd.to_datetime(compact_df.index)
    compact_df.index = compact_df.index.normalize()
    compact_df.index.name = "Date"
    compact_path = os.path.join(OUTPUT_DIR_INPUTS_DATA_PROCESSED, "my_portfolio_values.csv")
    compact_df.to_csv(compact_path, index=True, date_format="%Y-%m-%d")
    logger.info("Saved compact portfolio values to %s", compact_path)
    
    bench_df = compute_benchmark_values(prices, benchmark_ticker, start_value=portfolio_start_value)
    bench_path = os.path.join(OUTPUT_DIR_INPUTS_DATA_PROCESSED, "benchmark_portfolio_values.csv")
    bench_df.to_csv(bench_path)
    logger.info("Saved benchmark values to %s", bench_path)
    
    # Mean-variance and Sharpe plots
    plot_mean_variance_and_sharpe(returns_matrix, tickers_aligned, OUTPUT_DIR=OUTPUT_DIR)

# ---------- end main ----------

tickers = DEFAULT_TICKERS.copy()
prices_csv = None
weights_csv = None
start_date = "2002-01-01"
main(tickers=tickers, start=start_date, candidates=DEFAULT_WINDOW_CANDIDATES, embed_dim=EMBED_DIM, prices_csv=prices_csv, weights_csv=weights_csv, risk_free_rate=0.0, portfolio_start_value=100.0, benchmark_ticker="SPY")
logger.info("Pipeline complete. Check the '%s' directory for outputs.", OUTPUT_DIR)
