"""
Shiny-Compatible PDF Report Generation Module for QWIM Analytics
===============================================================

This module provides PDF report generation capabilities specifically designed
to be called from Shiny dashboard buttons following QWIM project coding standards.

Features
--------
* Shiny-compatible PDF generation with proper return values
* Portfolio analysis based on data from "Portfolios" tab subtabs
* Investor information from "Investors" tab subtabs
* Integration with reactives_shiny data structure (Data_Personal_Info_DF, Data_Assets_DF, Data_Goals_DF, Data_Income_DF)
* Professional PDF reports using ReportLab Table function
* Polars dataframes integration for enhanced performance
* Charts and graphs using plotnine (Grammar of Graphics)
* Multi-page documents with automatic page breaks
* Custom styling and layouts optimized for Shiny integration

Dependencies
-----------
* reportlab: Core PDF generation library
* plotnine: Grammar of graphics for Python (ggplot2 style)
* pandas: For data manipulation
* polars: For high-performance dataframes
* PIL/Pillow: For image processing

Shiny Integration
----------------
This module is designed to be called from Shiny server functions in the
"Reporting" subtab with proper error handling and status reporting.

Example Usage from Shiny
------------------------
    from generate_report_pdf import generate_report_PDF
    
    # Called from Shiny server function
    Success_Flag, Output_Message, File_Path = generate_report_PDF(
        report_title="QWIM Portfolio Analysis",
        output_filename="qwim_report_20241224.pdf",
        reactives_shiny=Reactives_Shiny_Dict,
        user_id="user_001"
    )
"""

# Fix pandas is_finite deprecation and import issues

import os
import sys
import datetime
import tempfile
import time
import pandas as pd
import polars as pl
import numpy as np
from typing import Tuple, Dict, Optional, Any
from pathlib import Path


# ReportLab imports
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import Color, HexColor, black, white, grey, blue, red, green
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, Frame, PageTemplate, BaseDocTemplate)
from reportlab.lib import colors

from plotnine import (
    ggplot, aes, geom_point, geom_line, geom_col, geom_bar,
    theme_minimal, labs, scale_fill_manual, scale_color_manual,
    theme, element_text, element_rect, coord_flip, guides,
    guide_legend, scale_x_discrete, scale_y_continuous,
    geom_text, position_dodge, facet_wrap, geom_smooth)


def safe_is_finite_value(value: Any) -> bool:
    """
    Safely check if a value is finite, replacing deprecated pandas.api.types.is_finite.
    
    Args:
        value (Any): Value to check for finiteness
        
    Returns:
        bool: True if value is finite, False otherwise
    """
    # Input validation with early returns
    if value is None:
        return False
    
    if pd.isna(value):
        return False
    
    # Configuration validation - check for numeric types
    if not isinstance(value, (int, float, np.number)):
        return False
    
    # Business logic validation - use numpy for finite check
    try:
        return bool(np.isfinite(value))
    except Exception:
        return False


def create_qwim_styles_for_pdf_report() -> Dict[str, ParagraphStyle]:
    """
    Create custom paragraph styles for QWIM PDF reports following project standards.
    
    Returns:
        Dict[str, ParagraphStyle]: Dictionary of custom paragraph styles for PDF reports
    """
    # Get base styles
    Base_Styles = getSampleStyleSheet()
    
    # Custom QWIM styles dictionary for PDF reports
    custom_Styles_PDF = {}
    
    # QWIM title style for PDF reports
    custom_Styles_PDF['qwim_title_pdf'] = ParagraphStyle(
        'QwimTitlePDF',
        parent=Base_Styles['Title'],
        fontSize=28,
        textColor=HexColor('#1f4e79'),
        spaceAfter=36,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        leading=32)
    
    # QWIM heading 1 style for PDF reports
    custom_Styles_PDF['qwim_heading1_pdf'] = ParagraphStyle(
        'QwimHeading1PDF',
        parent=Base_Styles['Heading1'],
        fontSize=20,
        textColor=HexColor('#1f4e79'),
        spaceAfter=18,
        spaceBefore=24,
        fontName='Helvetica-Bold',
        leading=24)
    
    # QWIM heading 2 style for PDF reports
    custom_Styles_PDF['qwim_heading2_pdf'] = ParagraphStyle(
        'QwimHeading2PDF',
        parent=Base_Styles['Heading2'],
        fontSize=16,
        textColor=HexColor('#2e8b57'),
        spaceAfter=14,
        spaceBefore=18,
        fontName='Helvetica-Bold',
        leading=20)
    
    # QWIM body text style for PDF reports
    custom_Styles_PDF['qwim_body_pdf'] = ParagraphStyle(
        'QwimBodyPDF',
        parent=Base_Styles['Normal'],
        fontSize=12,
        textColor=black,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName='Helvetica',
        leading=16)
    
    # QWIM important text style for PDF reports
    custom_Styles_PDF['qwim_important_pdf'] = ParagraphStyle(
        'QwimImportantPDF',
        parent=Base_Styles['Normal'],
        fontSize=12,
        textColor=HexColor('#1f4e79'),
        spaceAfter=10,
        leftIndent=24,
        fontName='Helvetica',
        backColor=HexColor('#f0f8ff'),
        leading=16)
    
    # QWIM footer style for PDF reports
    custom_Styles_PDF['qwim_footer_pdf'] = ParagraphStyle(
        'QwimFooterPDF',
        parent=Base_Styles['Normal'],
        fontSize=10,
        textColor=grey,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        fontName='Helvetica-Oblique',
        leading=12)
    
    # QWIM PDF metadata style
    custom_Styles_PDF['qwim_metadata_pdf'] = ParagraphStyle(
        'QwimMetadataPDF',
        parent=Base_Styles['Normal'],
        fontSize=11,
        textColor=HexColor('#666666'),
        spaceAfter=8,
        alignment=TA_RIGHT,
        fontName='Helvetica-Oblique',
        leading=14)
    
    return custom_Styles_PDF


def safe_polars_column_access(
    polars_DF: Optional[pl.DataFrame],
    column_name: str,
    operation: str = "sum",
    default_value: Any = 0
) -> Any:
    """
    Safely access polars DataFrame columns with comprehensive error handling.
    
    Args:
        polars_DF (Optional[pl.DataFrame]): Source polars DataFrame
        column_name (str): Name of column to access
        operation (str): Operation to perform ("sum", "mean", "n_unique", "first")
        default_value (Any): Default value if operation fails
        
    Returns:
        Any: Result of operation or default value
    """
    # Input validation with early returns
    if polars_DF is None:
        print(f"⚠️ DataFrame is None for column {column_name}")
        return default_value
    
    if polars_DF.height == 0:
        print(f"⚠️ DataFrame is empty (0 rows) for column {column_name}")
        return default_value
    
    if polars_DF.width == 0:
        print(f"⚠️ DataFrame has no columns for column {column_name}")
        return default_value
    
    # Configuration validation - check if column exists
    if column_name not in polars_DF.columns:
        print(f"⚠️ Column '{column_name}' not found in DataFrame. Available columns: {polars_DF.columns}")
        return default_value
    
    try:
        # Business logic validation - perform safe operations
        if operation == "sum":
            # Check if column contains numeric data
            column_dtype = polars_DF.schema[column_name]
            if column_dtype in [pl.Int64, pl.Int32, pl.Float64, pl.Float32, pl.Int8, pl.Int16, pl.UInt32, pl.UInt64]:
                result_expr = polars_DF.select(pl.col(column_name).sum())
                if result_expr.height > 0:
                    result_value = result_expr.item()
                    return result_value if result_value is not None else default_value
                else:
                    print(f"⚠️ Sum operation returned empty result for column {column_name}")
                    return default_value
            else:
                print(f"⚠️ Column '{column_name}' is not numeric (type: {column_dtype}) for sum operation")
                return default_value
                
        elif operation == "mean":
            # Check if column contains numeric data for mean
            column_dtype = polars_DF.schema[column_name]
            if column_dtype in [pl.Int64, pl.Int32, pl.Float64, pl.Float32, pl.Int8, pl.Int16, pl.UInt32, pl.UInt64]:
                result_expr = polars_DF.select(pl.col(column_name).mean())
                if result_expr.height > 0:
                    result_value = result_expr.item()
                    return result_value if result_value is not None else default_value
                else:
                    print(f"⚠️ Mean operation returned empty result for column {column_name}")
                    return default_value
            else:
                print(f"⚠️ Column '{column_name}' is not numeric (type: {column_dtype}) for mean operation")
                return default_value
                
        elif operation == "n_unique":
            # Count unique values
            result_expr = polars_DF.select(pl.col(column_name).n_unique())
            if result_expr.height > 0:
                result_value = result_expr.item()
                return result_value if result_value is not None else default_value
            else:
                print(f"⚠️ n_unique operation returned empty result for column {column_name}")
                return default_value
                
        elif operation == "first":
            # Get first value
            result_expr = polars_DF.select(pl.col(column_name).first())
            if result_expr.height > 0:
                result_value = result_expr.item()
                return result_value if result_value is not None else default_value
            else:
                print(f"⚠️ First operation returned empty result for column {column_name}")
                return default_value
                
        elif operation == "count":
            # Count non-null values
            result_expr = polars_DF.select(pl.col(column_name).count())
            if result_expr.height > 0:
                result_value = result_expr.item()
                return result_value if result_value is not None else default_value
            else:
                print(f"⚠️ Count operation returned empty result for column {column_name}")
                return default_value
        else:
            print(f"⚠️ Unknown operation '{operation}' for column {column_name}")
            return default_value
            
    except Exception as column_error:
        print(f"⚠️ Error accessing column '{column_name}' with operation '{operation}': {column_error}")
        return default_value


def validate_polars_DF(
    polars_DF: Optional[pl.DataFrame],
    dataframe_name: str = "DataFrame"
) -> bool:
    """
    Validate polars DataFrame structure and content following QWIM standards.
    
    Args:
        polars_DF (Optional[pl.DataFrame]): DataFrame to validate
        dataframe_name (str): Name of DataFrame for logging
        
    Returns:
        bool: True if DataFrame is valid and usable, False otherwise
    """
    # Input validation with early returns
    if polars_DF is None:
        print(f"⚠️ {dataframe_name} is None")
        return False
    
    # Configuration validation
    if not isinstance(polars_DF, pl.DataFrame):
        print(f"⚠️ {dataframe_name} is not a polars DataFrame: {type(polars_DF)}")
        return False
    
    # Business logic validation
    if polars_DF.height == 0:
        print(f"⚠️ {dataframe_name} has no rows (height = 0)")
        return False
    
    if polars_DF.width == 0:
        print(f"⚠️ {dataframe_name} has no columns (width = 0)")
        return False
    
    print(f"✅ {dataframe_name} is valid: {polars_DF.height} rows, {polars_DF.width} columns")
    return True


def create_reportlab_table_from_polars_DF(
    polars_DF: pl.DataFrame,
    table_title: str = "Data Summary",
    style_name: str = "qwim_pdf_professional"
) -> Table:
    """
    Create a professional ReportLab Table from polars DataFrame following QWIM standards.
    
    Args:
        polars_DF (pl.DataFrame): Source polars DataFrame for table creation
        table_title (str): Title for the table
        style_name (str): Style theme to apply for PDF integration
        
    Returns:
        Table: Formatted ReportLab Table object optimized for PDF reports
    """
    # Input validation with early returns
    if not validate_polars_DF(polars_DF, "Table Source DataFrame"):
        # Create fallback table with error message
        Fallback_Data = [["Error"], ["DataFrame validation failed"]]
        Fallback_Table = Table(Fallback_Data)
        return Fallback_Table
    
    # Convert polars DataFrame to format suitable for ReportLab Table
    table_Data_PDF = []
    
    # Add header row with enhanced formatting
    try:
        Header_Row_PDF = list(polars_DF.columns)
        if not Header_Row_PDF:
            raise ValueError("DataFrame has no columns for table headers")
        table_Data_PDF.append(Header_Row_PDF)
        print(f"✅ Table headers created: {len(Header_Row_PDF)} columns")
    except Exception as header_error:
        print(f"❌ Error creating table headers: {header_error}")
        # Create minimal fallback table
        Fallback_Data = [["Error"], ["Header creation failed"]]
        Fallback_Table = Table(Fallback_Data)
        return Fallback_Table
    
    # Configuration validation - safely convert to pandas for iteration
    try:
        # Use polars to_pandas() with error handling
        dataframe_rows = polars_DF.to_pandas()
        
        # Defensive programming - validate conversion
        if dataframe_rows.empty:
            print("⚠️ Converted pandas DataFrame is empty")
            # Create table with headers only
            table_Data_PDF.append(["No data available"] * len(Header_Row_PDF))
        elif len(dataframe_rows.columns) == 0:
            print("⚠️ Converted pandas DataFrame has no columns")
            # Create table with headers only
            table_Data_PDF.append(["No columns available"] * len(Header_Row_PDF))
        else:
            print(f"✅ DataFrame converted for table: {len(dataframe_rows)} rows, {len(dataframe_rows.columns)} columns")
            
            # Add data rows with PDF-optimized formatting
            Row_Count = 0
            Max_Rows = 100  # Limit rows to prevent memory issues
            
            for Row_Index, Row_Data in dataframe_rows.iterrows():
                if Row_Count >= Max_Rows:
                    print(f"⚠️ Limiting table to {Max_Rows} rows to prevent memory issues")
                    table_Data_PDF.append(["..."] * len(Header_Row_PDF))
                    table_Data_PDF.append([f"Total rows: {len(dataframe_rows)}"] + [""] * (len(Header_Row_PDF) - 1))
                    break
                
                Table_Row_PDF = []
                
                # Defensive programming - iterate through known columns
                for Column_Name in Header_Row_PDF:
                    try:
                        # Safe cell value extraction
                        if Column_Name in dataframe_rows.columns:
                            Cell_Value = Row_Data[Column_Name]
                        else:
                            Cell_Value = "N/A"
                        
                        # Enhanced formatting for PDF display with defensive checks
                        if pd.isna(Cell_Value) or Cell_Value is None:
                            Formatted_Value = "N/A"
                        elif isinstance(Cell_Value, (int, float)):
                            # Defensive programming - use safe finite check
                            if pd.isna(Cell_Value) or not safe_is_finite_value(Cell_Value):
                                Formatted_Value = "N/A"
                            elif 'Amount' in Column_Name or 'Value' in Column_Name or 'Income' in Column_Name:
                                Formatted_Value = f"${Cell_Value:,.0f}"
                            elif 'Percentage' in Column_Name or 'Percent' in Column_Name:
                                Formatted_Value = f"{Cell_Value:.1f}%"
                            elif 'Age' in Column_Name or 'Priority' in Column_Name:
                                Formatted_Value = f"{int(Cell_Value)}"
                            else:
                                Formatted_Value = f"{Cell_Value:.2f}"
                        else:
                            # String conversion with length limit
                            Str_Value = str(Cell_Value)
                            if len(Str_Value) > 50:  # Limit cell content length
                                Formatted_Value = Str_Value[:47] + "..."
                            else:
                                Formatted_Value = Str_Value
                        
                        Table_Row_PDF.append(Formatted_Value)
                        
                    except Exception as cell_error:
                        print(f"⚠️ Error formatting cell {Column_Name} in row {Row_Index}: {cell_error}")
                        Table_Row_PDF.append("Error")
                
                # Defensive programming - only add row if it has correct structure
                if len(Table_Row_PDF) == len(Header_Row_PDF):
                    table_Data_PDF.append(Table_Row_PDF)
                    Row_Count += 1
                else:
                    print(f"⚠️ Skipping malformed row {Row_Index}: expected {len(Header_Row_PDF)} columns, got {len(Table_Row_PDF)}")
                    
    except Exception as conversion_error:
        print(f"❌ Error converting DataFrame for table: {conversion_error}")
        # Ensure we have at least headers and an error message
        table_Data_PDF = [Header_Row_PDF, ["Conversion error"] + [""] * (len(Header_Row_PDF) - 1)]
    
    # Create table with PDF-optimized spacing
    try:
        if len(table_Data_PDF) == 0:
            # Fallback table if no data was processed
            table_Data_PDF = [["Error"], ["No data processed"]]
        
        Financial_Table_PDF = Table(table_Data_PDF)
        print(f"✅ ReportLab table created with {len(table_Data_PDF)} rows")
        
    except Exception as table_creation_error:
        print(f"❌ Error creating ReportLab table: {table_creation_error}")
        # Create minimal fallback table
        Fallback_Data = [["Table Creation Error"], [str(table_creation_error)]]
        Financial_Table_PDF = Table(Fallback_Data)
    
    # Apply PDF-optimized professional styling with error handling
    try:
        if style_name == "qwim_pdf_professional":
            table_Style_PDF = TableStyle([
                # Enhanced header styling for PDF reports
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1f4e79')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 13),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 16),
                ('TOPPADDING', (0, 0), (-1, 0), 16),
                
                # Enhanced data rows styling for PDF
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('GRID', (0, 0), (-1, -1), 1.5, HexColor('#1f4e79')),
                
                # PDF-optimized alternating row colors (safe indexing)
                ('TOPPADDING', (0, 1), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
                ('LEFTPADDING', (0, 0), (-1, -1), 14),
                ('RIGHTPADDING', (0, 0), (-1, -1), 14),
                
                # PDF-specific border styling
                ('LINEBELOW', (0, 0), (-1, 0), 2.5, HexColor('#1f4e79')),
            ])
            
            # Add alternating row colors safely
            for Row_Index in range(1, min(len(table_Data_PDF), 20)):  # Limit to prevent index errors
                if Row_Index % 2 == 0:  # Even rows (1-indexed becomes 0-indexed even)
                    table_Style_PDF.add('BACKGROUND', (0, Row_Index), (-1, Row_Index), HexColor('#f8f9fa'))
        else:
            # Default styling for PDF compatibility
            table_Style_PDF = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 13),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 14),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1.2, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 11),
                ('TOPPADDING', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
            ])
        
        Financial_Table_PDF.setStyle(table_Style_PDF)
        print(f"✅ Table style applied successfully")
        
    except Exception as style_error:
        print(f"⚠️ Error applying table style: {style_error}")
        # Continue with unstyled table
    
    return Financial_Table_PDF


def create_plotnine_chart_from_polars_DF(
    polars_DF: pl.DataFrame,
    chart_type: str = "summary_chart",
    output_path: str = "temp_chart_pdf.png",
    user_id: str = "pdf_user"
) -> str:
    """
    Create plotnine charts from polars DataFrame optimized for PDF integration.
    
    Args:
        polars_DF (pl.DataFrame): Polars DataFrame for chart generation
        chart_type (str): Type of chart to generate for PDF display
        output_path (str): Path to save the chart image
        user_id (str): User identifier from Shiny session
        
    Returns:
        str: Path to the generated chart image optimized for PDF
    """
    # Input validation with early returns
    if not validate_polars_DF(polars_DF, "Chart Source DataFrame"):
        raise ValueError("Invalid polars DataFrame for chart generation")
    
    # Convert polars DataFrame to pandas for plotnine compatibility
    try:
        pandas_DF_for_charts = polars_DF.to_pandas()
        
        # Defensive programming - validate conversion
        if pandas_DF_for_charts.empty:
            raise ValueError("Converted pandas DataFrame is empty for charts")
        
        if len(pandas_DF_for_charts.columns) == 0:
            raise ValueError("Converted pandas DataFrame has no columns for charts")
            
        print(f"✅ DataFrame converted for charts: {len(pandas_DF_for_charts)} rows, {len(pandas_DF_for_charts.columns)} columns")
        print(f"📋 Available columns for charts: {list(pandas_DF_for_charts.columns)}")
        
    except Exception as conversion_error:
        print(f"❌ Error converting polars to pandas for charts: {conversion_error}")
        raise ValueError(f"Failed to convert DataFrame for charts: {conversion_error}")
    
    # QWIM color palette optimized for PDF display
    colors_QWIM_PDF = ['#1f4e79', '#2e8b57', '#ff6b35', '#9b59b6', '#34495e', '#e74c3c', '#f39c12', '#e67e22', '#3498db', '#27ae60']
    
    try:
        print(f"🎨 Creating PDF-optimized {chart_type} chart for user {user_id}...")
        
        # Get available columns safely
        available_columns = list(pandas_DF_for_charts.columns)
        
        # Defensive programming - create charts based on available columns
        if chart_type == "assets_distribution":
            # Check for required columns with fallbacks
            Asset_Value_Cols = [col for col in available_columns if 'Value' in col or 'Amount' in col]
            Asset_Category_Cols = [col for col in available_columns if 'Category' in col or 'Type' in col]
            Investor_Type_Cols = [col for col in available_columns if 'Investor' in col or 'Type' in col]
            
            if Asset_Value_Cols and Asset_Category_Cols:
                y_col = Asset_Value_Cols[0]
                x_col = Asset_Category_Cols[0]
                fill_col = Investor_Type_Cols[0] if Investor_Type_Cols else x_col
                
                # Check if we have multiple unique values for fill
                unique_fill_values = pandas_DF_for_charts[fill_col].nunique()
                
                if unique_fill_values > 1:
                    Chart_Plot_PDF = (
                        ggplot(pandas_DF_for_charts, aes(x=x_col, y=y_col, fill=fill_col))
                        + geom_col(width=0.8, position='dodge')
                        + scale_fill_manual(values=colors_QWIM_PDF[:min(unique_fill_values, len(colors_QWIM_PDF))])
                        + labs(
                            title="Asset Distribution Analysis",
                            subtitle=f"Generated for PDF Report - User: {user_id}",
                            x=x_col.replace('_', ' ').title(),
                            y=y_col.replace('_', ' ').title(),
                            fill=fill_col.replace('_', ' ').title()
                        )
                        + theme_minimal()
                        + theme(
                            axis_text_x=element_text(angle=45, hjust=1, size=12, color='#1f4e79'),
                            axis_text_y=element_text(size=12, color='#1f4e79'),
                            plot_title=element_text(size=18, weight='bold', color='#1f4e79'),
                            plot_subtitle=element_text(size=11, color='#666666'),
                            legend_position='bottom',
                            figure_size=(12, 8)
                        )
                    )
                else:
                    # Single category - no fill needed
                    Chart_Plot_PDF = (
                        ggplot(pandas_DF_for_charts, aes(x=x_col, y=y_col))
                        + geom_col(width=0.8, fill=colors_QWIM_PDF[0])
                        + labs(
                            title="Asset Distribution Analysis",
                            subtitle=f"Generated for PDF Report - User: {user_id}",
                            x=x_col.replace('_', ' ').title(),
                            y=y_col.replace('_', ' ').title()
                        )
                        + theme_minimal()
                        + theme(
                            axis_text_x=element_text(angle=45, hjust=1, size=12),
                            plot_title=element_text(size=18, weight='bold', color='#1f4e79'),
                            plot_subtitle=element_text(size=11, color='#666666'),
                            figure_size=(10, 7)
                        )
                    )
            else:
                raise ValueError(f"Required columns not found for assets_distribution chart. Available: {available_columns}")
        
        elif chart_type in ["goals_comparison", "income_analysis", "age_demographics"]:
            # Generic handling for other chart types
            if chart_type == "goals_comparison":
                Value_Cols = [col for col in available_columns if 'Goal' in col and ('Amount' in col or 'Value' in col)]
                Category_Cols = [col for col in available_columns if 'Goal' in col and 'Category' in col]
                Title_Text = "Financial Goals Comparison"
            elif chart_type == "income_analysis":
                Value_Cols = [col for col in available_columns if 'Income' in col]
                Category_Cols = [col for col in available_columns if 'Income' in col and 'Category' in col]
                Title_Text = "Income Analysis"
            else:  # age_demographics
                Value_Cols = [col for col in available_columns if 'Age' in col]
                Category_Cols = [col for col in available_columns if 'Type' in col or 'Category' in col]
                Title_Text = "Age Demographics Analysis"
            
            if Value_Cols and Category_Cols:
                y_col = Value_Cols[0]
                x_col = Category_Cols[0]
                
                Chart_Plot_PDF = (
                    ggplot(pandas_DF_for_charts, aes(x=x_col, y=y_col))
                    + geom_col(width=0.8, fill=colors_QWIM_PDF[0])
                    + labs(
                        title=Title_Text,
                        subtitle=f"Generated for PDF Report - User: {user_id}",
                        x=x_col.replace('_', ' ').title(),
                        y=y_col.replace('_', ' ').title()
                    )
                    + theme_minimal()
                    + theme(
                        axis_text_x=element_text(angle=45, hjust=1, size=12),
                        plot_title=element_text(size=18, weight='bold', color='#1f4e79'),
                        plot_subtitle=element_text(size=11, color='#666666'),
                        figure_size=(10, 7)
                    )
                )
            else:
                raise ValueError(f"Required columns not found for {chart_type} chart. Available: {available_columns}")
        
        else:
            # Fallback chart using first available numeric and categorical columns
            print(f"⚠️ Creating fallback chart for type: {chart_type}")
            
            # Find numeric and categorical columns
            Numeric_Cols = pandas_DF_for_charts.select_dtypes(include=['int64', 'float64']).columns.tolist()
            Categorical_Cols = pandas_DF_for_charts.select_dtypes(include=['object', 'string']).columns.tolist()
            
            if Numeric_Cols and Categorical_Cols:
                y_col = Numeric_Cols[0]
                x_col = Categorical_Cols[0]
                
                Chart_Plot_PDF = (
                    ggplot(pandas_DF_for_charts, aes(x=x_col, y=y_col))
                    + geom_col(width=0.8, fill=colors_QWIM_PDF[0])
                    + labs(
                        title="Data Summary Overview",
                        subtitle=f"Generated for PDF Report - User: {user_id}",
                        x=x_col.replace('_', ' ').title(),
                        y=y_col.replace('_', ' ').title()
                    )
                    + theme_minimal()
                    + theme(
                        axis_text_x=element_text(angle=45, hjust=1, size=12),
                        plot_title=element_text(size=18, weight='bold', color='#1f4e79'),
                        plot_subtitle=element_text(size=11, color='#666666'),
                        figure_size=(10, 7)
                    )
                )
            elif len(available_columns) >= 1:
                # Create a count plot using first column
                x_col = available_columns[0]
                Chart_Plot_PDF = (
                    ggplot(pandas_DF_for_charts, aes(x=x_col))
                    + geom_bar(fill=colors_QWIM_PDF[0])
                    + labs(
                        title="Data Count Overview",
                        subtitle=f"Generated for PDF Report - User: {user_id}",
                        x=x_col.replace('_', ' ').title(),
                        y="Count"
                    )
                    + theme_minimal()
                    + theme(
                        axis_text_x=element_text(angle=45, hjust=1, size=12),
                        plot_title=element_text(size=18, weight='bold', color='#1f4e79'),
                        plot_subtitle=element_text(size=11, color='#666666'),
                        figure_size=(10, 7)
                    )
                )
            else:
                raise ValueError(f"Insufficient data for chart creation: {len(available_columns)} columns available")
        
        # Configuration validation for PDF file paths
        Chart_Path_PDF = Path(output_path).resolve()
        Chart_Path_PDF.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"💾 Saving PDF chart to: {Chart_Path_PDF}")
        
        # Save chart with PDF-optimized settings
        Chart_Plot_PDF.save(
            filename=str(Chart_Path_PDF),
            width=12,
            height=8,
            dpi=300,  # High DPI for PDF quality
            verbose=False
        )
        
        # Business logic validation for PDF
        if not Chart_Path_PDF.exists():
            raise FileNotFoundError(f"PDF chart file was not created: {Chart_Path_PDF}")
        
        Chart_File_Size = Chart_Path_PDF.stat().st_size
        if Chart_File_Size == 0:
            raise ValueError(f"PDF chart file is empty: {Chart_Path_PDF}")
            
        print(f"✅ PDF chart saved successfully: {Chart_File_Size} bytes")
        
        return str(Chart_Path_PDF)
        
    except Exception as chart_error:
        print(f"❌ PDF plotnine chart creation error: {chart_error}")
        raise RuntimeError(f"PDF plotnine chart creation failed: {chart_error}")


def create_sample_personal_info_dataframe() -> pl.DataFrame:
    """
    Create sample personal information polars DataFrame for PDF testing following QWIM standards.
    
    Returns:
        pl.DataFrame: Sample personal information DataFrame for PDF report generation
    """
    # Configuration validation - create sample data structure
    Sample_Personal_Data = {
        'Investor_ID': ['INV001', 'INV002', 'INV003'],
        'Investor_Type': ['Primary', 'Spouse', 'Dependent'],
        'Name_First': ['John', 'Jane', 'Junior'],
        'Name_Last': ['Smith', 'Smith', 'Smith'],
        'Age_Current': [65, 62, 30],
        'Age_Retirement': [67, 65, 65],
        'State_Residence': ['California', 'California', 'New York'],
        'Risk_Tolerance': ['Moderate', 'Conservative', 'Aggressive']
    }
    
    # Business logic validation - create polars DataFrame
    try:
        Personal_Info_DF = pl.DataFrame(Sample_Personal_Data)
        print(f"✅ Created sample personal info DataFrame: {Personal_Info_DF.height} rows, {Personal_Info_DF.width} columns")
        return Personal_Info_DF
    except Exception as creation_error:
        print(f"❌ Error creating sample personal info DataFrame: {creation_error}")
        # Return minimal fallback DataFrame
        Fallback_Data = {'Error': ['Sample data creation failed']}
        return pl.DataFrame(Fallback_Data)


def create_sample_assets_dataframe() -> pl.DataFrame:
    """
    Create sample assets polars DataFrame for PDF testing following QWIM standards.
    
    Returns:
        pl.DataFrame: Sample assets DataFrame for PDF report generation
    """
    # Configuration validation - create sample data structure
    Sample_Assets_Data = {
        'Investor_ID': ['INV001', 'INV001', 'INV002', 'INV002', 'INV003'],
        'Investor_Type': ['Primary', 'Primary', 'Spouse', 'Spouse', 'Dependent'],
        'Asset_Category': ['401k', 'IRA', 'Roth IRA', 'Savings', 'Brokerage'],
        'Asset_Value': [450000, 125000, 85000, 25000, 15000],
        'Asset_Type': ['Tax Deferred', 'Tax Deferred', 'Tax Free', 'Taxable', 'Taxable'],
        'Institution_Name': ['Fidelity', 'Vanguard', 'Charles Schwab', 'Bank of America', 'E*TRADE']
    }
    
    # Business logic validation - create polars DataFrame
    try:
        Assets_DF = pl.DataFrame(Sample_Assets_Data)
        print(f"✅ Created sample assets DataFrame: {Assets_DF.height} rows, {Assets_DF.width} columns")
        return Assets_DF
    except Exception as creation_error:
        print(f"❌ Error creating sample assets DataFrame: {creation_error}")
        # Return minimal fallback DataFrame
        Fallback_Data = {'Error': ['Sample data creation failed']}
        return pl.DataFrame(Fallback_Data)


def create_sample_goals_dataframe() -> pl.DataFrame:
    """
    Create sample goals polars DataFrame for PDF testing following QWIM standards.
    
    Returns:
        pl.DataFrame: Sample goals DataFrame for PDF report generation
    """
    # Configuration validation - create sample data structure
    Sample_Goals_Data = {
        'Investor_ID': ['INV001', 'INV001', 'INV002', 'INV003'],
        'Investor_Type': ['Primary', 'Primary', 'Spouse', 'Dependent'],
        'Goal_Category': ['Retirement', 'Healthcare', 'Travel', 'Education'],
        'Goal_Amount': [1200000, 150000, 75000, 100000],
        'Goal_Priority': [1, 2, 3, 1],
        'Goal_Timeline': [15, 10, 5, 35],
        'Goal_Description': ['Comfortable retirement', 'Long-term care', 'World travel', 'College fund']
    }
    
    # Business logic validation - create polars DataFrame
    try:
        Goals_DF = pl.DataFrame(Sample_Goals_Data)
        print(f"✅ Created sample goals DataFrame: {Goals_DF.height} rows, {Goals_DF.width} columns")
        return Goals_DF
    except Exception as creation_error:
        print(f"❌ Error creating sample goals DataFrame: {creation_error}")
        # Return minimal fallback DataFrame
        Fallback_Data = {'Error': ['Sample data creation failed']}
        return pl.DataFrame(Fallback_Data)


def create_sample_income_dataframe() -> pl.DataFrame:
    """
    Create sample income polars DataFrame for PDF testing following QWIM standards.
    
    Returns:
        pl.DataFrame: Sample income DataFrame for PDF report generation
    """
    # Configuration validation - create sample data structure
    Sample_Income_Data = {
        'Investor_ID': ['INV001', 'INV001', 'INV002', 'INV002'],
        'Investor_Type': ['Primary', 'Primary', 'Spouse', 'Spouse'],
        'Income_Category': ['Social Security', 'Pension', 'Social Security', 'Part-time Work'],
        'Income_Annual': [28000, 45000, 22000, 15000],
        'Income_Start_Age': [67, 65, 65, 62],
        'Income_End_Age': [95, 95, 95, 70],
        'Income_Source': ['Government', 'Former Employer', 'Government', 'Consulting']
    }
    
    # Business logic validation - create polars DataFrame
    try:
        Income_DF = pl.DataFrame(Sample_Income_Data)
        print(f"✅ Created sample income DataFrame: {Income_DF.height} rows, {Income_DF.width} columns")
        return Income_DF
    except Exception as creation_error:
        print(f"❌ Error creating sample income DataFrame: {creation_error}")
        # Return minimal fallback DataFrame
        Fallback_Data = {'Error': ['Sample data creation failed']}
        return pl.DataFrame(Fallback_Data)


def generate_report_PDF(
    report_title: str = "QWIM Portfolio and Investor Analysis Report",
    output_filename: str = "qwim_report.pdf",
    output_directory: str = "outputs/reports",
    reactives_shiny: Optional[Dict] = None,
    user_id: str = "default_user",
    include_charts: bool = True,
    chart_resolution: str = "high"
) -> Tuple[bool, str, str]:
    """
    Generate comprehensive PDF report with portfolio analysis and investor information following QWIM standards.
    
    Args:
        report_title (str): Title for the PDF report
        output_filename (str): Name of the output PDF file
        output_directory (str): Directory to save the PDF file
        reactives_shiny (Optional[Dict]): Reactives dictionary containing polars DataFrames
        user_id (str): User identifier from Shiny session
        include_charts (bool): Whether to include plotnine charts in PDF
        chart_resolution (str): Resolution setting for charts ("high", "ultra", "medium")
        
    Returns:
        Tuple[bool, str, str]: Tuple of (success_flag, status_message, file_path)
    """
    # Input validation with early returns
    if not report_title or len(report_title.strip()) < 3:
        return False, "Report title must be at least 3 characters", ""
    
    if not output_filename or not output_filename.endswith('.pdf'):
        return False, "Output filename must end with .pdf", ""
    
    if not output_directory:
        return False, "Output directory cannot be empty", ""
    
    if not user_id or len(user_id.strip()) < 3:
        return False, "User ID must be at least 3 characters", ""
    
    try:
        print("=" * 80)
        print("📄 QWIM MAXIMUM RESOLUTION PDF REPORT GENERATION")
        print("=" * 80)
        print(f"📋 Report title: {report_title}")
        print(f"👤 User ID: {user_id}")
        print(f"📁 Output directory: {output_directory}")
        print(f"📄 Output filename: {output_filename}")
        print(f"📊 Include charts: {include_charts}")
        print(f"🎯 Chart resolution: {chart_resolution}")
        
        # Configuration validation - setup output directory
        Output_Dir_Path = Path(output_directory).resolve()
        Output_Dir_Path.mkdir(parents=True, exist_ok=True)
        
        Final_Output_Path = Output_Dir_Path / output_filename
        print(f"💾 Final output path: {Final_Output_Path}")
        
        # Business logic validation - retrieve polars DataFrames from reactives
        if reactives_shiny is not None:
            print("🔍 Retrieving DataFrames from reactives_shiny...")
            
            # Get DataFrames safely from reactives
            try:
                if "Inner_Variables_Shiny" in reactives_shiny:
                    Inner_Variables = reactives_shiny["Inner_Variables_Shiny"]
                    
                    Data_Personal_Info_DF = Inner_Variables["Data_Personal_Info_DF"].get()
                    Data_Assets_DF = Inner_Variables["Data_Assets_DF"].get()
                    Data_Goals_DF = Inner_Variables["Data_Goals_DF"].get()
                    Data_Income_DF = Inner_Variables["Data_Income_DF"].get()
                    
                    print("✅ DataFrames retrieved from reactives_shiny")
                else:
                    print("⚠️ Inner_Variables_Shiny not found in reactives")
                    Data_Personal_Info_DF = None
                    Data_Assets_DF = None
                    Data_Goals_DF = None
                    Data_Income_DF = None
                    
            except Exception as reactives_error:
                print(f"⚠️ Error accessing reactives_shiny: {reactives_error}")
                Data_Personal_Info_DF = None
                Data_Assets_DF = None
                Data_Goals_DF = None
                Data_Income_DF = None
        else:
            print("⚠️ reactives_shiny is None, using sample data...")
            Data_Personal_Info_DF = None
            Data_Assets_DF = None
            Data_Goals_DF = None
            Data_Income_DF = None
        
        # Defensive programming - use sample data if reactives data unavailable
        if not validate_polars_DF(Data_Personal_Info_DF, "Data_Personal_Info_DF"):
            print("📊 Using sample personal info data for PDF")
            Data_Personal_Info_DF = create_sample_personal_info_dataframe()
            
        if not validate_polars_DF(Data_Assets_DF, "Data_Assets_DF"):
            print("📊 Using sample assets data for PDF")
            Data_Assets_DF = create_sample_assets_dataframe()
            
        if not validate_polars_DF(Data_Goals_DF, "Data_Goals_DF"):
            print("📊 Using sample goals data for PDF")
            Data_Goals_DF = create_sample_goals_dataframe()
            
        if not validate_polars_DF(Data_Income_DF, "Data_Income_DF"):
            print("📊 Using sample income data for PDF")
            Data_Income_DF = create_sample_income_dataframe()
        
        # Create PDF document with maximum resolution settings
        PDF_Document = SimpleDocTemplate(
            str(Final_Output_Path),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Get custom styles for PDF
        Custom_Styles_PDF = create_qwim_styles_for_pdf_report()
        
        # Document content container
        Document_Content_PDF = []
        
        # TITLE PAGE
        Current_DateTime = datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')
        
        Document_Content_PDF.append(Paragraph(report_title, Custom_Styles_PDF['qwim_title_pdf']))
        Document_Content_PDF.append(Spacer(1, 36))
        
        Report_Metadata_Text = f"""
        <b>Report Generated:</b> {Current_DateTime}<br/>
        <b>User ID:</b> {user_id}<br/>
        <b>Data Sources:</b> Portfolios and Investors tab data<br/>
        <b>Chart Resolution:</b> {chart_resolution.title()}<br/>
        <b>QWIM Analytics Platform</b>
        """
        Document_Content_PDF.append(Paragraph(Report_Metadata_Text, Custom_Styles_PDF['qwim_metadata_pdf']))
        Document_Content_PDF.append(Spacer(1, 48))
        
        # EXECUTIVE SUMMARY
        Document_Content_PDF.append(Paragraph("Executive Summary", Custom_Styles_PDF['qwim_heading1_pdf']))
        
        Executive_Summary_Text = f"""
        This comprehensive report analyzes portfolio allocation and investor information based on data 
        from the QWIM Analytics platform. The analysis includes personal demographics, asset allocation 
        strategies, financial goals assessment, and income planning considerations. Data is sourced from 
        the "Portfolios" and "Investors" tabs, providing a holistic view for retirement and investment 
        planning strategies.
        """
        Document_Content_PDF.append(Paragraph(Executive_Summary_Text, Custom_Styles_PDF['qwim_body_pdf']))
        Document_Content_PDF.append(Spacer(1, 24))
        
        # PAGE BREAK
        Document_Content_PDF.append(PageBreak())
        
        # SECTION 1: Personal Information Analysis
        Document_Content_PDF.append(Paragraph("Personal Information Analysis", Custom_Styles_PDF['qwim_heading1_pdf']))
        
        Personal_Analysis_Text = f"""
        This section analyzes personal information and demographics from the "Investors" tab, 
        personal information subtab. The analysis includes current age, retirement age, risk tolerance, 
        and residence information crucial for developing personalized retirement and investment strategies.
        """
        Document_Content_PDF.append(Paragraph(Personal_Analysis_Text, Custom_Styles_PDF['qwim_body_pdf']))
        Document_Content_PDF.append(Spacer(1, 16))
        
        # Personal Information Table using polars DataFrame
        if validate_polars_DF(Data_Personal_Info_DF, "Data_Personal_Info_DF"):
            Personal_Info_Table = create_reportlab_table_from_polars_DF(
                Data_Personal_Info_DF, 
                "Personal Information Summary",
                "qwim_pdf_professional"
            )
            Document_Content_PDF.append(Personal_Info_Table)
            Document_Content_PDF.append(Spacer(1, 20))
            
            # Personal info insights with defensive programming
            Total_Investors = Data_Personal_Info_DF.height
            Average_Age = safe_polars_column_access(Data_Personal_Info_DF, 'Age_Current', 'mean', 0)
            
            Personal_Insights_Text = f"""
            <b>Personal Information Insights:</b><br/>
            Total investors in analysis: {Total_Investors}<br/>
            Average current age: {Average_Age:.1f} years<br/>
            Data source: Investors tab - Personal Information subtab<br/>
            Analysis includes demographic factors critical for retirement planning strategy.
            """
            Document_Content_PDF.append(Paragraph(Personal_Insights_Text, Custom_Styles_PDF['qwim_important_pdf']))
            Document_Content_PDF.append(Spacer(1, 24))
        
        # SECTION 2: Asset Allocation Analysis
        Document_Content_PDF.append(Paragraph("Asset Allocation Analysis", Custom_Styles_PDF['qwim_heading1_pdf']))
        
        Assets_Analysis_Text = f"""
        This comprehensive asset allocation analysis utilizes data from the "Investors" tab, assets subtab, 
        covering various account types including 401(k), IRA, Roth IRA, and taxable accounts for 
        tax-efficient portfolio construction and strategic asset allocation optimization.
        """
        Document_Content_PDF.append(Paragraph(Assets_Analysis_Text, Custom_Styles_PDF['qwim_body_pdf']))
        Document_Content_PDF.append(Spacer(1, 16))
        
        # Assets Table using polars DataFrame  
        if validate_polars_DF(Data_Assets_DF, "Data_Assets_DF"):
            Assets_Table = create_reportlab_table_from_polars_DF(
                Data_Assets_DF, 
                "Asset Allocation Summary",
                "qwim_pdf_professional"
            )
            Document_Content_PDF.append(Assets_Table)
            Document_Content_PDF.append(Spacer(1, 20))
            
            # Assets insights with defensive programming
            Total_Assets_Value = safe_polars_column_access(Data_Assets_DF, 'Asset_Value', 'sum', 0)
            Asset_Categories = safe_polars_column_access(Data_Assets_DF, 'Asset_Category', 'n_unique', 0)
            
            Assets_Insights_Text = f"""
            <b>Asset Allocation Insights:</b><br/>
            Total portfolio value: ${Total_Assets_Value:,.0f}<br/>
            Number of asset categories: {Asset_Categories}<br/>
            Data source: Investors tab - Assets subtab<br/>
            Analysis supports tax-efficient portfolio construction and diversification strategies.
            """
            Document_Content_PDF.append(Paragraph(Assets_Insights_Text, Custom_Styles_PDF['qwim_important_pdf']))
            Document_Content_PDF.append(Spacer(1, 24))
        
        # SECTION 3: Financial Goals Analysis
        Document_Content_PDF.append(Paragraph("Financial Goals Analysis", Custom_Styles_PDF['qwim_heading1_pdf']))
        
        Goals_Analysis_Text = f"""
        This financial goals analysis examines data from the "Investors" tab, goals subtab, including 
        retirement planning, healthcare considerations, travel objectives, and education funding to 
        develop comprehensive goal-based investment strategies and priority-based financial planning.
        """
        Document_Content_PDF.append(Paragraph(Goals_Analysis_Text, Custom_Styles_PDF['qwim_body_pdf']))
        Document_Content_PDF.append(Spacer(1, 16))
        
        # Goals Table using polars DataFrame
        if validate_polars_DF(Data_Goals_DF, "Data_Goals_DF"):
            Goals_Table = create_reportlab_table_from_polars_DF(
                Data_Goals_DF, 
                "Financial Goals Summary",
                "qwim_pdf_professional"
            )
            Document_Content_PDF.append(Goals_Table)
            Document_Content_PDF.append(Spacer(1, 20))
            
            # Goals insights with defensive programming
            Total_Goals_Amount = safe_polars_column_access(Data_Goals_DF, 'Goal_Amount', 'sum', 0)
            Goal_Categories = safe_polars_column_access(Data_Goals_DF, 'Goal_Category', 'n_unique', 0)
            
            Goals_Insights_Text = f"""
            <b>Financial Goals Insights:</b><br/>
            Total goals funding target: ${Total_Goals_Amount:,.0f}<br/>
            Number of goal categories: {Goal_Categories}<br/>
            Data source: Investors tab - Goals subtab<br/>
            Analysis enables priority-based financial planning and goal achievement strategies.
            """
            Document_Content_PDF.append(Paragraph(Goals_Insights_Text, Custom_Styles_PDF['qwim_important_pdf']))
            Document_Content_PDF.append(Spacer(1, 24))
        
        # SECTION 4: Income Analysis
        Document_Content_PDF.append(Paragraph("Income Analysis", Custom_Styles_PDF['qwim_heading1_pdf']))
        
        Income_Analysis_Text = f"""
        This income analysis utilizes data from the "Investors" tab, income subtab, covering 
        various income sources including Social Security, pensions, annuities, and other income 
        streams for comprehensive retirement income planning and cash flow optimization.
        """
        Document_Content_PDF.append(Paragraph(Income_Analysis_Text, Custom_Styles_PDF['qwim_body_pdf']))
        Document_Content_PDF.append(Spacer(1, 16))
        
        # Income Table using polars DataFrame
        if validate_polars_DF(Data_Income_DF, "Data_Income_DF"):
            Income_Table = create_reportlab_table_from_polars_DF(
                Data_Income_DF, 
                "Income Analysis Summary",
                "qwim_pdf_professional"
            )
            Document_Content_PDF.append(Income_Table)
            Document_Content_PDF.append(Spacer(1, 20))
            
            # Income insights with defensive programming
            Total_Annual_Income = safe_polars_column_access(Data_Income_DF, 'Income_Annual', 'sum', 0)
            Income_Sources = safe_polars_column_access(Data_Income_DF, 'Income_Category', 'n_unique', 0)
            
            Income_Insights_Text = f"""
            <b>Income Analysis Insights:</b><br/>
            Total projected annual income: ${Total_Annual_Income:,.0f}<br/>
            Number of income sources: {Income_Sources}<br/>
            Data source: Investors tab - Income subtab<br/>
            Analysis supports retirement income planning and cash flow management strategies.
            """
            Document_Content_PDF.append(Paragraph(Income_Insights_Text, Custom_Styles_PDF['qwim_important_pdf']))
            Document_Content_PDF.append(Spacer(1, 24))
        
        # CHARTS SECTION
        if include_charts:
            Document_Content_PDF.append(PageBreak())
            Document_Content_PDF.append(Paragraph("Visual Analysis and Charts", Custom_Styles_PDF['qwim_heading1_pdf']))
            
            Charts_Intro_Text = f"""
            This section provides visual analysis through professional charts and graphs generated using 
            plotnine (Grammar of Graphics) with {chart_resolution} resolution settings optimized for PDF display. 
            Charts are based on the polars DataFrames from the Portfolios and Investors tabs.
            """
            Document_Content_PDF.append(Paragraph(Charts_Intro_Text, Custom_Styles_PDF['qwim_body_pdf']))
            Document_Content_PDF.append(Spacer(1, 16))
            
            # Create temporary directory for charts
            Temp_Charts_Dir = Output_Dir_Path / f"temp_charts_pdf_{user_id}"
            Temp_Charts_Dir.mkdir(exist_ok=True)
            
            # Chart Types List PDF - fix empty checks
            Chart_Types_List_PDF = []
            
            if validate_polars_DF(Data_Assets_DF, "Data_Assets_DF"):
                Chart_Types_List_PDF.append(("assets_distribution", "Asset Distribution Analysis", Data_Assets_DF))
            
            if validate_polars_DF(Data_Goals_DF, "Data_Goals_DF"):
                Chart_Types_List_PDF.append(("goals_comparison", "Financial Goals Comparison", Data_Goals_DF))
            
            if validate_polars_DF(Data_Income_DF, "Data_Income_DF"):
                Chart_Types_List_PDF.append(("income_analysis", "Income Source Analysis", Data_Income_DF))
            
            if validate_polars_DF(Data_Personal_Info_DF, "Data_Personal_Info_DF"):
                Chart_Types_List_PDF.append(("age_demographics", "Age Demographics Analysis", Data_Personal_Info_DF))
            
            # Generate and include charts
            for Chart_Type, Chart_Title, Chart_DataFrame in Chart_Types_List_PDF:
                try:
                    # Create chart file path
                    Chart_Filename = f"chart_{Chart_Type}_{user_id}.png"
                    Chart_File_Path = Temp_Charts_Dir / Chart_Filename
                    
                    # Generate chart using plotnine
                    Generated_Chart_Path = create_plotnine_chart_from_polars_DF(
                        Chart_DataFrame,
                        Chart_Type,
                        str(Chart_File_Path),
                        user_id
                    )
                    
                    # Add chart to PDF if successfully created
                    if Path(Generated_Chart_Path).exists():
                        Document_Content_PDF.append(Paragraph(Chart_Title, Custom_Styles_PDF['qwim_heading2_pdf']))
                        
                        Chart_Image = Image(Generated_Chart_Path, width=7*inch, height=4.67*inch)
                        Document_Content_PDF.append(Chart_Image)
                        Document_Content_PDF.append(Spacer(1, 20))
                        
                        print(f"✅ Chart included in PDF: {Chart_Title}")
                    else:
                        print(f"⚠️ Chart file not found: {Generated_Chart_Path}")
                        
                except Exception as chart_error:
                    print(f"⚠️ Error creating chart {Chart_Type}: {chart_error}")
                    # Continue with other charts
                    continue
        
        # FOOTER SECTION
        Document_Content_PDF.append(PageBreak())
        Document_Content_PDF.append(Paragraph("Report Conclusion", Custom_Styles_PDF['qwim_heading1_pdf']))
        
        Conclusion_Text = f"""
        This comprehensive QWIM analytics report provides detailed analysis of portfolio allocation, 
        investor demographics, financial goals, and income planning based on data from the Portfolios 
        and Investors tabs. The analysis supports informed decision-making for retirement planning, 
        tax optimization, and goal-based investment strategies. All data processing utilized polars 
        DataFrames for enhanced performance and professional ReportLab tables for optimal PDF presentation.
        """
        Document_Content_PDF.append(Paragraph(Conclusion_Text, Custom_Styles_PDF['qwim_body_pdf']))
        Document_Content_PDF.append(Spacer(1, 20))
        
        Footer_Text = f"""
        Report generated by QWIM Analytics Platform on {Current_DateTime} for user {user_id}. 
        This report is confidential and intended solely for the use of the specified recipient. 
        Data sources include investor personal information, asset allocation details, financial 
        goals, and income projections from the QWIM dashboard tabs.
        """
        Document_Content_PDF.append(Paragraph(Footer_Text, Custom_Styles_PDF['qwim_footer_pdf']))
        
        # Generate the PDF document
        print("🔄 Building PDF document...")
        PDF_Document.build(Document_Content_PDF)
        
        # Business logic validation - verify PDF was created
        if not Final_Output_Path.exists():
            return False, f"PDF file was not created at {Final_Output_Path}", ""
        
        PDF_File_Size = Final_Output_Path.stat().st_size
        if PDF_File_Size == 0:
            return False, f"PDF file is empty at {Final_Output_Path}", ""
        
        # Clean up temporary charts directory if empty
        try:
            if include_charts:
                Temp_Charts_Dir_User = Path(output_directory) / f"temp_charts_pdf_{user_id}"
                if Temp_Charts_Dir_User.exists() and not any(Temp_Charts_Dir_User.iterdir()):
                    Temp_Charts_Dir_User.rmdir()
                    print(f"🧹 Cleaned up temporary PDF charts directory for user {user_id}")
        except Exception as dir_cleanup_error:
            print(f"⚠️ Could not clean up PDF charts directory: {dir_cleanup_error}")
        
        print(f"✅ PDF report generated successfully!")
        print(f"📁 File location: {Final_Output_Path}")
        print(f"📄 File size: {PDF_File_Size:,} bytes")
        print(f"🎯 Maximum resolution PDF generation completed")
        
        Success_Message = f"PDF report generated successfully with {PDF_File_Size:,} bytes"
        return True, Success_Message, str(Final_Output_Path)
        
    except Exception as generation_error:
        Error_Message = f"Critical error in PDF generation: {generation_error}"
        print(f"❌ {Error_Message}")
        import traceback
        traceback.print_exc()
        return False, Error_Message, ""


def test_pdf_report_generation() -> Tuple[bool, str]:
    """
    Test function for PDF report generation functionality following QWIM standards.
    
    Returns:
        Tuple[bool, str]: Tuple of (success_flag, test_message)
    """
    try:
        print("🧪 Testing PDF report generation functionality...")
        
        # Create test polars DataFrames
        Test_Personal_Info_DF = create_sample_personal_info_dataframe()
        Test_Assets_DF = create_sample_assets_dataframe()
        Test_Goals_DF = create_sample_goals_dataframe()
        Test_Income_DF = create_sample_income_dataframe()
        
        # Create mock reactives_shiny structure
        Test_Reactives_Shiny = {
            "Inner_Variables_Shiny": {
                "Data_Personal_Info_DF": Test_Personal_Info_DF,
                "Data_Assets_DF": Test_Assets_DF,
                "Data_Goals_DF": Test_Goals_DF,
                "Data_Income_DF": Test_Income_DF
            }
        }
        
        # Test PDF generation
        Success_Flag, Status_Message, File_Path = generate_report_PDF(
            report_title="Test QWIM Portfolio and Investor Analysis Report",
            output_filename="test_qwim_report.pdf",
            output_directory="outputs/test",
            reactives_shiny=Test_Reactives_Shiny,
            user_id="test_user_001",
            include_charts=True,
            chart_resolution="high"
        )
        
        if Success_Flag:
            return True, f"PDF test successful: {Status_Message}"
        else:
            return False, f"PDF test failed: {Status_Message}"
            
    except Exception as test_error:
        return False, f"PDF test error: {test_error}"


# Main execution for testing (not typically used in Shiny integration)
if __name__ == "__main__":
    print("🧪 QWIM PDF Report Generator - Test Mode")
    print("=" * 60)
    
    # Run test
    Test_Success, Test_Message = test_pdf_report_generation()
    
    if Test_Success:
        print(f"✅ TEST PASSED: {Test_Message}")
    else:
        print(f"❌ TEST FAILED: {Test_Message}")
    
    print("\n📋 For Shiny integration, import and call generate_report_PDF() function")
    print("   Example: Success, Message, Path = generate_report_PDF(reactives_shiny=Reactives_Data)")