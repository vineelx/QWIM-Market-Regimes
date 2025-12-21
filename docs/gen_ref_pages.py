"""Generate the code reference pages and navigation."""

from pathlib import Path
import mkdocs_gen_files
from datetime import datetime


def generate_reference_documentation():
    """
    Generate API reference documentation from Python source files.
    
    This function scans specific directories and files in the dashboard folder,
    creates markdown files for each Python module, and generates a navigation
    structure for MkDocs.
    
    Only processes:
    - main_App.py from dashboard folder
    - All files from modules_tab_portfolios subfolder
    - All files from utils_dashboard subfolder
    """
    # Define the base source directory
    src_dir = Path("src")
    dashboard_dir = src_dir / "dashboard"
    nav_lines = []
    
    # Generate current date for documentation
    current_date = datetime.now().strftime("%B %Y")
    
    # Validate source directory exists
    if not src_dir.exists():
        print(f"Warning: Source directory '{src_dir}' does not exist")
        return
    
    if not dashboard_dir.exists():
        print(f"Warning: Dashboard directory '{dashboard_dir}' does not exist")
        return
    
    print(f"Scanning dashboard directory: {dashboard_dir}")
    print(f"Documentation generation date: {current_date}")
    
    # Define specific files and folders to include
    Target_Files = ["main_App.py"]
    Target_Folders = ["modules_tab_portfolios", "modules_tab_investors", "utils_dashboard"]
    
    # Process main_App.py file
    main_app_file = dashboard_dir / "main_App.py"
    if main_app_file.exists():
        _process_python_file(
            path=main_app_file,
            src_dir=src_dir,
            nav_lines=nav_lines
        )
    else:
        print(f"Warning: main_App.py not found in {dashboard_dir}")
    
    # Process files in target subfolders
    for folder_name in Target_Folders:
        folder_path = dashboard_dir / folder_name
        if folder_path.exists() and folder_path.is_dir():
            print(f"Processing folder: {folder_path}")
            
            # Walk through the subfolder
            for file_path in sorted(folder_path.rglob("*.py")):
                # Skip __pycache__ and other non-source files
                if "__pycache__" in str(file_path) or file_path.name.startswith("_"):
                    continue
                
                _process_python_file(
                    path=file_path,
                    src_dir=src_dir,
                    nav_lines=nav_lines
                )
        else:
            print(f"Warning: Folder '{folder_name}' not found in {dashboard_dir}")
    
    # Write navigation files only if we have content
    if nav_lines:
        _create_navigation_files(nav_lines=nav_lines)
        
        print(f"Generated reference documentation with {len(nav_lines)} entries")
        print("Files created:")
        print("  - reference/index.md")
        print("  - reference/SUMMARY.md")
        print(f"  - {len(nav_lines)} module documentation files")
    else:
        print("No Python files found to document")


def _process_python_file(
    path: Path,
    src_dir: Path,
    nav_lines: list
):
    """
    Process a single Python file for documentation generation.
    
    Args:
        path: Path to the Python file to process
        src_dir: Base source directory path
        nav_lines: List to append navigation entries to
    """
    print(f"Processing file: {path}")
    
    # Create module path
    module_path = path.relative_to(src_dir).with_suffix("")
    doc_path = path.relative_to(src_dir).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)
    
    # Convert path to module name
    parts = tuple(module_path.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        return
    
    # Skip if no valid parts remain
    if not parts:
        return
    
    # Create navigation entry in proper Markdown list format
    display_name = parts[-1].replace("_", " ").title()
    nav_entry = f"* [{display_name}]({doc_path})"
    nav_lines.append(nav_entry)
    print(f"Added nav entry: {nav_entry}")
    
    # Generate documentation content with explicit no-date frontmatter
    with mkdocs_gen_files.open(full_doc_path, "w") as file_descriptor:
        identifier = ".".join(parts)
        # Add frontmatter to explicitly disable date plugins
        file_descriptor.write("---\n")
        file_descriptor.write("hide:\n")
        file_descriptor.write("  - footer\n")
        file_descriptor.write("---\n\n")
        file_descriptor.write(f"# {identifier}\n\n")
        file_descriptor.write(f"::: {identifier}\n\n")
        print(f"Generated documentation for: {identifier}")
    
    # Set edit path
    mkdocs_gen_files.set_edit_path(full_doc_path, path)


def _create_navigation_files(nav_lines: list):
    """
    Create navigation files for MkDocs.
    
    Args:
        nav_lines: List of navigation entries to include
    """
    # Create main reference index without date metadata
    with mkdocs_gen_files.open("reference/index.md", "w") as nav_file:
        # Add frontmatter to explicitly disable date plugins
        nav_file.write("---\n")
        nav_file.write("hide:\n")
        nav_file.write("  - footer\n")
        nav_file.write("---\n\n")
        nav_file.write("# API Reference\n\n")
        nav_file.write("This section contains the complete API documentation for the QWIM Dashboard.\n\n")
        nav_file.write("## Dashboard Components\n\n")
        nav_file.write("The documentation covers the following components:\n\n")
        nav_file.write("- **Main Application**: Core dashboard entry point\n")
        nav_file.write("- **Portfolio Modules**: Portfolio analysis and management functionality\n")
        nav_file.write("- **Dashboard Utilities**: Common utilities and helper functions\n\n")
        nav_file.write("## Available Modules\n\n")
        for line in nav_lines:
            nav_file.write(f"{line}\n")
    
    # Create SUMMARY.md for literate-nav in proper format
    with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as summary_file:
        summary_file.write("# Reference\n\n")
        
        # Group navigation entries by module type
        Main_App_Entries = []
        Portfolio_Entries = []
        Utils_Entries = []
        
        for entry in nav_lines:
            if "main_App" in entry:
                Main_App_Entries.append(entry)
            elif "modules_tab_portfolios" in entry:
                Portfolio_Entries.append(entry)
            elif "utils_dashboard" in entry:
                Utils_Entries.append(entry)
        
        # Write organized navigation
        if Main_App_Entries:
            summary_file.write("## Main Application\n\n")
            for entry in Main_App_Entries:
                summary_file.write(f"{entry}\n")
            summary_file.write("\n")
        
        if Portfolio_Entries:
            summary_file.write("## Portfolio Modules\n\n")
            for entry in Portfolio_Entries:
                summary_file.write(f"{entry}\n")
            summary_file.write("\n")
        
        if Utils_Entries:
            summary_file.write("## Dashboard Utilities\n\n")
            for entry in Utils_Entries:
                summary_file.write(f"{entry}\n")


# Execute the documentation generation
generate_reference_documentation()