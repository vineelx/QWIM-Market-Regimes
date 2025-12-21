#!/bin/bash

echo "================================================"
echo "Testing Esen NLP-Enhanced Model Integration"
echo "================================================"

echo ""
echo "1. Checking if module files exist..."
if [ -f "Viz-QWIM/src/dashboard/modules_tab_nlp_regime/tab_nlp_regime.py" ]; then
    echo "   ✓ tab_nlp_regime.py exists"
else
    echo "   ✗ tab_nlp_regime.py NOT FOUND"
fi

echo ""
echo "2. Checking if data files exist..."
if [ -f "Viz-QWIM/data/regime_detection_nlp.png" ]; then
    echo "   ✓ regime_detection_nlp.png exists ($(ls -lh Viz-QWIM/data/regime_detection_nlp.png | awk '{print $5}'))"
else
    echo "   ✗ regime_detection_nlp.png NOT FOUND"
fi

if [ -f "Viz-QWIM/data/portfolio_comprehensive.png" ]; then
    echo "   ✓ portfolio_comprehensive.png exists ($(ls -lh Viz-QWIM/data/portfolio_comprehensive.png | awk '{print $5}'))"
else
    echo "   ✗ portfolio_comprehensive.png NOT FOUND"
fi

echo ""
echo "3. Checking Python imports..."
cd Viz-QWIM
python3 -c "
try:
    from src.dashboard.modules_tab_nlp_regime.tab_nlp_regime import tab_nlp_regime_ui, tab_nlp_regime_server
    print('   ✓ Module imports successfully')
except Exception as e:
    print(f'   ✗ Import error: {e}')
" 2>&1

echo ""
echo "4. Checking main_App.py integration..."
if grep -q "modules_tab_nlp_regime" src/dashboard/main_App.py; then
    echo "   ✓ Module imported in main_App.py"
else
    echo "   ✗ Module NOT imported in main_App.py"
fi

if grep -q "tab_nlp_regime_ui" src/dashboard/main_App.py; then
    echo "   ✓ UI function called in main_App.py"
else
    echo "   ✗ UI function NOT called in main_App.py"
fi

if grep -q "tab_nlp_regime_server" src/dashboard/main_App.py; then
    echo "   ✓ Server function called in main_App.py"
else
    echo "   ✗ Server function NOT called in main_App.py"
fi

echo ""
echo "================================================"
echo "Integration Test Complete!"
echo "================================================"
echo ""
echo "To launch the dashboard:"
echo "  cd Viz-QWIM"
echo "  python app.py"
echo ""
echo "Then open: http://127.0.0.1:8000"
echo "Click on: 'Esen-NLP Regime Model' tab"
echo ""
