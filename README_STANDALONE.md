# Viz-QWIM Dashboard - Standalone Version

## ✅ This Folder is READY to Share!

This Viz-QWIM folder is now **completely standalone** and can be zipped and shared with teammates.

## 📦 How to Zip & Share

```bash
cd /Users/esendashnyam/Desktop/Project_2_fe800
zip -r Viz-QWIM.zip Viz-QWIM/ -x "*__pycache__*" "*.pyc"
```

**Size**: ~220 MB (includes all data, plots, and code)

## 🚀 How Teammates Use It

### 1. **Unzip**
```bash
unzip Viz-QWIM.zip
cd Viz-QWIM
```

### 2. **Install Dependencies**
```bash
pip install shiny plotly pandas polars great-tables numpy
```

**OR** use requirements.txt:
```bash
pip install -r requirements.txt
```

### 3. **Run Dashboard**
```bash
python app.py
```

### 4. **Open Browser**
```
http://127.0.0.1:8000
```

Click on: **"Esen-NLP Regime Model"** tab

## 📊 Features

- **Portfolio Performance**: 60+ stocks across 6 sectors
- **Stock Selector**: Asset managers can choose custom portfolios
- **Instant Backtesting**: Run backtests vs SPY in real-time
- **Regime Detection**: Visual market regime analysis
- **Performance Metrics**: Returns, Sharpe ratios, drawdowns

## 💻 System Requirements

- **Python**: 3.10 or higher
- **OS**: Mac, Windows, or Linux
- **RAM**: 2GB minimum
- **Disk**: 250 MB

## 🎯 What's Included

```
Viz-QWIM/
├── app.py                      # Main dashboard
├── data/                       # All required data (standalone!)
│   ├── cache/                  # Price data
│   ├── plots/                  # Regime & portfolio plots
│   └── portfolio_results/      # Performance data
├── src/
│   └── dashboard/
│       ├── main_App.py         # Dashboard core
│       └── modules_tab_nlp_regime/  # Esen-NLP tab
└── inputs/                     # Other dashboard data
```

## ✅ Integration Status

- ✅ **Fully integrated** with Viz-QWIM dashboard
- ✅ **Works as "Esen-NLP Regime Model" tab**
- ✅ **All data included** (no external dependencies)
- ✅ **Stock selector** for custom portfolios
- ✅ **Real-time backtesting**

## 🔧 Troubleshooting

**Port 8000 already in use?**
```bash
# Kill existing process
pkill -f "python.*app.py"
# Or change port in app.py
```

**Missing dependencies?**
```bash
pip install --upgrade shiny plotly pandas
```

**Data not loading?**
- Ensure `data/` folder is in Viz-QWIM directory
- Check that `.parquet` and `.png` files exist

## 📞 Support

If teammates have issues:
1. Check Python version: `python --version` (need 3.10+)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Verify data folder exists: `ls data/`

---

**Ready to share!** 🚀

