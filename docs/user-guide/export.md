# Export Features

The QWIM Dashboard provides comprehensive export capabilities to save and share your analysis results.

## Export Capabilities

### PNG Chart Export

All visualizations can be exported as high-quality PNG images:

!!! success "PNG Export Features"
    - **High Resolution**: Publication-quality images
    - **Current State**: Exports reflect current selections
    - **Multiple Charts**: All chart types supported
    - **Automatic Naming**: Descriptive filenames

#### Supported Chart Exports

| Chart Type | Export Quality | Best For |
|------------|----------------|----------|
| **Stacked Area** | High resolution | Presentations, reports |
| **Line Chart** | Vector-quality lines | Analysis documentation |
| **Bar Chart** | Clean rendering | Executive summaries |
| **Heatmap** | Color-accurate | Pattern documentation |
| **Pie Chart** | Clear labels | Composition reports |

### Table Export

Statistical analysis tables can be exported for further analysis:

!!! info "Table Export Features"
    - **PNG Format**: Visual table representation
    - **Current Selection**: Reflects selected components
    - **Complete Statistics**: All calculated metrics
    - **Professional Formatting**: Clean, readable layout

#### Statistical Table Contents

| Metric | Description | Export Quality |
|--------|-------------|----------------|
| **Component Names** | Selected ETF identifiers | Clear labels |
| **Latest** | Most recent weights | Current precision |
| **Average** | Historical mean | Statistical accuracy |
| **Min/Max** | Range values | Extreme value precision |
| **StdDev** | Volatility measure | Statistical precision |

## Export Workflow

### Basic Export Process

1. **Configure Analysis**
   - Select desired time period
   - Choose components for analysis
   - Set visualization preferences

2. **Review Results**
   - Verify charts show desired data
   - Check statistical table accuracy
   - Confirm component selection

3. **Export Content**
   - Charts export automatically (if enabled)
   - Tables export with analysis
   - Files saved with descriptive names

### Export Synchronization

!!! success "Real-Time Export Sync"
    All exports automatically reflect current dashboard state:
    
    - **Component Changes**: Select/deselect components → Exports update
    - **Time Period Changes**: Modify period → Exports refresh
    - **Visualization Changes**: Switch chart type → Export updates
    - **Settings Changes**: Toggle percentage view → Exports adjust

## Export Configuration

### Export Settings

The dashboard provides configurable export options:

```python
# Export configuration options
ENABLE_PNG_SAVING = True                    # Enable/disable PNG exports
PNG_EXPORT_DPI = 300                        # High-resolution exports
PNG_EXPORT_WIDTH = 1200                     # Export width in pixels
PNG_EXPORT_HEIGHT = 800                     # Export height in pixels
EXPORT_FILENAME_TEMPLATE = "qwim_{type}_{date}"  # Naming convention
```

### Automatic vs. Manual Export

=== "Automatic Export"
    **When Enabled:**
    - Charts save automatically when rendered
    - Tables export when statistics calculated
    - No user action required
    - Files accumulate in export directory
    
    **Benefits:**
    - Complete analysis trail
    - No missed exports
    - Batch processing capability

=== "Manual Export"
    **When Needed:**
    - User-controlled export timing
    - Selective content export
    - Custom naming options
    - On-demand processing
    
    **Benefits:**
    - User control
    - Selective exports
    - Custom organization

## File Management

### Export Directory Structure

```
project_root/
├── exports/
│   ├── charts/
│   │   ├── qwim_area_chart_2025-06-10.png
│   │   ├── qwim_line_chart_2025-06-10.png
│   │   └── qwim_heatmap_2025-06-10.png
│   ├── tables/
│   │   ├── qwim_statistics_2025-06-10.png
│   │   └── qwim_summary_2025-06-10.png
│   └── analysis/
│       ├── portfolio_analysis_session_1.zip
│       └── complete_analysis_2025-06-10.zip
```

### File Naming Conventions

!!! tip "Descriptive Filenames"
    Export files use consistent, descriptive naming:
    
    **Chart Files:**
    - `qwim_area_chart_5y_3components_2025-06-10.png`
    - `qwim_line_ytd_allcomponents_2025-06-10.png`
    
    **Table Files:**
    - `qwim_statistics_custom_selected_2025-06-10.png`
    - `qwim_summary_1y_comparison_2025-06-10.png`

### Export Organization

| Content Type | Directory | Naming Pattern | Purpose |
|--------------|-----------|----------------|---------|
| **Charts** | `/exports/charts/` | `qwim_[type]_[period]_[date].png` | Visualizations |
| **Tables** | `/exports/tables/` | `qwim_stats_[selection]_[date].png` | Statistical analysis |
| **Reports** | `/exports/reports/` | `qwim_report_[session]_[date].pdf` | Complete analysis |

## Advanced Export Features

### Batch Export

For comprehensive analysis documentation:

1. **Session Export**
   - All charts from current session
   - All statistical tables
   - Configuration summary
   - Timestamp documentation

2. **Comparative Export**
   - Multiple time periods
   - Different component selections
   - Various visualization types
   - Side-by-side comparisons

3. **Historical Export**
   - Time series of exports
   - Trend documentation
   - Change tracking
   - Archive creation

### Custom Export Scenarios

#### Executive Summary Export

!!! example "Executive Package"
    **Contents:**
    - Portfolio composition pie chart
    - 5-year trend area chart
    - Key statistics table
    - Executive summary table
    
    **Settings:**
    - All 12 components
    - 5-year period
    - Professional formatting
    - High-resolution exports

#### Detailed Analysis Export

!!! example "Analyst Package"
    **Contents:**
    - Multiple chart types
    - Various time periods
    - Component-specific analysis
    - Statistical deep dive
    
    **Settings:**
    - Selected components focus
    - Custom time periods
    - Multiple visualizations
    - Detailed statistics

#### Risk Assessment Export

!!! example "Risk Management Package"
    **Contents:**
    - Volatility analysis charts
    - Standard deviation focus
    - Min/max range analysis
    - Correlation patterns
    
    **Settings:**
    - High-volatility components
    - Multiple time horizons
    - Statistical emphasis
    - Risk metrics focus

## Export Quality Control

### Image Quality Standards

!!! success "High-Quality Exports"
    - **Resolution**: 300 DPI for print quality
    - **Format**: PNG for lossless quality
    - **Colors**: Accurate color reproduction
    - **Text**: Clear, readable labels
    - **Scaling**: Proper size for presentations

### Content Validation

Before export, the dashboard validates:

- **Data Completeness**: All selected data available
- **Chart Rendering**: Proper visualization display
- **Statistical Accuracy**: Correct calculations
- **Label Clarity**: Readable text and legends

## Troubleshooting Exports

??? question "Exports not generating"
    **Possible Causes:**
    - Export functionality disabled
    - Insufficient permissions
    - Directory access issues
    
    **Solutions:**
    - Check export settings
    - Verify file permissions
    - Create export directories

??? question "Poor export quality"
    **Possible Causes:**
    - Low resolution settings
    - Browser rendering issues
    - Large dataset complexity
    
    **Solutions:**
    - Increase DPI settings
    - Refresh browser
    - Simplify selections

??? question "Export files not found"
    **Possible Causes:**
    - Incorrect export directory
    - File naming conflicts
    - Browser download settings
    
    **Solutions:**
    - Check export folder
    - Review file naming
    - Verify browser settings

## Best Practices

### Export Planning

!!! tip "Effective Export Strategy"
    1. **Plan Analysis First**: Know what you want to export
    2. **Configure Settings**: Set up proper time periods and components
    3. **Review Before Export**: Verify charts and tables are correct
    4. **Organize Files**: Use consistent naming and directory structure
    5. **Document Context**: Include analysis notes and assumptions

### Export Workflow

1. **Preparation Phase**
   - Define analysis objectives
   - Select appropriate time periods
   - Choose relevant components

2. **Analysis Phase**
   - Generate visualizations
   - Review statistical results
   - Validate data quality

3. **Export Phase**
   - Configure export settings
   - Generate files
   - Verify export quality

4. **Documentation Phase**
   - Add context notes
   - Create summaries
   - Archive complete analysis

## Next Steps

Continue exploring the dashboard:

- [Dashboard Tab named "Portfolios"](tab-portfolios.md) - Advanced analysis techniques
- [Data Filtering](data-filtering.md) - Refine your analysis focus
- [Dashboard Overview](overview.md) - Complete feature tour