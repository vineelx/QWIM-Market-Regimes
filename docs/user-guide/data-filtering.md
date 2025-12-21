# Data Filtering

The QWIM Dashboard provides flexible data filtering capabilities to focus your analysis on specific time periods and portfolio components.

## Time Period Filtering

### Preset Time Periods

The dashboard offers convenient preset options for common analysis timeframes:

=== "Short-Term Analysis"
    **1 Year (1Y)**
    - Last 12 months of data
    - Recent performance focus
    - High-resolution recent trends
    
    **Year to Date (YTD)**
    - January 1st to current date
    - Current year performance
    - Budget/planning analysis

=== "Medium-Term Analysis"
    **3 Years (3Y)**
    - 3-year historical window
    - Market cycle analysis
    - Medium-term trend identification
    
    **5 Years (5Y) - Default**
    - Balanced historical perspective
    - Multiple market conditions
    - Comprehensive trend analysis

=== "Long-Term Analysis"
    **10 Years (10Y)**
    - Long-term historical view
    - Multiple economic cycles
    - Strategic allocation analysis

### Custom Date Range

!!! tip "Custom Period Selection"
    For specific analysis needs:
    
    - **Event Analysis**: Focus on specific market events
    - **Comparison Periods**: Analyze similar timeframes
    - **Detailed Investigation**: Zoom into specific periods
    
    **Usage:**
    1. Select "Custom" from time period dropdown
    2. Choose start and end dates
    3. Apply filter for immediate update

### Time Period Impact on Analysis

| Period | Data Points | Best For | Considerations |
|--------|-------------|----------|----------------|
| **1Y** | ~252 trading days | Recent trends | May miss cyclical patterns |
| **3Y** | ~750 points | Medium-term analysis | Good balance of detail/overview |
| **5Y** | ~1,250 points | Default comprehensive view | Recommended starting point |
| **10Y** | ~2,500 points | Long-term patterns | May include regime changes |
| **YTD** | Variable | Current year focus | Changes throughout year |
| **Custom** | Variable | Specific investigations | User-defined scope |

## Component Filtering

### Selection Strategies

#### Conservative Selection (3-5 Components)

**Benefits:**
- Clear, focused analysis
- Fast rendering and updates
- Easy to interpret results
- Good for specific investigation

**Use Cases:**
- Core holdings analysis
- Specific sector focus
- Detailed component comparison
- Initial exploration

#### Moderate Selection (6-8 Components)

**Benefits:**
- Balanced detail and overview
- Moderate complexity
- Still manageable visualization
- Good coverage without overwhelm

**Use Cases:**
- Sector diversification analysis
- Risk distribution review
- Comparative analysis
- Portfolio subset focus

#### Comprehensive Selection (9-12 Components)

**Benefits:**
- Complete portfolio view
- Full diversification picture
- No components excluded
- Complete statistical analysis

**Use Cases:**
- Full portfolio review
- Complete risk assessment
- Comprehensive reporting
- Strategic analysis

### Dynamic Component Selection

#### Real-Time Selection Changes

!!! success "Immediate Updates"
    When you change component selection:
    
    1. **Charts Redraw**: All visualizations update instantly
    2. **Statistics Recalculate**: New metrics for selected subset
    3. **Data Info Updates**: Current selection summary refreshes
    4. **Export Ready**: All exports reflect new selection

#### Selection Patterns

=== "Progressive Analysis"
    **Workflow:**
    1. Start with default 3 components
    2. Add components one by one
    3. Observe impact of each addition
    4. Build understanding progressively
    
    **Benefits:**
    - Controlled complexity increase
    - Clear impact understanding
    - Educational approach

=== "Comparative Analysis"
    **Workflow:**
    1. Select specific component group
    2. Analyze characteristics
    3. Switch to different group
    4. Compare results
    
    **Benefits:**
    - Focused comparisons
    - Clear differentiation
    - Targeted insights

=== "Full Portfolio Baseline"
    **Workflow:**
    1. Start with all 12 components
    2. Identify outliers or patterns
    3. Focus on specific subsets
    4. Return to full view for context
    
    **Benefits:**
    - Complete context first
    - Top-down analysis approach
    - No missing perspective

### Advanced Filtering Techniques

#### Component Correlation Analysis

1. **Select Similar Components**
   - Choose components from same sector
   - Analyze correlation patterns
   - Understand shared risk factors

2. **Select Diverse Components**
   - Choose across different sectors
   - Analyze diversification benefits
   - Understand portfolio balance

3. **Outlier Analysis**
   - Select components with extreme statistics
   - Focus on high/low volatility
   - Investigate unusual patterns

#### Time Period + Component Combinations

!!! info "Powerful Analysis Combinations"
    **Crisis Period Analysis:**
    - Custom date range around market events
    - Select vulnerable components
    - Analyze stress behavior
    
    **Growth Period Analysis:**
    - Bull market time periods
    - Select growth-oriented components
    - Understand momentum patterns
    
    **Rebalancing Analysis:**
    - Specific rebalancing dates
    - Select affected components
    - Understand rebalancing impact

## Filtering Performance

### Automatic Optimizations

The dashboard automatically optimizes performance based on your filtering choices:

| Filter Combination | Optimization | User Experience |
|-------------------|--------------|------------------|
| **Large Time Period + Many Components** | Aggressive downsampling | Smooth rendering |
| **Short Period + Few Components** | Minimal processing | High detail |
| **Custom Period + Specific Components** | Targeted calculation | Fast updates |
| **YTD + All Components** | Current year focus | Real-time relevance |

### Performance Best Practices

!!! tip "Optimal Filtering"
    1. **Start Simple**: Begin with default settings
    2. **Add Gradually**: Increase complexity step by step
    3. **Use Presets**: Leverage preset time periods when possible
    4. **Monitor Response**: Watch for performance indicators
    5. **Reset When Needed**: Return to defaults if system slows

## Filter State Management

### Session Persistence

The dashboard maintains your filter selections during your session:

- **Component Selection**: Remembers checked components
- **Time Period**: Maintains period choice
- **Visualization Options**: Preserves chart type and settings
- **Navigation**: Retains state when switching tabs

### Filter Reset Options

=== "Partial Reset"
    **Component Reset:**
    - Uncheck all components
    - Return to 3-component default
    - Keep time period and other settings
    
    **Time Period Reset:**
    - Return to 5-year default
    - Keep component selections
    - Maintain visualization settings

=== "Complete Reset"
    **Full Default Restoration:**
    - 5-year time period
    - First 3 components selected
    - Stacked area chart
    - Absolute weight view

### Filter Validation

The dashboard validates filter combinations:

!!! warning "Filter Validation Rules"
    - **Minimum Components**: At least 1 component must be selected
    - **Valid Date Range**: End date must be after start date
    - **Data Availability**: Warns if no data exists for selection
    - **Performance Limits**: May suggest optimization for large selections

## Troubleshooting Filters

??? question "No data appears after filtering"
    **Possible Causes:**
    - Selected time period has no data
    - No components selected
    - Custom date range is invalid
    
    **Solutions:**
    - Try different time period
    - Select at least one component
    - Verify custom date range

??? question "Filtering is slow"
    **Possible Causes:**
    - Too many components selected
    - Very large time period
    - Browser performance limits
    
    **Solutions:**
    - Reduce number of components
    - Use shorter time periods
    - Refresh browser tab

??? question "Filter changes not applying"
    **Possible Causes:**
    - Browser cache issues
    - Session state problems
    - Network connectivity
    
    **Solutions:**
    - Refresh browser page
    - Clear browser cache
    - Check network connection

## Next Steps

Learn about additional features:

- [Export Features](export.md) - Save filtered analysis
- [Dashboard Tab named "Portfolios"](tab-portfolios.md) - Deep dive into analysis techniques
- [Dashboard Overview](overview.md) - Complete feature overview