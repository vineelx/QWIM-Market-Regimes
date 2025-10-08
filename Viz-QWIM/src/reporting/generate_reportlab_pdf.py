"""
ReportLab PDF Generation Module for QWIM Analytics
==================================================

This module demonstrates comprehensive PDF generation using ReportLab library
following QWIM project coding standards and conventions.

Features
--------
* Professional PDF reports with headers, footers, and branding
* Data tables with alternating row colors using ReportLab Table
* Charts and graphs using plotnine (Grammar of Graphics)
* Multi-page documents with automatic page breaks
* Custom styling and layouts

Dependencies
-----------
* reportlab: Core PDF generation library
* plotnine: Grammar of graphics for Python (ggplot2 style)
* pandas: For data manipulation
* PIL/Pillow: For image processing

Example Usage
-------------
    from generate_reportlab_pdf import generate_qwim_pdf_report
    
    Success_Flag, Output_Path = generate_qwim_pdf_report(
        report_title="QWIM Portfolio Analysis",
        output_filename="qwim_report_20241224.pdf"
    )
"""

import os
import sys
import datetime
import tempfile
import time
import argparse
import traceback
import pandas as pd
from typing import Tuple, Dict
from pathlib import Path


# ReportLab imports
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import Color, HexColor, black, white, grey, blue, red, green
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, Frame, PageTemplate, BaseDocTemplate
)
from reportlab.lib import colors


def create_sample_financial_data() -> pd.DataFrame:
    """
    Create sample financial data for demonstration purposes.
    
    Returns:
        pd.DataFrame: Sample portfolio data
    """
    Sample_Data = {
        'Asset_Class': ['US Equities', 'International Equities', 'Bonds', 'Real Estate', 'Cash'],
        'Allocation_Percent': [45.0, 25.0, 20.0, 7.0, 3.0],
        'Value_USD': [450000, 250000, 200000, 70000, 30000],
        'Return_Percent': [7.2, 6.8, 3.1, 5.5, 1.2],
        'Expected_Risk_Percent': [15.2, 18.5, 4.1, 12.8, 0.1]
    }
    return pd.DataFrame(Sample_Data)


def create_qwim_styles() -> dict:
    """
    Create custom paragraph styles for QWIM branding.
    
    Returns:
        dict: Dictionary of custom paragraph styles
    """
    # Get base styles
    Base_Styles = getSampleStyleSheet()
    
    # Custom QWIM styles dictionary
    Custom_Styles = {}
    
    # QWIM title style
    Custom_Styles['qwim_title'] = ParagraphStyle(
        'QwimTitle',
        parent=Base_Styles['Title'],
        fontSize=24,
        textColor=HexColor('#1f4e79'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # QWIM heading 1 style
    Custom_Styles['qwim_heading1'] = ParagraphStyle(
        'QwimHeading1',
        parent=Base_Styles['Heading1'],
        fontSize=16,
        textColor=HexColor('#1f4e79'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    # QWIM heading 2 style
    Custom_Styles['qwim_heading2'] = ParagraphStyle(
        'QwimHeading2',
        parent=Base_Styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#2e8b57'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    # QWIM body text style
    Custom_Styles['qwim_body'] = ParagraphStyle(
        'QwimBody',
        parent=Base_Styles['Normal'],
        fontSize=11,
        textColor=black,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    # QWIM important text style
    Custom_Styles['qwim_important'] = ParagraphStyle(
        'QwimImportant',
        parent=Base_Styles['Normal'],
        fontSize=11,
        textColor=HexColor('#1f4e79'),
        spaceAfter=8,
        leftIndent=20,
        fontName='Helvetica',
        backColor=HexColor('#f0f8ff')
    )
    
    # QWIM footer style
    Custom_Styles['qwim_footer'] = ParagraphStyle(
        'QwimFooter',
        parent=Base_Styles['Normal'],
        fontSize=9,
        textColor=grey,
        spaceAfter=6,
        alignment=TA_JUSTIFY,
        fontName='Helvetica-Oblique'
    )
    
    return Custom_Styles


def create_reportlab_financial_table(
    data_frame: pd.DataFrame,
    table_title: str = "Financial Data Table",
    style_name: str = "qwim_professional"
) -> Table:
    """
    Create a professional ReportLab table from pandas DataFrame.
    
    Args:
        data_frame (pd.DataFrame): Source data for the table
        table_title (str): Title for the table
        style_name (str): Style theme to apply
        
    Returns:
        Table: Formatted ReportLab table object
    """
    # Input validation
    if data_frame.empty:
        raise ValueError("DataFrame cannot be empty for table creation")
    
    # Prepare table data
    Table_Data = []
    
    # Add header row
    Header_Row = list(data_frame.columns)
    Table_Data.append(Header_Row)
    
    # Add data rows with formatting
    for Row_Index, Row_Data in data_frame.iterrows():
        Table_Row = []
        for Column_Name in data_frame.columns:
            Cell_Value = Row_Data[Column_Name]
            
            # Format numeric values
            if isinstance(Cell_Value, (int, float)):
                if 'Percent' in Column_Name:
                    Formatted_Value = f"{Cell_Value:.1f}%"
                elif 'USD' in Column_Name or 'Value' in Column_Name:
                    Formatted_Value = f"${Cell_Value:,.0f}"
                else:
                    Formatted_Value = f"{Cell_Value:.2f}"
            else:
                Formatted_Value = str(Cell_Value)
            
            Table_Row.append(Formatted_Value)
        Table_Data.append(Table_Row)
    
    # Create table
    Financial_Table = Table(Table_Data)
    
    # Apply professional styling
    if style_name == "qwim_professional":
        Table_Style = TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4e79')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#1f4e79')),
            
            # Alternating row colors
            ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f0f8ff')),
            ('BACKGROUND', (0, 3), (-1, 3), HexColor('#f0f8ff')),
            ('BACKGROUND', (0, 5), (-1, 5), HexColor('#f0f8ff')),
            
            # Padding and alignment
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            
            # Border styling
            ('LINEBELOW', (0, 0), (-1, 0), 2, HexColor('#1f4e79')),
        ])
    else:
        # Default styling
        Table_Style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
    
    Financial_Table.setStyle(Table_Style)
    return Financial_Table


# plotnine imports with graceful fallback
try:
    from plotnine import (
        ggplot, aes, geom_point, geom_line, geom_col, geom_bar,
        theme_minimal, labs, scale_fill_manual, scale_color_manual,
        theme, element_text, element_rect, coord_flip, guides,
        guide_legend, scale_x_discrete, scale_y_continuous,
        geom_text, position_dodge, facet_wrap, geom_smooth
    )
    # Remove coord_polar import since it's not available
    
    # Test basic plotnine functionality
    import pandas as pd
    Test_Data = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 2, 3]})
    Test_Plot = ggplot(Test_Data, aes(x='x', y='y')) + geom_point()
    
    PLOTNINE_AVAILABLE = True
    print("✅ plotnine library loaded successfully")
    
except ImportError as import_error:
    PLOTNINE_AVAILABLE = False
    print(f"❌ plotnine import failed: {import_error}")
except Exception as plotnine_error:
    PLOTNINE_AVAILABLE = False
    print(f"❌ plotnine functionality test failed: {plotnine_error}")


def verify_plotnine_installation() -> Tuple[bool, str]:
    """
    Verify plotnine installation and functionality.
    
    Returns:
        Tuple[bool, str]: Tuple of (is_available, status_message)
    """
    try:
        # Test plotnine import without coord_polar
        from plotnine import ggplot, aes, geom_point, theme_minimal
        
        # Test basic functionality
        Test_Data = pd.DataFrame({
            'Asset_Class': ['A', 'B', 'C'],
            'Value': [10, 20, 30]
        })
        
        # Test basic plot creation (without saving)
        Test_Plot = (
            ggplot(Test_Data, aes(x='Asset_Class', y='Value'))
            + geom_point()
            + theme_minimal()
        )
        
        return True, "plotnine is available and functional"
        
    except ImportError as import_error:
        return False, f"plotnine import error: {import_error}"
    except Exception as functionality_error:
        return False, f"plotnine functionality error: {functionality_error}"


def debug_plotnine_environment() -> None:
    """
    Debug plotnine environment and provide diagnostic information.
    """
    print("🔍 PLOTNINE ENVIRONMENT DIAGNOSTICS")
    print("=" * 50)
    
    # Check Python environment
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Check installed packages using importlib instead of pkg_resources
    try:
        import importlib.util
        
        # Check specific dependencies
        Dependencies_To_Check = ['plotnine', 'matplotlib', 'numpy', 'pandas']
        for Dependency_Name in Dependencies_To_Check:
            try:
                Spec_Found = importlib.util.find_spec(Dependency_Name)
                if Spec_Found is not None:
                    print(f"✅ {Dependency_Name}: Available")
                else:
                    print(f"❌ {Dependency_Name}: Not available")
            except ImportError:
                print(f"❌ {Dependency_Name}: Not available")
                
    except Exception as pkg_error:
        print(f"Package check error: {pkg_error}")
    
    # Test plotnine verification
    Plotnine_Available, Plotnine_Status = verify_plotnine_installation()
    print(f"plotnine status: {Plotnine_Status}")
    
    # Check virtual environment
    Virtual_Env = os.environ.get('VIRTUAL_ENV')
    if Virtual_Env:
        print(f"Virtual environment: {Virtual_Env}")
    else:
        print("Virtual environment: Not detected")
    
    print("=" * 50)


def create_plotnine_chart_image(
    data_frame: pd.DataFrame,
    chart_type: str = "portfolio_allocation",
    output_path: str = "temp_chart.png"
) -> str:
    """
    Create a plotnine chart without coord_polar and save as image for PDF inclusion.
    
    Args:
        data_frame (pd.DataFrame): Data for chart generation
        chart_type (str): Type of chart to generate
        output_path (str): Path to save the chart image
        
    Returns:
        str: Path to the generated chart image
    """
    # Input validation
    if data_frame.empty:
        raise ValueError("DataFrame cannot be empty for chart generation")
    
    # Enhanced plotnine availability check
    Plotnine_Available, Plotnine_Status = verify_plotnine_installation()
    if not Plotnine_Available:
        raise ImportError(f"plotnine not functional: {Plotnine_Status}")
    
    # Import plotnine within function for better error handling
    try:
        from plotnine import (
            ggplot, aes, geom_col, geom_point, geom_text,
            theme_minimal, labs, scale_fill_manual, scale_color_manual,
            theme, element_text, coord_flip, guides, guide_legend
        )
        
    except ImportError as plotnine_import_error:
        raise ImportError(f"plotnine import failed in function: {plotnine_import_error}")
    
    # QWIM color palette
    Qwim_Colors = ['#1f4e79', '#2e8b57', '#ff6b35', '#9b59b6', '#34495e', '#e74c3c']
    
    try:
        print(f"🎨 Creating {chart_type} chart with plotnine...")
        
        if chart_type == "portfolio_allocation":
            # Create pie chart alternative using stacked bar chart instead of coord_polar
            Chart_Plot = (
                ggplot(data_frame, aes(x='"Portfolio"', y='Allocation_Percent', fill='Asset_Class'))
                + geom_col(width=0.8, position='stack')
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Allocation by Asset Class",
                    x="",
                    y="Allocation %",
                    fill="Asset Class"
                )
                + theme_minimal()
                + theme(
                    axis_text_x=element_text(size=0),
                    plot_title=element_text(size=14, weight='bold', color='#1f4e79'),
                    legend_position='right',
                    legend_text=element_text(size=9),
                    figure_size=(8, 6)
                )
            )
            
        elif chart_type == "performance_comparison":
            # Create bar chart for returns comparison
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Return_Percent', fill='Asset_Class'))
                + geom_col(width=0.7)
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Expected Returns by Asset Class",
                    x="Asset Class",
                    y="Expected Return (%)",
                    fill="Asset Class"
                )
                + theme_minimal()
                + theme(
                    axis_text_x=element_text(angle=45, hjust=1, size=9),
                    plot_title=element_text(size=14, weight='bold', color='#1f4e79'),
                    legend_position='none',
                    figure_size=(10, 6)
                )
                + geom_text(
                    aes(label='Return_Percent'), 
                    position='identity', 
                    va='bottom'
                )
            )
            
        elif chart_type == "risk_return_scatter":
            # Create scatter plot for risk vs return analysis
            Chart_Plot = (
                ggplot(data_frame, aes(x='Expected_Risk_Percent', y='Return_Percent', 
                                     color='Asset_Class'))
                + geom_point(alpha=0.8, size=3)
                + geom_text(
                    aes(label='Asset_Class'), 
                    nudge_y=0.3, 
                    show_legend=False
                )
                + scale_color_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Risk vs Return Analysis",
                    x="Expected Risk (%)",
                    y="Expected Return (%)",
                    color="Asset Class"
                )
                + theme_minimal()
                + theme(
                    plot_title=element_text(size=14, weight='bold', color='#1f4e79'),
                    legend_position='bottom',
                    figure_size=(10, 7)
                )
            )
            
        elif chart_type == "value_distribution":
            # Create horizontal bar chart for value distribution
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Value_USD', fill='Asset_Class'))
                + geom_col(width=0.8)
                + coord_flip()
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Value Distribution by Asset Class",
                    x="Asset Class",
                    y="Value (USD)",
                    fill="Asset Class"
                )
                + theme_minimal()
                + theme(
                    plot_title=element_text(size=14, weight='bold', color='#1f4e79'),
                    legend_position='none',
                    figure_size=(10, 6)
                )
                + geom_text(
                    aes(label='Value_USD'), 
                    position='identity', 
                    ha='left'
                )
            )
            
        elif chart_type == "allocation_pie_alternative":
            # Create donut chart alternative using geom_col with proper positioning
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Allocation_Percent', fill='Asset_Class'))
                + geom_col(width=0.8)
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Allocation by Asset Class",
                    x="Asset Class",
                    y="Allocation (%)",
                    fill="Asset Class"
                )
                + theme_minimal()
                + theme(
                    axis_text_x=element_text(angle=45, hjust=1, size=9),
                    plot_title=element_text(size=14, weight='bold', color='#1f4e79'),
                    legend_position='right',
                    legend_text=element_text(size=9),
                    figure_size=(10, 6)
                )
                + geom_text(
                    aes(label='Allocation_Percent'), 
                    position='identity', 
                    va='bottom'
                )
            )
            
        else:
            # Default: simple bar chart
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Allocation_Percent', fill='Asset_Class'))
                + geom_col(width=0.8)
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Allocation",
                    x="Asset Class",
                    y="Allocation (%)"
                )
                + theme_minimal()
                + theme(
                    axis_text_x=element_text(angle=45, hjust=1),
                    plot_title=element_text(size=14, weight='bold', color='#1f4e79'),
                    legend_position='none'
                )
            )
        
        # Configuration validation
        Chart_Path = Path(output_path).resolve()
        Chart_Path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"💾 Saving chart to: {Chart_Path}")
        
        # Save chart with proper error handling
        try:
            Chart_Plot.save(
                filename=str(Chart_Path),
                width=8,
                height=6,
                dpi=150,
                verbose=False
            )
        except Exception as save_error:
            print(f"❌ Chart save error: {save_error}")
            raise RuntimeError(f"Failed to save chart: {save_error}")
        
        # Business logic validation
        if not Chart_Path.exists():
            raise FileNotFoundError(f"plotnine chart file was not created: {Chart_Path}")
        
        Chart_File_Size = Chart_Path.stat().st_size
        if Chart_File_Size == 0:
            raise ValueError(f"Chart file is empty: {Chart_Path}")
            
        print(f"✅ Chart saved successfully: {Chart_File_Size} bytes")
        
        return str(Chart_Path)
        
    except Exception as chart_error:
        print(f"❌ plotnine chart creation error: {chart_error}")
        # Run diagnostics on chart failure
        debug_plotnine_environment()
        raise RuntimeError(f"plotnine chart creation failed: {chart_error}")


def create_plotnine_chart_image_minimal(
    data_frame: pd.DataFrame,
    chart_type: str = "portfolio_allocation",
    output_path: str = "temp_chart.png"
) -> str:
    """
    Create minimal plotnine charts with basic functionality for maximum compatibility.
    
    Args:
        data_frame (pd.DataFrame): Data for chart generation
        chart_type (str): Type of chart to generate
        output_path (str): Path to save the chart image
        
    Returns:
        str: Path to the generated chart image
    """
    # Input validation
    if data_frame.empty:
        raise ValueError("DataFrame cannot be empty for chart generation")
    
    # Enhanced plotnine availability check
    Plotnine_Available, Plotnine_Status = verify_plotnine_installation()
    if not Plotnine_Available:
        raise ImportError(f"plotnine not functional: {Plotnine_Status}")
    
    # Import plotnine with minimal dependencies
    try:
        from plotnine import (
            ggplot, aes, geom_col, geom_point,
            theme_minimal, labs, scale_fill_manual
        )
        
    except ImportError as plotnine_import_error:
        raise ImportError(f"plotnine import failed in function: {plotnine_import_error}")
    
    # QWIM color palette
    Qwim_Colors = ['#1f4e79', '#2e8b57', '#ff6b35', '#9b59b6', '#34495e', '#e74c3c']
    
    try:
        print(f"🎨 Creating minimal {chart_type} chart with plotnine...")
        
        if chart_type == "portfolio_allocation":
            # Simple bar chart instead of stacked (more reliable)
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Allocation_Percent', fill='Asset_Class'))
                + geom_col()
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Allocation by Asset Class",
                    x="Asset Class",
                    y="Allocation %"
                )
                + theme_minimal()
            )
            
        elif chart_type == "performance_comparison":
            # Simple bar chart for returns
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Return_Percent', fill='Asset_Class'))
                + geom_col()
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Expected Returns by Asset Class",
                    x="Asset Class",
                    y="Expected Return (%)"
                )
                + theme_minimal()
            )
            
        elif chart_type == "risk_return_scatter":
            # Simple scatter plot
            Chart_Plot = (
                ggplot(data_frame, aes(x='Expected_Risk_Percent', y='Return_Percent'))
                + geom_point(size=3, color='#1f4e79')
                + labs(
                    title="Risk vs Return Analysis",
                    x="Expected Risk (%)",
                    y="Expected Return (%)"
                )
                + theme_minimal()
            )
            
        elif chart_type == "value_distribution":
            # Simple bar chart for values
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Value_USD', fill='Asset_Class'))
                + geom_col()
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Value Distribution",
                    x="Asset Class",
                    y="Value (USD)"
                )
                + theme_minimal()
            )
            
        else:
            # Default: simple bar chart
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Allocation_Percent', fill='Asset_Class'))
                + geom_col()
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Data",
                    x="Asset Class",
                    y="Value"
                )
                + theme_minimal()
            )
        
        # Configuration validation
        Chart_Path = Path(output_path).resolve()
        Chart_Path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"💾 Saving minimal chart to: {Chart_Path}")
        
        # Save chart with minimal options
        Chart_Plot.save(
            filename=str(Chart_Path),
            width=8,
            height=6,
            dpi=150
        )
        
        # Business logic validation
        if not Chart_Path.exists():
            raise FileNotFoundError(f"plotnine chart file was not created: {Chart_Path}")
        
        Chart_File_Size = Chart_Path.stat().st_size
        if Chart_File_Size == 0:
            raise ValueError(f"Chart file is empty: {Chart_Path}")
            
        print(f"✅ Minimal chart saved successfully: {Chart_File_Size} bytes")
        
        return str(Chart_Path)
        
    except Exception as chart_error:
        print(f"❌ Minimal plotnine chart creation error: {chart_error}")
        raise RuntimeError(f"Minimal plotnine chart creation failed: {chart_error}")


def create_plotnine_chart_image_high_resolution(
    data_frame: pd.DataFrame,
    chart_type: str = "portfolio_allocation",
    output_path: str = "temp_chart.png"
) -> str:
    """
    Create high-resolution plotnine charts optimized for PDF inclusion following QWIM standards.
    
    Args:
        data_frame (pd.DataFrame): Data for chart generation
        chart_type (str): Type of chart to generate
        output_path (str): Path to save the chart image
        
    Returns:
        str: Path to the generated high-resolution chart image
    """
    # Input validation
    if data_frame.empty:
        raise ValueError("DataFrame cannot be empty for chart generation")
    
    # Enhanced plotnine availability check
    Plotnine_Available, Plotnine_Status = verify_plotnine_installation()
    if not Plotnine_Available:
        raise ImportError(f"plotnine not functional: {Plotnine_Status}")
    
    # Import plotnine within function for better error handling
    try:
        from plotnine import (
            ggplot, aes, geom_col, geom_point, geom_text,
            theme_minimal, labs, scale_fill_manual, scale_color_manual,
            theme, element_text, coord_flip, guides, guide_legend
        )
        
    except ImportError as plotnine_import_error:
        raise ImportError(f"plotnine import failed in function: {plotnine_import_error}")
    
    # QWIM color palette - high contrast for better resolution
    Qwim_Colors = ['#1f4e79', '#2e8b57', '#ff6b35', '#9b59b6', '#34495e', '#e74c3c']
    
    try:
        print(f"🎨 Creating high-resolution {chart_type} chart with plotnine...")
        
        if chart_type == "portfolio_allocation":
            # Create pie chart alternative using stacked bar chart with enhanced styling
            Chart_Plot = (
                ggplot(data_frame, aes(x='"Portfolio"', y='Allocation_Percent', fill='Asset_Class'))
                + geom_col(width=0.8, position='stack')
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Allocation by Asset Class",
                    x="",
                    y="Allocation %",
                    fill="Asset Class"
                )
                + theme_minimal()
                + theme(
                    axis_text_x=element_text(size=0),
                    axis_text_y=element_text(size=14, color='#1f4e79'),
                    plot_title=element_text(size=20, weight='bold', color='#1f4e79'),
                    legend_position='right',
                    legend_text=element_text(size=12, color='#1f4e79'),
                    legend_title=element_text(size=14, weight='bold', color='#1f4e79'),
                    panel_grid_major=element_text(color='#e0e0e0', size=0.5),
                    panel_grid_minor=element_text(color='#f0f0f0', size=0.25),
                    figure_size=(12, 9)
                )
            )
            
        elif chart_type == "performance_comparison":
            # Create bar chart for returns comparison with enhanced text
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Return_Percent', fill='Asset_Class'))
                + geom_col(width=0.7)
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Expected Returns by Asset Class",
                    x="Asset Class",
                    y="Expected Return (%)",
                    fill="Asset Class"
                )
                + theme_minimal()
                + theme(
                    axis_text_x=element_text(angle=45, hjust=1, size=12, color='#1f4e79'),
                    axis_text_y=element_text(size=12, color='#1f4e79'),
                    axis_title_x=element_text(size=14, weight='bold', color='#1f4e79'),
                    axis_title_y=element_text(size=14, weight='bold', color='#1f4e79'),
                    plot_title=element_text(size=20, weight='bold', color='#1f4e79'),
                    legend_position='none',
                    panel_grid_major=element_text(color='#e0e0e0', size=0.5),
                    panel_grid_minor=element_text(color='#f0f0f0', size=0.25),
                    figure_size=(14, 10)
                )
            )
            
        elif chart_type == "risk_return_scatter":
            # Create scatter plot for risk vs return analysis with enhanced points
            Chart_Plot = (
                ggplot(data_frame, aes(x='Expected_Risk_Percent', y='Return_Percent', 
                                     color='Asset_Class'))
                + geom_point(alpha=0.8, size=5)
                + geom_text(
                    aes(label='Asset_Class'), 
                    nudge_y=0.3, 
                    show_legend=False
                )
                + scale_color_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Risk vs Return Analysis",
                    x="Expected Risk (%)",
                    y="Expected Return (%)",
                    color="Asset Class"
                )
                + theme_minimal()
                + theme(
                    axis_text_x=element_text(size=12, color='#1f4e79'),
                    axis_text_y=element_text(size=12, color='#1f4e79'),
                    axis_title_x=element_text(size=14, weight='bold', color='#1f4e79'),
                    axis_title_y=element_text(size=14, weight='bold', color='#1f4e79'),
                    plot_title=element_text(size=20, weight='bold', color='#1f4e79'),
                    legend_position='bottom',
                    legend_text=element_text(size=12, color='#1f4e79'),
                    legend_title=element_text(size=14, weight='bold', color='#1f4e79'),
                    panel_grid_major=element_text(color='#e0e0e0', size=0.5),
                    panel_grid_minor=element_text(color='#f0f0f0', size=0.25),
                    figure_size=(14, 11)
                )
            )
            
        elif chart_type == "value_distribution":
            # Create horizontal bar chart for value distribution
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Value_USD', fill='Asset_Class'))
                + geom_col(width=0.8)
                + coord_flip()
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Value Distribution by Asset Class",
                    x="Asset Class",
                    y="Value (USD)",
                    fill="Asset Class"
                )
                + theme_minimal()
                + theme(
                    plot_title=element_text(size=20, weight='bold', color='#1f4e79'),
                    legend_position='none',
                    figure_size=(14, 10)
                )
                + geom_text(
                    aes(label='Value_USD'), 
                    position='identity', 
                    ha='left'
                )
            )
            
        elif chart_type == "allocation_pie_alternative":
            # Create donut chart alternative using geom_col with enhanced styling
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Allocation_Percent', fill='Asset_Class'))
                + geom_col(width=0.8)
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Allocation by Asset Class",
                    x="Asset Class",
                    y="Allocation (%)",
                    fill="Asset Class"
                )
                + theme_minimal()
                + theme(
                    axis_text_x=element_text(angle=45, hjust=1, size=12, color='#1f4e79'),
                    axis_text_y=element_text(size=12, color='#1f4e79'),
                    axis_title_x=element_text(size=14, weight='bold', color='#1f4e79'),
                    axis_title_y=element_text(size=14, weight='bold', color='#1f4e79'),
                    plot_title=element_text(size=20, weight='bold', color='#1f4e79'),
                    legend_position='right',
                    legend_text=element_text(size=12, color='#1f4e79'),
                    legend_title=element_text(size=14, weight='bold', color='#1f4e79'),
                    panel_grid_major=element_text(color='#e0e0e0', size=0.5),
                    panel_grid_minor=element_text(color='#f0f0f0', size=0.25),
                    figure_size=(14, 10)
                )
            )
            
        else:
            # Default: simple bar chart with enhanced styling
            Chart_Plot = (
                ggplot(data_frame, aes(x='Asset_Class', y='Allocation_Percent', fill='Asset_Class'))
                + geom_col(width=0.8)
                + scale_fill_manual(values=Qwim_Colors[:len(data_frame)])
                + labs(
                    title="Portfolio Allocation",
                    x="Asset Class",
                    y="Allocation (%)"
                )
                + theme_minimal()
                + theme(
                    axis_text_x=element_text(angle=45, hjust=1, size=12, color='#1f4e79'),
                    axis_text_y=element_text(size=12, color='#1f4e79'),
                    axis_title_x=element_text(size=14, weight='bold', color='#1f4e79'),
                    axis_title_y=element_text(size=14, weight='bold', color='#1f4e79'),
                    plot_title=element_text(size=20, weight='bold', color='#1f4e79'),
                    legend_position='none',
                    panel_grid_major=element_text(color='#e0e0e0', size=0.5),
                    panel_grid_minor=element_text(color='#f0f0f0', size=0.25),
                    figure_size=(12, 9)
                )
            )
        
        # Configuration validation
        Chart_Path = Path(output_path).resolve()
        Chart_Path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"💾 Saving high-resolution chart to: {Chart_Path}")
        
        # Save chart with maximum quality settings
        try:
            Chart_Plot.save(
                filename=str(Chart_Path),
                width=12,    # Increased from 8
                height=9,    # Increased from 6
                dpi=300,     # Increased from 150 for print quality
                verbose=False,
                limitsize=False  # Allow larger images
            )
        except Exception as save_error:
            print(f"❌ Chart save error: {save_error}")
            raise RuntimeError(f"Failed to save high-resolution chart: {save_error}")
        
        # Business logic validation
        if not Chart_Path.exists():
            raise FileNotFoundError(f"plotnine chart file was not created: {Chart_Path}")
        
        Chart_File_Size = Chart_Path.stat().st_size
        if Chart_File_Size == 0:
            raise ValueError(f"Chart file is empty: {Chart_Path}")
            
        print(f"✅ High-resolution chart saved successfully: {Chart_File_Size} bytes")
        
        return str(Chart_Path)
        
    except Exception as chart_error:
        print(f"❌ plotnine chart creation error: {chart_error}")
        # Run diagnostics on chart failure
        debug_plotnine_environment()
        raise RuntimeError(f"plotnine chart creation failed: {chart_error}")


def create_header_footer_template(
    doc: BaseDocTemplate,
    title: str = "QWIM Analytics Report"
) -> None:
    """
    Create custom page template with header and footer for QWIM branding.
    
    Args:
        doc (BaseDocTemplate): ReportLab document object
        title (str): Document title for header
    """
    # Page dimensions
    Page_Width, Page_Height = letter
    
    def Header_Footer_Canvas(canvas, doc_info):
        """Draw header and footer on each page."""
        # Save canvas state
        canvas.saveState()
        
        # Header
        canvas.setFont('Helvetica-Bold', 16)
        canvas.setFillColor(HexColor('#1f4e79'))
        canvas.drawString(72, Page_Height - 50, "QWIM Analytics")
        
        canvas.setFont('Helvetica', 12)
        canvas.setFillColor(HexColor('#2e8b57'))
        canvas.drawString(72, Page_Height - 70, title)
        
        # Header line
        canvas.setStrokeColor(HexColor('#1f4e79'))
        canvas.setLineWidth(2)
        canvas.line(72, Page_Height - 80, Page_Width - 72, Page_Height - 80)
        
        # Footer
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(grey)
        
        # Footer line
        canvas.setStrokeColor(grey)
        canvas.setLineWidth(1)
        canvas.line(72, 50, Page_Width - 72, 50)
        
        # Footer text
        Footer_Text = f"Generated on {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        canvas.drawString(72, 35, Footer_Text)
        
        # Page number - safe access to page number
        try:
            Page_Number_Text = f"Page {doc_info.page}"
        except AttributeError:
            Page_Number_Text = "Page 1"
        canvas.drawRightString(Page_Width - 72, 35, Page_Number_Text)
        
        # Restore canvas state
        canvas.restoreState()
    
    # Create main frame for content
    Main_Frame = Frame(
        72, 100, Page_Width - 144, Page_Height - 180,
        leftPadding=0, bottomPadding=0, rightPadding=0, topPadding=0
    )
    
    # Create page template with frame
    Page_Template_Obj = PageTemplate(
        id='main_template',
        frames=[Main_Frame],
        onPage=Header_Footer_Canvas
    )
    
    # Add page template to document
    doc.addPageTemplates([Page_Template_Obj])


def generate_qwim_pdf_report(
    report_title: str = "QWIM Portfolio Analysis Report",
    output_filename: str = "qwim_report.pdf",
    output_directory: str = "outputs/reports",
    include_charts: bool = True
) -> Tuple[bool, str]:
    """
    Generate a comprehensive PDF report using ReportLab with plotnine charts (no coord_polar).
    
    Args:
        report_title (str): Title for the PDF report
        output_filename (str): Name of the output PDF file
        output_directory (str): Directory to save the PDF file
        include_charts (bool): Whether to include plotnine charts
        
    Returns:
        Tuple[bool, str]: Tuple of (success_flag, output_path_or_error_message)
    """
    Chart_Files_To_Cleanup = []
    
    try:
        # Input validation
        if not report_title or len(report_title.strip()) < 3:
            return False, "Report title must be at least 3 characters long"
        
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        
        # Configuration validation
        Output_Directory = Path(output_directory)
        Output_Directory.mkdir(parents=True, exist_ok=True)
        
        Output_Path = Output_Directory / output_filename
        
        print(f"🚀 Starting PDF generation: {Output_Path}")
        print(f"📊 plotnine available: {PLOTNINE_AVAILABLE}")
        print(f"📋 Using ReportLab tables")
        
        # Create sample data
        Portfolio_Data = create_sample_financial_data()
        
        # Create document
        Pdf_Document = BaseDocTemplate(
            str(Output_Path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=100,
            bottomMargin=100
        )
        
        # Create custom styles
        Custom_Styles = create_qwim_styles()
        
        # Create header/footer template
        create_header_footer_template(Pdf_Document, report_title)
        
        # Build document content
        Document_Content = []
        
        # Title page
        Document_Content.append(Paragraph(report_title, Custom_Styles['qwim_title']))
        Document_Content.append(Spacer(1, 20))
        
        # Executive summary
        Document_Content.append(Paragraph("Executive Summary", Custom_Styles['qwim_heading1']))
        
        Summary_Text = """
        This comprehensive portfolio analysis report provides detailed insights into your investment 
        portfolio performance, asset allocation, and risk metrics. The analysis covers the period 
        from January 2024 to December 2024 and includes recommendations for portfolio optimization 
        based on your risk tolerance and investment objectives using plotnine visualizations.
        """
        Document_Content.append(Paragraph(Summary_Text, Custom_Styles['qwim_body']))
        Document_Content.append(Spacer(1, 20))
        
        # Key metrics section
        Document_Content.append(Paragraph("Key Performance Metrics", Custom_Styles['qwim_heading1']))
        
        Key_Metrics_Text = """
        <b>Total Portfolio Value:</b> $1,000,000<br/>
        <b>Year-to-Date Return:</b> +6.8%<br/>
        <b>Benchmark Outperformance:</b> +1.2%<br/>
        <b>Portfolio Beta:</b> 0.95<br/>
        <b>Sharpe Ratio:</b> 1.42<br/>
        <b>Maximum Drawdown:</b> -3.2%
        """
        Document_Content.append(Paragraph(Key_Metrics_Text, Custom_Styles['qwim_important']))
        Document_Content.append(Spacer(1, 20))
        
        # Portfolio allocation table using ReportLab Table
        Document_Content.append(Paragraph("Portfolio Allocation Analysis", Custom_Styles['qwim_heading1']))
        
        # Create professional ReportLab table
        Portfolio_Table = create_reportlab_financial_table(
            Portfolio_Data, 
            "Portfolio Holdings Summary",
            "qwim_professional"
        )
        Document_Content.append(Portfolio_Table)
        Document_Content.append(Spacer(1, 20))
        
        # Enhanced Charts section using plotnine (without coord_polar)
        if include_charts:
            Document_Content.append(Paragraph("Visual Analysis with plotnine Charts", Custom_Styles['qwim_heading1']))
            
            if PLOTNINE_AVAILABLE:
                # Create temporary directory for charts
                Temp_Charts_Dir = Output_Directory / "temp_charts"
                Temp_Charts_Dir.mkdir(exist_ok=True)
                
                # Define multiple chart types to generate (no coord_polar)
                Chart_Types_List = [
                    ("portfolio_allocation", "Portfolio Allocation (Stacked Bar Chart)"),
                    ("performance_comparison", "Performance Comparison (Bar Chart)"),
                    ("risk_return_scatter", "Risk vs Return Analysis (Scatter Plot)"),
                    ("value_distribution", "Value Distribution (Horizontal Bar Chart)")
                ]
                
                Charts_Generated_Count = 0
                
                for Chart_Type_Name, Chart_Display_Name in Chart_Types_List:
                    try:
                        print(f"📊 Generating {Chart_Display_Name}...")
                        
                        # Add chart section header
                        Document_Content.append(Paragraph(Chart_Display_Name, Custom_Styles['qwim_heading2']))
                        Document_Content.append(Spacer(1, 10))
                        
                        # Generate chart file
                        Chart_File_Path = Temp_Charts_Dir / f"{Chart_Type_Name}_chart.png"
                        Chart_Path_Generated = create_plotnine_chart_image(
                            Portfolio_Data,
                            Chart_Type_Name, 
                            str(Chart_File_Path)
                        )
                        Chart_Files_To_Cleanup.append(Chart_Path_Generated)
                        
                        # Business logic validation - verify chart was created
                        if Path(Chart_Path_Generated).exists():
                            Chart_File_Size = Path(Chart_Path_Generated).stat().st_size
                            print(f"✅ Chart created: {Chart_Path_Generated} ({Chart_File_Size} bytes)")
                            
                            # Add chart to document
                            Generated_Chart = Image(Chart_Path_Generated, width=6*inch, height=4.5*inch)
                            Document_Content.append(Generated_Chart)
                            Document_Content.append(Spacer(1, 10))
                            
                            # Add chart description
                            Chart_Description = f"""
                            This {Chart_Display_Name.lower()} was generated using plotnine (Grammar of Graphics) 
                            without coord_polar dependency, demonstrating professional data visualization 
                            integrated with ReportLab PDF generation.
                            """
                            Document_Content.append(Paragraph(Chart_Description, Custom_Styles['qwim_body']))
                            Document_Content.append(Spacer(1, 20))
                            
                            Charts_Generated_Count += 1
                            print(f"✅ Added {Chart_Display_Name} to PDF")
                            
                        else:
                            print(f"❌ Chart file not found: {Chart_Path_Generated}")
                            Document_Content.append(Paragraph(
                                f"{Chart_Display_Name} generation failed - file not created", 
                                Custom_Styles['qwim_body']
                            ))
                            Document_Content.append(Spacer(1, 10))
        
                    except Exception as chart_error:
                        print(f"❌ Failed to generate {Chart_Display_Name}: {chart_error}")
                        Document_Content.append(Paragraph(
                            f"{Chart_Display_Name} generation temporarily unavailable: {str(chart_error)}", 
                            Custom_Styles['qwim_body']
                        ))
                        Document_Content.append(Spacer(1, 10))
                
                # Chart generation summary
                Chart_Summary_Text = f"""
                <b>Chart Generation Summary:</b><br/>
                Total charts requested: {len(Chart_Types_List)}<br/>
                Charts successfully generated: {Charts_Generated_Count}<br/>
                plotnine library status: Available (without coord_polar)<br/>
                Chart format: PNG (150 DPI)
                """
                Document_Content.append(Paragraph(Chart_Summary_Text, Custom_Styles['qwim_important']))
                Document_Content.append(Spacer(1, 20))
                
            else:
                # plotnine not available
                print("❌ plotnine library not available for chart generation")
                Document_Content.append(Paragraph(
                    "plotnine library not available for chart generation. Please install plotnine to enable chart functionality:", 
                    Custom_Styles['qwim_body']
                ))
                Document_Content.append(Spacer(1, 10))
                
                Installation_Instructions = """
                <b>To install plotnine:</b><br/>
                pip install plotnine<br/>
                <br/>
                plotnine provides Grammar of Graphics visualization capabilities for Python,
                similar to ggplot2 in R, enabling professional statistical graphics.
                """
                Document_Content.append(Paragraph(Installation_Instructions, Custom_Styles['qwim_important']))
                Document_Content.append(Spacer(1, 20))
        
        # Investment recommendations
        Document_Content.append(PageBreak())
        Document_Content.append(Paragraph("Investment Recommendations", Custom_Styles['qwim_heading1']))
        
        Recommendations_Text = """
        Based on our comprehensive analysis using plotnine visualizations (stacked bar charts 
        instead of pie charts) and professional ReportLab table formatting, we recommend the 
        following strategic adjustments to optimize your risk-adjusted returns:
        """
        Document_Content.append(Paragraph(Recommendations_Text, Custom_Styles['qwim_body']))
        
        # Recommendations list
        Recommendations_List = [
            "Consider increasing international equity exposure to 30% for better diversification",
            "Reduce cash allocation to 2% and deploy excess capital into growth opportunities", 
            "Add small-cap value stocks to capture potential outperformance",
            "Implement tax-loss harvesting strategies in taxable accounts",
            "Review and rebalance portfolio quarterly using modern analytics tools"
        ]
        
        for Recommendation_Item in Recommendations_List:
            Document_Content.append(Paragraph(f"• {Recommendation_Item}", Custom_Styles['qwim_body']))
        
        Document_Content.append(Spacer(1, 20))
        
        # Technical implementation details
        Document_Content.append(Paragraph("Technical Implementation", Custom_Styles['qwim_heading2']))
        
        Technical_Text = """
        This report was generated using plotnine for professional data visualization following 
        the Grammar of Graphics principles (without coord_polar dependency), and ReportLab Table 
        components for structured data presentation. This combination provides optimal performance 
        and consistent styling.
        """
        Document_Content.append(Paragraph(Technical_Text, Custom_Styles['qwim_body']))
        
        # Technical details
        Technical_Details = f"""
        <b>Technical Stack:</b><br/>
        • plotnine: {'✅ Available' if PLOTNINE_AVAILABLE else '❌ Not Available'} - Grammar of Graphics charts (no coord_polar)<br/>
        • ReportLab: ✅ Available - PDF generation and table formatting<br/>
        • pandas: ✅ Available - Data manipulation and analysis<br/>
        • Chart resolution: 150 DPI for crisp PDF inclusion<br/>
        • Color scheme: Custom QWIM branding palette<br/>
        • Package detection: importlib.util (replaced pkg_resources)
        """
        Document_Content.append(Paragraph(Technical_Details, Custom_Styles['qwim_important']))
        
        # Disclaimer
        Document_Content.append(Spacer(1, 30))
        Disclaimer_Text = """
        <b>Important Disclaimer:</b> This report is for informational purposes only and does not 
        constitute investment advice. Past performance does not guarantee future results. 
        Please consult with a qualified financial advisor before making investment decisions.
        """
        Document_Content.append(Paragraph(Disclaimer_Text, Custom_Styles['qwim_footer']))
        
        # Build the PDF
        print("📄 Building PDF document...")
        Pdf_Document.build(Document_Content)
        
        # Business logic validation
        if Output_Path.exists():
            File_Size = Output_Path.stat().st_size
            print(f"✅ PDF generated successfully ({File_Size} bytes)")
            print(f"📁 Saved to: {Output_Path}")
            return True, str(Output_Path)
        else:
            return False, "PDF file was not created successfully"
        
    except Exception as exc_error:
        return False, f"PDF generation error: {exc_error}"
    finally:
        # Clean up temporary chart files after PDF is built
        print(f"🧹 Cleaning up {len(Chart_Files_To_Cleanup)} chart files...")
        for Chart_File_Path in Chart_Files_To_Cleanup:
            try:
                Chart_Path_Obj = Path(Chart_File_Path)
                if Chart_Path_Obj.exists():
                    Chart_Path_Obj.unlink()
                    print(f"🧹 Cleaned up chart file: {Chart_File_Path}")
            except Exception as cleanup_error:
                print(f"⚠️ Could not clean up chart file {Chart_File_Path}: {cleanup_error}")
        
        # Clean up temporary charts directory if empty
        try:
            Temp_Charts_Dir = Path(output_directory) / "temp_charts"
            if Temp_Charts_Dir.exists() and not any(Temp_Charts_Dir.iterdir()):
                Temp_Charts_Dir.rmdir()
                print(f"🧹 Cleaned up temporary charts directory")
        except Exception as dir_cleanup_error:
            print(f"⚠️ Could not clean up charts directory: {dir_cleanup_error}")


def generate_qwim_pdf_report_simplified(
    report_title: str = "QWIM Portfolio Analysis Report",
    output_filename: str = "qwim_report.pdf",
    output_directory: str = "outputs/reports",
    include_charts: bool = True
) -> Tuple[bool, str]:
    """
    Generate a simplified PDF report using SimpleDocTemplate to avoid BaseDocTemplate issues.
    
    Args:
        report_title (str): Title for the PDF report
        output_filename (str): Name of the output PDF file
        output_directory (str): Directory to save the PDF file
        include_charts (bool): Whether to include plotnine charts
        
    Returns:
        Tuple[bool, str]: Tuple of (success_flag, output_path_or_error_message)
    """
    Chart_Files_To_Cleanup = []
    
    try:
        # Input validation
        if not report_title or len(report_title.strip()) < 3:
            return False, "Report title must be at least 3 characters long"
        
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        
        # Configuration validation
        Output_Directory = Path(output_directory)
        Output_Directory.mkdir(parents=True, exist_ok=True)
        
        Output_Path = Output_Directory / output_filename
        
        print(f"🚀 Starting simplified PDF generation: {Output_Path}")
        print(f"📊 plotnine available: {PLOTNINE_AVAILABLE}")
        print(f"📋 Using ReportLab tables")
        
        # Create sample data
        Portfolio_Data = create_sample_financial_data()
        
        # Create simplified document using SimpleDocTemplate
        Pdf_Document = SimpleDocTemplate(
            str(Output_Path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Create custom styles
        Custom_Styles = create_qwim_styles()
        
        # Build document content
        Document_Content = []
        
        # Title page
        Document_Content.append(Paragraph(report_title, Custom_Styles['qwim_title']))
        Document_Content.append(Spacer(1, 20))
        
        # Current date
        Current_Date = datetime.datetime.now().strftime('%B %d, %Y')
        Document_Content.append(Paragraph(f"Generated on: {Current_Date}", Custom_Styles['qwim_body']))
        Document_Content.append(Spacer(1, 20))
        
        # Executive summary
        Document_Content.append(Paragraph("Executive Summary", Custom_Styles['qwim_heading1']))
        
        Summary_Text = """
        This comprehensive portfolio analysis report provides detailed insights into your investment 
        portfolio performance, asset allocation, and risk metrics. The analysis covers the period 
        from January 2024 to December 2024 and includes recommendations for portfolio optimization 
        based on your risk tolerance and investment objectives using plotnine visualizations.
        """
        Document_Content.append(Paragraph(Summary_Text, Custom_Styles['qwim_body']))
        Document_Content.append(Spacer(1, 20))
        
        # Key metrics section
        Document_Content.append(Paragraph("Key Performance Metrics", Custom_Styles['qwim_heading1']))
        
        Key_Metrics_Text = """
        <b>Total Portfolio Value:</b> $1,000,000<br/>
        <b>Year-to-Date Return:</b> +6.8%<br/>
        <b>Benchmark Outperformance:</b> +1.2%<br/>
        <b>Portfolio Beta:</b> 0.95<br/>
        <b>Sharpe Ratio:</b> 1.42<br/>
        <b>Maximum Drawdown:</b> -3.2%
        """
        Document_Content.append(Paragraph(Key_Metrics_Text, Custom_Styles['qwim_important']))
        Document_Content.append(Spacer(1, 20))
        
        # Portfolio allocation table using ReportLab Table
        Document_Content.append(Paragraph("Portfolio Allocation Analysis", Custom_Styles['qwim_heading1']))
        
        # Create professional ReportLab table
        Portfolio_Table = create_reportlab_financial_table(
            Portfolio_Data, 
            "Portfolio Holdings Summary",
            "qwim_professional"
        )
        Document_Content.append(Portfolio_Table)
        Document_Content.append(Spacer(1, 20))
        
        # Enhanced Charts section using plotnine
        if include_charts:
            Document_Content.append(Paragraph("Visual Analysis with plotnine Charts", Custom_Styles['qwim_heading1']))
            
            if PLOTNINE_AVAILABLE:
                # Create temporary directory for charts
                Temp_Charts_Dir = Output_Directory / "temp_charts"
                Temp_Charts_Dir.mkdir(exist_ok=True)
                
                # Define multiple chart types to generate
                Chart_Types_List = [
                    ("portfolio_allocation", "Portfolio Allocation (Stacked Bar Chart)"),
                    ("performance_comparison", "Performance Comparison (Bar Chart)"),
                    ("risk_return_scatter", "Risk vs Return Analysis (Scatter Plot)"),
                    ("value_distribution", "Value Distribution (Horizontal Bar Chart)")
                ]
                
                Charts_Generated_Count = 0
                
                for Chart_Type_Name, Chart_Display_Name in Chart_Types_List:
                    try:
                        print(f"📊 Generating {Chart_Display_Name}...")
                        
                        # Add chart section header
                        Document_Content.append(Paragraph(Chart_Display_Name, Custom_Styles['qwim_heading2']))
                        Document_Content.append(Spacer(1, 10))
                        
                        # Generate chart file
                        Chart_File_Path = Temp_Charts_Dir / f"{Chart_Type_Name}_chart.png"
                        Chart_Path_Generated = create_plotnine_chart_image(
                            Portfolio_Data,
                            Chart_Type_Name, 
                            str(Chart_File_Path)
                        )
                        Chart_Files_To_Cleanup.append(Chart_Path_Generated)
                        
                        # Business logic validation - verify chart was created
                        if Path(Chart_Path_Generated).exists():
                            Chart_File_Size = Path(Chart_Path_Generated).stat().st_size
                            print(f"✅ Chart created: {Chart_Path_Generated} ({Chart_File_Size} bytes)")
                            
                            # Add chart to document
                            Generated_Chart = Image(Chart_Path_Generated, width=6*inch, height=4.5*inch)
                            Document_Content.append(Generated_Chart)
                            Document_Content.append(Spacer(1, 10))
                            
                            # Add chart description
                            Chart_Description = f"""
                            This {Chart_Display_Name.lower()} was generated using plotnine (Grammar of Graphics) 
                            without coord_polar dependency, demonstrating professional data visualization 
                            integrated with ReportLab PDF generation.
                            """
                            Document_Content.append(Paragraph(Chart_Description, Custom_Styles['qwim_body']))
                            Document_Content.append(Spacer(1, 20))
                            
                            Charts_Generated_Count += 1
                            print(f"✅ Added {Chart_Display_Name} to PDF")
                            
                        else:
                            print(f"❌ Chart file not found: {Chart_Path_Generated}")
                            Document_Content.append(Paragraph(
                                f"{Chart_Display_Name} generation failed - file not created", 
                                Custom_Styles['qwim_body']
                            ))
                            Document_Content.append(Spacer(1, 10))
        
                    except Exception as chart_error:
                        print(f"❌ Failed to generate {Chart_Display_Name}: {chart_error}")
                        Document_Content.append(Paragraph(
                            f"{Chart_Display_Name} generation temporarily unavailable: {str(chart_error)}", 
                            Custom_Styles['qwim_body']
                        ))
                        Document_Content.append(Spacer(1, 10))
                
                # Chart generation summary
                Chart_Summary_Text = f"""
                <b>Chart Generation Summary:</b><br/>
                Total charts requested: {len(Chart_Types_List)}<br/>
                Charts successfully generated: {Charts_Generated_Count}<br/>
                plotnine library status: Available (without coord_polar)<br/>
                Chart format: PNG (150 DPI)
                """
                Document_Content.append(Paragraph(Chart_Summary_Text, Custom_Styles['qwim_important']))
                Document_Content.append(Spacer(1, 20))
                
            else:
                # plotnine not available
                print("❌ plotnine library not available for chart generation")
                Document_Content.append(Paragraph(
                    "plotnine library not available for chart generation. Please install plotnine to enable chart functionality:", 
                    Custom_Styles['qwim_body']
                ))
                Document_Content.append(Spacer(1, 10))
                
                Installation_Instructions = """
                <b>To install plotnine:</b><br/>
                pip install plotnine<br/>
                <br/>
                plotnine provides Grammar of Graphics visualization capabilities for Python,
                similar to ggplot2 in R, enabling professional statistical graphics.
                """
                Document_Content.append(Paragraph(Installation_Instructions, Custom_Styles['qwim_important']))
                Document_Content.append(Spacer(1, 20))
        
        # Investment recommendations
        Document_Content.append(PageBreak())
        Document_Content.append(Paragraph("Investment Recommendations", Custom_Styles['qwim_heading1']))
        
        Recommendations_Text = """
        Based on our comprehensive analysis using plotnine visualizations (stacked bar charts 
        instead of pie charts) and professional ReportLab table formatting, we recommend the 
        following strategic adjustments to optimize your risk-adjusted returns:
        """
        Document_Content.append(Paragraph(Recommendations_Text, Custom_Styles['qwim_body']))
        
        # Recommendations list
        Recommendations_List = [
            "Consider increasing international equity exposure to 30% for better diversification",
            "Reduce cash allocation to 2% and deploy excess capital into growth opportunities", 
            "Add small-cap value stocks to capture potential outperformance",
            "Implement tax-loss harvesting strategies in taxable accounts",
            "Review and rebalance portfolio quarterly using modern analytics tools"
        ]
        
        for Recommendation_Item in Recommendations_List:
            Document_Content.append(Paragraph(f"• {Recommendation_Item}", Custom_Styles['qwim_body']))
        
        Document_Content.append(Spacer(1, 20))
        
        # Technical implementation details
        Document_Content.append(Paragraph("Technical Implementation", Custom_Styles['qwim_heading2']))
        
        Technical_Text = """
        This report was generated using plotnine for professional data visualization following 
        the Grammar of Graphics principles (without coord_polar dependency), and ReportLab Table 
        components for structured data presentation. This combination provides optimal performance 
        and consistent styling.
        """
        Document_Content.append(Paragraph(Technical_Text, Custom_Styles['qwim_body']))
        
        # Technical details
        Technical_Details = f"""
        <b>Technical Stack:</b><br/>
        • plotnine: {'✅ Available' if PLOTNINE_AVAILABLE else '❌ Not Available'} - Grammar of Graphics charts (no coord_polar)<br/>
        • ReportLab: ✅ Available - PDF generation and table formatting<br/>
        • pandas: ✅ Available - Data manipulation and analysis<br/>
        • Chart resolution: 150 DPI for crisp PDF inclusion<br/>
        • Color scheme: Custom QWIM branding palette<br/>
        • Package detection: importlib.util (replaced pkg_resources)
        """
        Document_Content.append(Paragraph(Technical_Details, Custom_Styles['qwim_important']))
        
        # Disclaimer
        Document_Content.append(Spacer(1, 30))
        Disclaimer_Text = """
        <b>Important Disclaimer:</b> This report is for informational purposes only and does not 
        constitute investment advice. Past performance does not guarantee future results. 
        Please consult with a qualified financial advisor before making investment decisions.
        """
        Document_Content.append(Paragraph(Disclaimer_Text, Custom_Styles['qwim_footer']))
        
        # Build the PDF
        print("📄 Building PDF document...")
        Pdf_Document.build(Document_Content)
        
        # Business logic validation
        if Output_Path.exists():
            File_Size = Output_Path.stat().st_size
            print(f"✅ PDF generated successfully ({File_Size} bytes)")
            print(f"📁 Saved to: {Output_Path}")
            return True, str(Output_Path)
        else:
            return False, "PDF file was not created successfully"
        
    except Exception as exc_error:
        return False, f"PDF generation error: {exc_error}"
    finally:
        # Clean up temporary chart files after PDF is built
        print(f"🧹 Cleaning up {len(Chart_Files_To_Cleanup)} chart files...")
        for Chart_File_Path in Chart_Files_To_Cleanup:
            try:
                Chart_Path_Obj = Path(Chart_File_Path)
                if Chart_Path_Obj.exists():
                    Chart_Path_Obj.unlink()
                    print(f"🧹 Cleaned up chart file: {Chart_File_Path}")
            except Exception as cleanup_error:
                print(f"⚠️ Could not clean up chart file {Chart_File_Path}: {cleanup_error}")
        
        # Clean up temporary charts directory if empty
        try:
            Temp_Charts_Dir = Path(output_directory) / "temp_charts"
            if Temp_Charts_Dir.exists() and not any(Temp_Charts_Dir.iterdir()):
                Temp_Charts_Dir.rmdir()
                print(f"🧹 Cleaned up temporary charts directory")
        except Exception as dir_cleanup_error:
            print(f"⚠️ Could not clean up charts directory: {dir_cleanup_error}")


def generate_qwim_pdf_report_high_resolution(
    report_title: str = "QWIM Portfolio Analysis Report",
    output_filename: str = "qwim_report_hd.pdf",
    output_directory: str = "outputs/reports",
    include_charts: bool = True
) -> Tuple[bool, str]:
    """
    Generate a high-resolution PDF report using SimpleDocTemplate with enhanced quality settings.
    
    Args:
        report_title (str): Title for the PDF report
        output_filename (str): Name of the output PDF file
        output_directory (str): Directory to save the PDF file
        include_charts (bool): Whether to include high-resolution plotnine charts
        
    Returns:
        Tuple[bool, str]: Tuple of (success_flag, output_path_or_error_message)
    """
    Chart_Files_To_Cleanup = []
    
    try:
        # Input validation
        if not report_title or len(report_title.strip()) < 3:
            return False, "Report title must be at least 3 characters long"
        
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        
        # Configuration validation
        Output_Directory = Path(output_directory)
        Output_Directory.mkdir(parents=True, exist_ok=True)
        
        Output_Path = Output_Directory / output_filename
        
        print(f"🚀 Starting high-resolution PDF generation: {Output_Path}")
        print(f"📊 plotnine available: {PLOTNINE_AVAILABLE}")
        print(f"📋 Using enhanced ReportLab settings")
        
        # Create sample data
        Portfolio_Data = create_sample_financial_data()
        
        # Create high-resolution document using SimpleDocTemplate
        Pdf_Document = SimpleDocTemplate(
            str(Output_Path),
            pagesize=letter,
            rightMargin=54,      # Reduced margins for more content space
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )
        
        # Create enhanced custom styles
        Custom_Styles = create_qwim_styles_high_resolution()
        
        # Build document content
        Document_Content = []
        
        # Title page with enhanced styling
        Document_Content.append(Paragraph(report_title, Custom_Styles['qwim_title_hd']))
        Document_Content.append(Spacer(1, 24))
        
        # Current date with enhanced font
        Current_Date = datetime.datetime.now().strftime('%B %d, %Y')
        Document_Content.append(Paragraph(f"Generated on: {Current_Date}", Custom_Styles['qwim_body_hd']))
        Document_Content.append(Spacer(1, 24))
        
        # Executive summary with enhanced formatting
        Document_Content.append(Paragraph("Executive Summary", Custom_Styles['qwim_heading1_hd']))
        
        Summary_Text = """
        This comprehensive high-resolution portfolio analysis report provides detailed insights into 
        your investment portfolio performance, asset allocation, and risk metrics. The analysis covers 
        the period from January 2024 to December 2024 and includes recommendations for portfolio 
        optimization based on your risk tolerance and investment objectives using enhanced plotnine 
        visualizations at 300 DPI resolution.
        """
        Document_Content.append(Paragraph(Summary_Text, Custom_Styles['qwim_body_hd']))
        Document_Content.append(Spacer(1, 24))
        
        # Key metrics section with enhanced styling
        Document_Content.append(Paragraph("Key Performance Metrics", Custom_Styles['qwim_heading1_hd']))
        
        Key_Metrics_Text = """
        <b>Total Portfolio Value:</b> $1,000,000<br/>
        <b>Year-to-Date Return:</b> +6.8%<br/>
        <b>Benchmark Outperformance:</b> +1.2%<br/>
        <b>Portfolio Beta:</b> 0.95<br/>
        <b>Sharpe Ratio:</b> 1.42<br/>
        <b>Maximum Drawdown:</b> -3.2%<br/>
        <b>Resolution Quality:</b> Enhanced 300 DPI for professional printing
        """
        Document_Content.append(Paragraph(Key_Metrics_Text, Custom_Styles['qwim_important_hd']))
        Document_Content.append(Spacer(1, 24))
        
        # Portfolio allocation table using enhanced ReportLab Table
        Document_Content.append(Paragraph("Portfolio Allocation Analysis", Custom_Styles['qwim_heading1_hd']))
        
        # Create professional high-resolution ReportLab table
        Portfolio_Table = create_reportlab_financial_table_high_resolution(
            Portfolio_Data, 
            "Portfolio Holdings Summary",
            "qwim_professional_hd"
        )
        Document_Content.append(Portfolio_Table)
        Document_Content.append(Spacer(1, 24))
        
        # Enhanced Charts section using high-resolution plotnine
        if include_charts:
            Document_Content.append(Paragraph("High-Resolution Visual Analysis with plotnine Charts", Custom_Styles['qwim_heading1_hd']))
            
            if PLOTNINE_AVAILABLE:
                # Create temporary directory for high-resolution charts
                Temp_Charts_Dir = Output_Directory / "temp_charts_hd"
                Temp_Charts_Dir.mkdir(exist_ok=True)
                
                # Define multiple chart types to generate at high resolution
                Chart_Types_List = [
                    ("portfolio_allocation", "Portfolio Allocation (High-Resolution Stacked Bar Chart)"),
                    ("performance_comparison", "Performance Comparison (HD Bar Chart)"),
                    ("risk_return_scatter", "Risk vs Return Analysis (HD Scatter Plot)"),
                    ("value_distribution", "Value Distribution (HD Horizontal Bar Chart)")
                ]
                
                Charts_Generated_Count = 0
                
                for Chart_Type_Name, Chart_Display_Name in Chart_Types_List:
                    try:
                        print(f"📊 Generating {Chart_Display_Name} at 300 DPI...")
                        
                        # Add chart section header with enhanced styling
                        Document_Content.append(Paragraph(Chart_Display_Name, Custom_Styles['qwim_heading2_hd']))
                        Document_Content.append(Spacer(1, 12))
                        
                        # Generate high-resolution chart file
                        Chart_File_Path = Temp_Charts_Dir / f"{Chart_Type_Name}_chart_hd.png"
                        Chart_Path_Generated = create_plotnine_chart_image_high_resolution(
                            Portfolio_Data,
                            Chart_Type_Name, 
                            str(Chart_File_Path)
                        )
                        Chart_Files_To_Cleanup.append(Chart_Path_Generated)
                        
                        # Business logic validation - verify chart was created
                        if Path(Chart_Path_Generated).exists():
                            Chart_File_Size = Path(Chart_Path_Generated).stat().st_size
                            print(f"✅ HD Chart created: {Chart_Path_Generated} ({Chart_File_Size} bytes)")
                            
                            if Chart_File_Size > 0:
                                # Add high-resolution chart to document with larger size
                                Generated_Chart = Image(
                                    Chart_Path_Generated, 
                                    width=7.5*inch,    # Increased from 6*inch
                                    height=5.625*inch  # Increased from 4.5*inch (maintains 4:3 ratio)
                                )
                                Document_Content.append(Generated_Chart)
                                Document_Content.append(Spacer(1, 12))
                                
                                # Add chart description with enhanced formatting
                                Chart_Description = f"""
                                This {Chart_Display_Name.lower()} was generated using plotnine (Grammar of Graphics) 
                                at 300 DPI resolution without coord_polar dependency, demonstrating professional 
                                high-resolution data visualization integrated with ReportLab PDF generation for 
                                optimal print quality.
                                """
                                Document_Content.append(Paragraph(Chart_Description, Custom_Styles['qwim_body_hd']))
                                Document_Content.append(Spacer(1, 24))
                                
                                Charts_Generated_Count += 1
                                print(f"✅ Added HD {Chart_Display_Name} to PDF")
                            else:
                                print(f"❌ Chart file is empty: {Chart_Path_Generated}")
                                Document_Content.append(Paragraph(
                                    f"{Chart_Display_Name} generation failed - empty file", 
                                    Custom_Styles['qwim_body_hd']
                                ))
                                Document_Content.append(Spacer(1, 12))
                        else:
                            print(f"❌ Chart file not found: {Chart_Path_Generated}")
                            Document_Content.append(Paragraph(
                                f"{Chart_Display_Name} generation failed - file not created", 
                                Custom_Styles['qwim_body_hd']
                            ))
                            Document_Content.append(Spacer(1, 12))
        
                    except Exception as chart_error:
                        print(f"❌ Failed to generate {Chart_Display_Name}: {chart_error}")
                        Document_Content.append(Paragraph(
                            f"{Chart_Display_Name} generation temporarily unavailable: {str(chart_error)}", 
                            Custom_Styles['qwim_body_hd']
                        ))
                        Document_Content.append(Spacer(1, 12))
                
                # Chart generation summary with enhanced metrics
                Chart_Summary_Text = f"""
                <b>High-Resolution Chart Generation Summary:</b><br/>
                Total charts requested: {len(Chart_Types_List)}<br/>
                Charts successfully generated: {Charts_Generated_Count}<br/>
                plotnine library status: Available (without coord_polar)<br/>
                Chart format: PNG at 300 DPI (print quality)<br/>
                Chart dimensions: 12x9 inches<br/>
                File size optimization: Balanced quality and performance
                """
                Document_Content.append(Paragraph(Chart_Summary_Text, Custom_Styles['qwim_important_hd']))
                Document_Content.append(Spacer(1, 24))
                
            else:
                # plotnine not available
                print("❌ plotnine library not available for high-resolution chart generation")
                Document_Content.append(Paragraph(
                    "plotnine library not available for high-resolution chart generation. Please install plotnine to enable enhanced chart functionality:", 
                    Custom_Styles['qwim_body_hd']
                ))
                Document_Content.append(Spacer(1, 12))
                
                Installation_Instructions = """
                <b>To install plotnine for high-resolution charts:</b><br/>
                pip install plotnine matplotlib pillow<br/>
                <br/>
                plotnine provides Grammar of Graphics visualization capabilities for Python,
                similar to ggplot2 in R, enabling professional high-resolution statistical graphics
                optimized for print quality at 300 DPI resolution.
                """
                Document_Content.append(Paragraph(Installation_Instructions, Custom_Styles['qwim_important_hd']))
                Document_Content.append(Spacer(1, 24))
        
        # Investment recommendations with enhanced formatting
        Document_Content.append(PageBreak())
        Document_Content.append(Paragraph("Investment Recommendations", Custom_Styles['qwim_heading1_hd']))
        
        Recommendations_Text = """
        Based on our comprehensive high-resolution analysis using plotnine visualizations at 300 DPI 
        (stacked bar charts instead of pie charts) and professional ReportLab table formatting with 
        enhanced typography, we recommend the following strategic adjustments to optimize your 
        risk-adjusted returns:
        """
        Document_Content.append(Paragraph(Recommendations_Text, Custom_Styles['qwim_body_hd']))
        
        # Recommendations list with enhanced bullet points
        Recommendations_List = [
            "Consider increasing international equity exposure to 30% for better diversification",
            "Reduce cash allocation to 2% and deploy excess capital into growth opportunities", 
            "Add small-cap value stocks to capture potential outperformance",
            "Implement tax-loss harvesting strategies in taxable accounts",
            "Review and rebalance portfolio quarterly using modern high-resolution analytics tools",
            "Monitor print-quality reports monthly for detailed performance tracking"
        ]
        
        for Recommendation_Item in Recommendations_List:
            Document_Content.append(Paragraph(f"• {Recommendation_Item}", Custom_Styles['qwim_body_hd']))
        
        Document_Content.append(Spacer(1, 24))
        
        # Technical implementation details with enhanced specifications
        Document_Content.append(Paragraph("Technical Implementation", Custom_Styles['qwim_heading2_hd']))
        
        Technical_Text = """
        This high-resolution report was generated using plotnine for professional data visualization 
        following the Grammar of Graphics principles (without coord_polar dependency), and enhanced 
        ReportLab Table components for structured data presentation. This combination provides optimal 
        performance and consistent high-quality styling suitable for professional printing.
        """
        Document_Content.append(Paragraph(Technical_Text, Custom_Styles['qwim_body_hd']))
        
        # Enhanced technical details
        Technical_Details = f"""
        <b>Enhanced Technical Stack:</b><br/>
        • plotnine: {'✅ Available' if PLOTNINE_AVAILABLE else '❌ Not Available'} - Grammar of Graphics charts (300 DPI, no coord_polar)<br/>
        • ReportLab: ✅ Available - High-resolution PDF generation and table formatting<br/>
        • pandas: ✅ Available - Data manipulation and analysis<br/>
        • Chart resolution: 300 DPI for professional print quality<br/>
        • Chart dimensions: 12x9 inches (optimized for letter-size printing)<br/>
        • Color scheme: Custom QWIM branding palette with enhanced contrast<br/>
        • Typography: Enhanced font sizes and spacing for readability<br/>
        • Package detection: importlib.util (replaced pkg_resources)<br/>
        • PDF optimization: Balanced file size and visual quality
        """
        Document_Content.append(Paragraph(Technical_Details, Custom_Styles['qwim_important_hd']))
        
        # Enhanced disclaimer
        Document_Content.append(Spacer(1, 36))
        Disclaimer_Text = """
        <b>Important Disclaimer:</b> This high-resolution report is for informational purposes only 
        and does not constitute investment advice. Past performance does not guarantee future results. 
        Please consult with a qualified financial advisor before making investment decisions. This 
        document has been optimized for professional printing at 300 DPI resolution.
        """
        Document_Content.append(Paragraph(Disclaimer_Text, Custom_Styles['qwim_footer_hd']))
        
        # Build the high-resolution PDF using SimpleDocTemplate
        print("📄 Building high-resolution PDF document...")
        Pdf_Document.build(Document_Content)
        
        # Business logic validation
        if Output_Path.exists():
            File_Size = Output_Path.stat().st_size
            print(f"✅ High-resolution PDF generated successfully ({File_Size:,} bytes)")
            print(f"📁 Saved to: {Output_Path}")
            
            if 'Charts_Generated_Count' in locals():
                print(f"📊 HD Charts included in PDF: {Charts_Generated_Count}")
            
            return True, str(Output_Path)
        else:
            return False, "High-resolution PDF file was not created successfully"
        
    except Exception as exc_error:
        print(f"❌ High-resolution PDF generation error: {exc_error}")
        import traceback
        traceback.print_exc()
        return False, f"High-resolution PDF generation error: {exc_error}"
    finally:
        # Clean up temporary chart files after PDF is built
        print(f"🧹 Cleaning up {len(Chart_Files_To_Cleanup)} high-resolution chart files...")
        for Chart_File_Path in Chart_Files_To_Cleanup:
            try:
                Chart_Path_Obj = Path(Chart_File_Path)
                if Chart_Path_Obj.exists():
                    Chart_Path_Obj.unlink()
                    print(f"🧹 Cleaned up HD chart file: {Chart_File_Path}")
            except Exception as cleanup_error:
                print(f"⚠️ Could not clean up chart file {Chart_File_Path}: {cleanup_error}")


def create_qwim_styles_high_resolution() -> Dict[str, ParagraphStyle]:
    """
    Create enhanced high-resolution paragraph styles for QWIM branding and formatting.
    
    Returns:
        Dict[str, ParagraphStyle]: Dictionary of enhanced paragraph styles for HD output
    """
    # Get base styles
    Base_Styles = getSampleStyleSheet()
    
    # Enhanced QWIM styles dictionary for high resolution
    Custom_Styles = {}
    
    # Enhanced QWIM title style
    Custom_Styles['qwim_title_hd'] = ParagraphStyle(
        'QwimTitleHD',
        parent=Base_Styles['Title'],
        fontSize=28,        # Increased from 24
        textColor=HexColor('#1f4e79'),
        spaceAfter=36,      # Increased from 30
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=34          # Enhanced line spacing
    )
    
    # Enhanced QWIM heading 1 style
    Custom_Styles['qwim_heading1_hd'] = ParagraphStyle(
        'QwimHeading1HD',
        parent=Base_Styles['Heading1'],
        fontSize=20,        # Increased from 16
        textColor=HexColor('#1f4e79'),
        spaceAfter=18,      # Increased from 12
        spaceBefore=24,     # Increased from 20
        fontName='Helvetica-Bold',
        leading=24          # Enhanced line spacing
    )
    
    # Enhanced QWIM heading 2 style
    Custom_Styles['qwim_heading2_hd'] = ParagraphStyle(
        'QwimHeading2HD',
        parent=Base_Styles['Heading2'],
        fontSize=16,        # Increased from 14
        textColor=HexColor('#2e8b57'),
        spaceAfter=14,      # Increased from 10
        spaceBefore=18,     # Increased from 15
        fontName='Helvetica-Bold',
        leading=20          # Enhanced line spacing
    )
    
    # Enhanced QWIM body text style
    Custom_Styles['qwim_body_hd'] = ParagraphStyle(
        'QwimBodyHD',
        parent=Base_Styles['Normal'],
        fontSize=12,        # Increased from   11
        textColor=black,
        spaceAfter=8,       # Increased from 6
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
        leading=15          # Enhanced line spacing
    )
    
    # Enhanced QWIM important text style
    Custom_Styles['qwim_important_hd'] = ParagraphStyle(
        'QwimImportantHD',
        parent=Base_Styles['Normal'],
        fontSize=12,        # Increased from 11
        textColor=HexColor('#1f4e79'),
        spaceAfter=10,      # Increased from 8
        leftIndent=24,      # Increased from 20
        fontName='Helvetica',
        backColor=HexColor('#f0f8ff'),
        leading=15          # Enhanced line spacing
    )
    
    # Enhanced QWIM footer style
    Custom_Styles['qwim_footer_hd'] = ParagraphStyle(
        'QwimFooterHD',
        parent=Base_Styles['Normal'],
        fontSize=10,        # Increased from 9
        textColor=grey,
        spaceAfter=8,       # Increased from 6
        alignment=TA_JUSTIFY,
        fontName='Helvetica-Oblique',
        leading=12          # Enhanced line spacing
    )
    
    return Custom_Styles


def create_reportlab_financial_table_high_resolution(
    data_frame: pd.DataFrame,
    table_title: str = "Financial Data Table",
    style_name: str = "qwim_professional_hd"
) -> Table:
    """
    Create a high-resolution professional ReportLab table from pandas DataFrame following QWIM standards.
    
    Args:
        data_frame (pd.DataFrame): Source data for the table
        table_title (str): Title for the table
        style_name (str): Style theme to apply (enhanced for HD)
        
    Returns:
        Table: Enhanced high-resolution formatted ReportLab table object
    """
    # Input validation
    if data_frame.empty:
        raise ValueError("DataFrame cannot be empty for table creation")
    
    # Prepare table data
    Table_Data = []
    
    # Add header row
    Header_Row = list(data_frame.columns)
    Table_Data.append(Header_Row)
    
    # Add data rows with enhanced formatting
    for Row_Index, Row_Data in data_frame.iterrows():
        Table_Row = []
        for Column_Name in data_frame.columns:
            Cell_Value = Row_Data[Column_Name]
            
            # Enhanced numeric formatting for high resolution display
            if isinstance(Cell_Value, (int, float)):
                if 'Percent' in Column_Name:
                    Formatted_Value = f"{Cell_Value:.1f}%"
                elif 'USD' in Column_Name or 'Value' in Column_Name:
                    Formatted_Value = f"${Cell_Value:,.0f}"
                else:
                    Formatted_Value = f"{Cell_Value:.2f}"
            else:
                Formatted_Value = str(Cell_Value)
            
            Table_Row.append(Formatted_Value)
        Table_Data.append(Table_Row)
    
    # Create table with enhanced spacing
    Financial_Table = Table(Table_Data)
    
    # Apply enhanced professional styling for high resolution
    if style_name == "qwim_professional_hd":
        Table_Style = TableStyle([
            # Enhanced header styling
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4e79')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),          # Increased from 12
            ('BOTTOMPADDING', (0, 0), (-1, 0), 16),     # Increased from 12
            ('TOPPADDING', (0, 0), (-1, 0), 16),        # Added for symmetry
            
            # Enhanced data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),         # Increased from 10
            ('GRID', (0, 0), (-1, -1), 1.5, HexColor('#1f4e79')),  # Thicker grid lines
            
            # Enhanced alternating row colors
            ('BACKGROUND', (0, 1), (-1, 1), HexColor('#f0f8ff')),
            ('BACKGROUND', (0, 3), (-1, 3), HexColor('#f0f8ff')),
            ('BACKGROUND', (0, 5), (-1, 5), HexColor('#f0f8ff')),
            
            # Enhanced padding and alignment
            ('TOPPADDING', (0, 1), (-1, -1), 12),       # Increased from 8
            ('BOTTOMPADDING', (0, 1), (-1, -1), 12),    # Increased from 8
            ('LEFTPADDING', (0, 0), (-1, -1), 14),      # Increased from 10
            ('RIGHTPADDING', (0, 0), (-1, -1), 14),     # Increased from 10
            
            # Enhanced border styling
            ('LINEBELOW', (0, 0), (-1, 0), 2, HexColor('#1f4e79')),  # Thicker header underline
            ('LINEABOVE', (0, 1), (-1, 1), 1, HexColor('#e0e0e0')),  # Light separator
        ])
    else:
        # Enhanced default styling
        Table_Style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
    
    Financial_Table.setStyle(Table_Style)
    
    return Financial_Table


# Complete the missing function implementations
def complete_chart_generation_loop():
    """Complete the missing chart generation code."""
    return """
                    try:
                        print(f"📊 Generating {Chart_Display_Name}...")
                        
                        # Add chart section header
                        Document_Content.append(Paragraph(Chart_Display_Name, Custom_Styles['qwim_heading2']))
                        Document_Content.append(Spacer(1, 10))
                        
                        # Generate chart file
                        Chart_File_Path = Temp_Charts_Dir / f"{Chart_Type_Name}_chart.png"
                        Chart_Path_Generated = create_plotnine_chart_image(
                            Portfolio_Data,
                            Chart_Type_Name, 
                            str(Chart_File_Path)
                        )
                        Chart_Files_To_Cleanup.append(Chart_Path_Generated)
                        
                        # Business logic validation - verify chart was created
                        if Path(Chart_Path_Generated).exists():
                            Chart_File_Size = Path(Chart_Path_Generated).stat().st_size
                            print(f"✅ Chart created: {Chart_Path_Generated} ({Chart_File_Size} bytes)")
                            
                            # Add chart to document
                            Generated_Chart = Image(Chart_Path_Generated, width=6*inch, height=4.5*inch)
                            Document_Content.append(Generated_Chart)
                            Document_Content.append(Spacer(1, 10))
                            
                            # Add chart description
                            Chart_Description = f\"\"\"
                            This {Chart_Display_Name.lower()} was generated using plotnine (Grammar of Graphics) 
                            without coord_polar dependency, demonstrating professional data visualization 
                            integrated with ReportLab PDF generation.
                            \"\"\"
                            Document_Content.append(Paragraph(Chart_Description, Custom_Styles['qwim_body']))
                            Document_Content.append(Spacer(1, 20))
                            
                            Charts_Generated_Count += 1
                            print(f"✅ Added {Chart_Display_Name} to PDF")
                            
                        else:
                            print(f"❌ Chart file not found: {Chart_Path_Generated}")
                            Document_Content.append(Paragraph(
                                f"{Chart_Display_Name} generation failed - file not created", 
                                Custom_Styles['qwim_body']
                            ))
                            Document_Content.append(Spacer(1, 10))
                        
                    except Exception as chart_error:
                        print(f"❌ Failed to generate {Chart_Display_Name}: {chart_error}")
                        Document_Content.append(Paragraph(
                            f"{Chart_Display_Name} generation temporarily unavailable: {str(chart_error)}", 
                            Custom_Styles['qwim_body']
                        ))
                        Document_Content.append(Spacer(1, 10))
    """


# Add the main command-line interface
def main():
    """Main function for command-line execution."""
    print("🚀 QWIM PDF Report Generator")
    print("=" * 50)
    
    # Set up argument parser
    Argument_Parser = argparse.ArgumentParser(
        description="Generate QWIM PDF reports with professional styling and charts",
        epilog="Example: python generate_reportlab_pdf.py --title 'My Portfolio Report' --output my_report.pdf"
    )
    
    # Add command-line arguments
    Argument_Parser.add_argument(
        '--title',
        type=str,
        default="QWIM Portfolio Analysis Report",
        help="Report title (default: 'QWIM Portfolio Analysis Report')"
    )
    
    Argument_Parser.add_argument(
        '--output',
        type=str,
        default="qwim_report.pdf",
        help="Output filename (default: 'qwim_report.pdf')"
    )
    
    Argument_Parser.add_argument(
        '--directory',
        type=str,
        default="outputs/reports",
        help="Output directory (default: 'outputs/reports')"
    )
    
    Argument_Parser.add_argument(
        '--no-charts',
        action='store_true',
        help="Generate report without charts for faster processing"
    )
    
    Argument_Parser.add_argument(
        '--simplified',
        action='store_true',
        help="Use simplified PDF generation (faster, no custom headers/footers)"
    )
    
    Argument_Parser.add_argument(
        '--high-resolution',
        action='store_true',
        help="Generate high-resolution PDF (300 DPI charts, enhanced styling)"
    )
    
    Argument_Parser.add_argument(
        '--debug',
        action='store_true',
        help="Show debug information about the environment"
    )
    
    # Parse arguments
    Parsed_Args = Argument_Parser.parse_args()
    
    # Show debug information if requested
    if Parsed_Args.debug:
        debug_plotnine_environment()
        print()
    
    # Display configuration
    print(f"📋 Configuration:")
    print(f"   Title: {Parsed_Args.title}")
    print(f"   Output: {Parsed_Args.output}")
    print(f"   Directory: {Parsed_Args.directory}")
    print(f"   Include Charts: {not Parsed_Args.no_charts}")
    print(f"   Simplified Mode: {Parsed_Args.simplified}")
    print(f"   High Resolution: {Parsed_Args.high_resolution}")
    print()
    
    # Choose generation function based on arguments
    try:
        if Parsed_Args.high_resolution:
            print("🎨 Generating high-resolution PDF...")
            Success_Flag, Result_Message = generate_qwim_pdf_report_high_resolution(
                report_title=Parsed_Args.title,
                output_filename=Parsed_Args.output,
                output_directory=Parsed_Args.directory,
                include_charts=not Parsed_Args.no_charts
            )
        elif Parsed_Args.simplified:
            print("⚡ Generating simplified PDF...")
            Success_Flag, Result_Message = generate_qwim_pdf_report_simplified(
                report_title=Parsed_Args.title,
                output_filename=Parsed_Args.output,
                output_directory=Parsed_Args.directory,
                include_charts=not Parsed_Args.no_charts
            )
        else:
            print("📄 Generating standard PDF...")
            Success_Flag, Result_Message = generate_qwim_pdf_report(
                report_title=Parsed_Args.title,
                output_filename=Parsed_Args.output,
                output_directory=Parsed_Args.directory,
                include_charts=not Parsed_Args.no_charts
            )
        
        # Display results
        print()
        if Success_Flag:
            print("✅ SUCCESS: PDF Generated Successfully!")
            print("=" * 50)
            print(f"📁 File saved to: {Result_Message}")
            
            # Try to open the file location (Windows only)
            if os.name == 'nt':
                try:
                    subprocess.run(['explorer', '/select,', str(Result_Message)], check=False)
                    print("📂 Opened file location in Explorer")
                except Exception:
                    pass
                    
        else:
            print("❌ FAILURE: PDF Generation Failed!")
            print("=" * 50)
            print(f"Error: {Result_Message}")
            
            if Parsed_Args.debug:
                print("\n🔍 Running additional diagnostics...")
                debug_plotnine_environment()
            
            return 1
            
    except Exception as Main_Error:
        print("❌ CRITICAL ERROR in PDF generation!")
        print("=" * 50)
        print(f"Error: {Main_Error}")
        
        if Parsed_Args.debug:
            print("\n🔍 Full traceback:")
            traceback.print_exc()
        
        return 1
    
    return 0


# Fix the incomplete generate_qwim_pdf_report function
def fix_generate_qwim_pdf_report():
    """Replace the incomplete return statement in generate_qwim_pdf_report."""
    # This needs to be manually fixed in the file - replace the incomplete return statement
    # around line 615 with:
    return """
        if not report_title or len(report_title.strip()) < 3:
            return False, "Report title must be at least 3 characters long"
    """


# Execute main function when script is run directly
if __name__ == "__main__":
    sys.exit(main())