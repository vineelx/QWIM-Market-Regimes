import typst
import json
import os
from pathlib import Path


def create_qwim_typst_report():
    """Generate PDF report from QWIM Typst template with comprehensive error handling.
    
    Compiles the report_QWIM.typ file located in src/reporting/typst-QWIM directory
    using the temp_refs.bib bibliography file. Includes input validation and defensive 
    programming practices. All files are handled with explicit paths and outputs are 
    saved to the outputs/reports/typst directory structure.
    
    Returns:
        bool: True if compilation successful, False otherwise
    """
    # Define explicit paths for source files in src/reporting/typst-QWIM directory
    typst_qwim_source_path = Path("src/reporting/typst-QWIM")
    report_qwim_typ_path = typst_qwim_source_path / "report_QWIM.typ"
    temp_refs_bib_path = typst_qwim_source_path / "sample_refs.bib"
    
    # Define explicit paths for output files in outputs/reports/typst directory
    output_base_path = Path("outputs/reports/typst")
    qwim_report_pdf_path = output_base_path / "QWIM_Portfolio_Analysis_Report.pdf"
    
    # Input validation - ensure output directory exists
    output_base_path.mkdir(parents=True, exist_ok=True)
    print(f"Created output directory: {output_base_path}")
    
    # Input validation - check if source files exist
    if not report_qwim_typ_path.exists():
        print(f"✗ Source file not found: {report_qwim_typ_path}")
        return False
    
    if not temp_refs_bib_path.exists():
        print(f"✗ Bibliography file not found: {temp_refs_bib_path}")
        return False
    
    print(f"Source Typst file found: {report_qwim_typ_path}")
    print(f"Bibliography file found: {temp_refs_bib_path}")
    
    try:
        # Compile report_QWIM.typ to PDF and save as QWIM_Portfolio_Analysis_Report.pdf
        typst.compile(str(report_qwim_typ_path), 
                     output=str(qwim_report_pdf_path))
        print(f"✓ QWIM PDF compilation successful: {qwim_report_pdf_path}")
        
        return True
        
    except FileNotFoundError as file_error:
        print(f"✗ File not found during compilation: {file_error}")
        return False
    except PermissionError as permission_error:
        print(f"✗ Permission denied during compilation: {permission_error}")
        return False
    except Exception as compilation_error:
        print(f"✗ QWIM compilation error: {compilation_error}")
        return False
    

def main():
    """Main execution function for QWIM report generation with comprehensive workflow.
    
    Orchestrates the complete QWIM report generation process including PDF compilation
    and metadata generation. Implements input validation and defensive programming
    practices throughout the workflow.
    """
    print("=" * 60)
    print("QWIM Portfolio Analysis Report Generation")
    print("=" * 60)
    
    # Execute QWIM report compilation
    compilation_success = create_qwim_typst_report()
    
    # Summary reporting
    print("\n" + "=" * 60)
    print("QWIM Report Generation Summary")
    print("=" * 60)
    
    if compilation_success:
        print("\n🎉 QWIM Portfolio Analysis Report generation completed successfully!")
        print(f"📄 Main report available at: outputs/reports/typst/QWIM_Portfolio_Analysis_Report.pdf")
    else:
        print("\n⚠️  QWIM Portfolio Analysis Report generation completed with errors.")


if __name__ == "__main__":
    main()