# Portfolio Analysis

The portfolio analysis module provides comprehensive tools for analyzing ETF weight distributions and performance over time.

## Analysis Features

### Weight Distribution Analysis

The core functionality focuses on understanding how portfolio weights change over time across different ETF components.

!!! success "Key Capabilities"
    - **12 ETF Components**: Analyze up to 12 different ETF components
    - **Flexible Selection**: Choose any combination of components
    - **Real-Time Updates**: Immediate recalculation when selection changes
    - **Multiple Visualizations**: Various chart types for different insights

### Component Selection System

#### Default Selection Behavior

- **Initial State**: First 3 ETF components selected by default
- **Rationale**: Provides immediate analysis capability while maintaining performance
- **User Control**: Full flexibility to modify selection

#### Interactive Selection

=== "Individual Selection"
    **Checkbox Interface:**
    - Each ETF component has individual checkbox
    - Check/uncheck for custom combinations
    - Real-time count display shows "X of 12 components selected"
    
    **Example Workflows:**
    - Start with 3 → Add 2 more → Now analyzing 5 components
    - Select 7 specific components → Focus on key holdings
    - Choose 1 component → Detailed individual analysis

=== "Bulk Selection"
    **Select All Feature:**
    - "Select All ETFs" checkbox controls all components
    - Toggle between full portfolio and custom selection
    - Useful for comprehensive analysis
    
    **Usage Patterns:**
    - Full portfolio view: All 12 components
    - Quick reset: Deselect all, then choose specific ones
    - Comparison: All vs. subset analysis

#### Selection Synchronization

!!! info "Real-Time Synchronization"
    When component selection changes:
    
    1. **Main Chart Updates**: Shows only selected components
    2. **Statistics Recalculate**: Based on selected subset
    3. **Composition Chart**: Reflects current selection
    4. **Data Info Updates**: Shows component count and names

## Visualization Types

### Stacked Area Chart (Default)

**Best For**: Understanding portfolio composition flow over time

**Features:**
- Shows cumulative weight distribution
- Easy to see proportion changes
- Stacked layers for each component
- Interactive hover details

**Use Cases:**
- Portfolio rebalancing analysis
- Composition drift identification
- Allocation trend analysis

### Line Chart

**Best For**: Individual component trend analysis

**Features:**
- Clear trend lines for each component
- Individual component performance
- Easy comparison of trajectories
- Detailed hover information

**Use Cases:**
- Component-specific analysis
- Correlation identification
- Performance comparison

### Stacked Bar Chart

**Best For**: Discrete time period comparisons

**Features:**
- Bar representation of weights
- Good for specific date analysis
- Clear period-to-period comparison
- Automatic downsampling for performance

**Use Cases:**
- Monthly/quarterly snapshots
- Rebalancing event analysis
- Specific date investigations

### Heatmap

**Best For**: Pattern identification and correlation analysis

**Features:**
- Color-coded weight intensity
- Pattern recognition capability
- Time-series correlation visualization
- Compact representation

**Use Cases:**
- Pattern detection
- Correlation analysis
- Historical behavior review

## Statistical Analysis

### Comprehensive Metrics

For each selected component, the dashboard calculates:

| Metric | Calculation | Interpretation |
|--------|-------------|----------------|
| **Latest** | Most recent weight value | Current allocation percentage |
| **Average** | Historical mean across selected period | Typical allocation level |
| **Min** | Minimum weight in period | Lowest allocation point |
| **Max** | Maximum weight in period | Highest allocation point |
| **StdDev** | Standard deviation | Volatility/stability measure |

### Percentage vs. Absolute Views

=== "Percentage View"
    **When Enabled:**
    - All weights normalized to 100% of selected components
    - Useful for relative comparison
    - Shows proportion changes clearly
    
    **Calculation:**
    ```
    Component_Percentage = (Component_Weight / Sum_Selected_Weights) × 100
    ```

=== "Absolute View"
    **When Disabled:**
    - Raw weight values displayed
    - Shows actual allocation levels
    - Useful for absolute analysis
    
    **Usage:**
    - Actual portfolio weights
    - Absolute allocation analysis
    - Raw data examination

### Time Period Impact

!!! tip "Statistical Variations by Period"
    - **1 Year**: Recent trends and volatility
    - **3 Years**: Medium-term patterns
    - **5 Years**: Balanced historical view (default)
    - **10 Years**: Long-term behavior
    - **YTD**: Current year performance
    - **Custom**: Event-specific analysis

## Advanced Analysis Workflows

### Component Comparison Analysis

1. **Start with Default Selection**
   - Review 3-component baseline
   - Understand primary holdings

2. **Expand Selection Gradually**
   - Add 1-2 components at a time
   - Observe impact on statistics
   - Note correlation patterns

3. **Full Portfolio Review**
   - Select all 12 components
   - Comprehensive overview
   - Identify outliers

### Volatility Analysis

1. **Focus on Standard Deviation**
   - High StdDev = High volatility
   - Low StdDev = Stable allocation
   - Compare across components

2. **Time Period Sensitivity**
   - Short periods: Recent volatility
   - Long periods: Historical stability
   - Custom periods: Event analysis

3. **Visualization Selection**
   - Line charts: Individual volatility patterns
   - Heatmaps: Volatility correlation
   - Area charts: Aggregate stability

### Rebalancing Analysis

1. **Identify Rebalancing Events**
   - Sharp changes in line charts
   - Color transitions in heatmaps
   - Statistical outliers in tables

2. **Analyze Impact**
   - Before/after comparisons
   - Component selection focus
   - Custom date ranges

3. **Pattern Recognition**
   - Regular rebalancing schedules
   - Threshold-based rebalancing
   - Market event responses

## Data Information Panel

### Real-Time Status Display

The Data Information panel provides current analysis context:

!!! info "Information Elements"
    - **Period**: Selected time range
    - **Chart Type**: Current visualization
    - **Data Points**: Number of data points in analysis
    - **Components**: Count of selected components
    - **Selected**: Names of chosen components (if ≤5)
    - **Status**: Data availability and readiness

### Component Status Indicators

| Status | Meaning | Action |
|--------|---------|--------|
| ✅ **Ready for analysis** | Sufficient data, multiple components | Proceed with analysis |
| ⚠️ **Limited data available** | Few data points | Consider longer time period |
| ❌ **No components selected** | No analysis possible | Select components |
| ❌ **No data available** | Data loading issue | Check data files |

## Performance Considerations

### Automatic Optimizations

!!! success "Built-in Performance Features"
    - **Data Downsampling**: Large datasets automatically reduced to 200 points
    - **Lazy Loading**: Charts render only when needed
    - **Efficient Calculations**: Optimized statistical computations
    - **Responsive Updates**: Smooth transitions between selections

### Best Practices

1. **Start Small**: Begin with few components, expand as needed
2. **Use Appropriate Periods**: Match time period to analysis needs
3. **Leverage Downsampling**: Trust automatic optimization for large datasets
4. **Monitor Performance**: Use Data Information panel for status

## Troubleshooting

??? question "Components not updating"
    - Verify checkbox selection is working
    - Check Data Information panel status
    - Refresh browser if needed

??? question "Statistics seem incorrect"
    - Verify time period selection
    - Check percentage vs. absolute view setting
    - Ensure components are properly selected

??? question "Charts loading slowly"
    - Large datasets may need processing time
    - Consider shorter time periods for faster response
    - Check system resources

## Next Steps

Continue exploring:

- [Data Filtering](data-filtering.md) - Advanced filtering techniques
- [Export Features](export.md) - Saving your analysis
- [Development Guide](../development/contributing.md) - Contributing improvements