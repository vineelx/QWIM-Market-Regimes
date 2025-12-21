from pathlib import Path
import pandas as pd


def _get_base_dir():
    here = Path(__file__).resolve()
    for base in here.parents:
        if (base / "inputs" / "cjm_backtest.csv").exists():
            return base
    raise FileNotFoundError(
        f"Cannot find inputs/cjm_backtest.csv by searching parents of: {here}"
    )


BASE_DIR = _get_base_dir()
INPUTS_DIR = BASE_DIR / "inputs"


def load_backtest():
    path = INPUTS_DIR / "cjm_backtest.csv"
    return pd.read_csv(path, parse_dates=["date"])


def load_spy_ts():
    path = INPUTS_DIR / "spy_timeseries.csv"
    return pd.read_csv(path, parse_dates=["date"])


def load_cjm_regimes():
    path = INPUTS_DIR / "cjm_regimes.csv"
    return pd.read_csv(path, parse_dates=["date"])
