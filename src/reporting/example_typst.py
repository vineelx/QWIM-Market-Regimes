import typst
import json
import os
from pathlib import Path


def create_sample_typst_file():
    """Create a sample hello.typ file for demonstration purposes.
    
    Creates a basic Typst document with sample content including typography,
    mathematical expressions, and queryable elements for testing purposes.
    The file is created in the src/reporting directory without external dependencies.
    """
    # Define the explicit path for the hello.typ file
    hello_typ_path = Path("src/reporting/hello.typ")
    
    # Ensure the directory exists
    hello_typ_path.parent.mkdir(parents=True, exist_ok=True)
    
    sample_content = """
#set page(paper: "a4")
#set text(font: "Times New Roman", size: 12pt)

= Hello World

This is a sample Typst document.

== Features
- Beautiful typography
- Mathematical expressions: $sum_(i=1)^n i = (n(n+1))/2$
- Code blocks
- And much more!

== Math notation
The Fibonacci sequence can be defined through its
recurrence relation $F_n = F_(n-1) + F_(n-2)$.

You can also do math on its own, centered paragraph:

$ F_n = round(1 / sqrt(5) phi.alt^n), quad
  phi.alt = (1 + sqrt(5)) / 2 $

== Formatting
This *bold text* is created using asterisks. _Italics_ are made using underlines.

- An unordered list
- with a few
- items uses hyphens 
- for markers

+ This numbered list 
+ uses instead
+ the plus sign
+ for each item

== Code blocks
Here's some example code:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

<note>This is a note for querying</note>
"""
    
    with open(hello_typ_path, "w", encoding="utf-8") as file_handle:
        file_handle.write(sample_content.strip())


def compile_typst_examples():
    """Demonstrate various Typst compilation methods with comprehensive error handling.
    
    Showcases different compilation formats including PDF, PNG, SVG, and demonstrates
    the Compiler class usage along with query functionality. Includes input validation
    and defensive programming practices. All files are handled in the src/reporting directory
    with outputs saved to the outputs/reports/typst directory structure.
    """
    # Define explicit paths for source file in src/reporting directory
    hello_typ_path = Path("src/reporting/hello.typ")
    
    # Define explicit paths for all output files in outputs/reports/typst directory
    output_base_path = Path("outputs/reports/typst")
    hello_pdf_path = output_base_path / "hello.pdf"
    hello_png_path = output_base_path / "hello.png"
    hello_from_bytes_pdf_path = output_base_path / "hello_from_bytes.pdf"
    hello_multipage_pattern = str(output_base_path / "hello{n}.png")
    
    # Input validation - ensure output directory exists
    output_base_path.mkdir(parents=True, exist_ok=True)
    print(f"Created output directory: {output_base_path}")
    
    # Input validation - always recreate the file to ensure clean content
    print("Creating sample hello.typ file...")
    create_sample_typst_file()
    
    # Validate file exists after creation
    if not hello_typ_path.exists():
        print("✗ Failed to create hello.typ file")
        return
    
    try:
        # Compile hello.typ to PDF and save as hello.pdf
        typst.compile(str(hello_typ_path), 
                     output=str(hello_pdf_path))
        print(f"✓ PDF compilation successful: {hello_pdf_path}")
        
        # Compile hello.typ to PNG and save as hello.png
        typst.compile(str(hello_typ_path), 
                     output=str(hello_png_path), 
                     format="png", 
                     ppi=144.0)
        print(f"✓ PNG compilation successful: {hello_png_path}")
        
        # Or pass hello.typ content as bytes
        with open(hello_typ_path, "rb") as file_handle:
            typst.compile(file_handle.read(), 
                         output=str(hello_from_bytes_pdf_path))
        print(f"✓ Compilation from bytes successful: {hello_from_bytes_pdf_path}")
        
        # Or return PDF content as bytes and save manually
        pdf_bytes = typst.compile(str(hello_typ_path))
        pdf_bytes_path = output_base_path / "hello_bytes_manual.pdf"
        with open(pdf_bytes_path, "wb") as pdf_file:
            pdf_file.write(pdf_bytes)
        print(f"✓ PDF bytes generated and saved: {pdf_bytes_path} (size: {len(pdf_bytes)} bytes)")
        
        # Also for svg and save manually
        svg_bytes = typst.compile(str(hello_typ_path), format="svg")
        svg_bytes_path = output_base_path / "hello_manual.svg"
        with open(svg_bytes_path, "wb") as svg_file:
            svg_file.write(svg_bytes)
        print(f"✓ SVG bytes generated and saved: {svg_bytes_path} (size: {len(svg_bytes)} bytes)")
        
        # For multi-page export (the template is the same as the typst cli)
        # Defensive programming - handle potential None return
        images = typst.compile(str(hello_typ_path), 
                              output=hello_multipage_pattern, 
                              format="png")
        if images is not None:
            print(f"✓ Multi-page export successful: {len(images)} images in {output_base_path}")
        else:
            print(f"✓ Multi-page export completed (single page document) in {output_base_path}")
        
        # Or use Compiler class to avoid reinitialization
        compiler = typst.Compiler(str(hello_typ_path))
        png_result = compiler.compile(format="png", ppi=144.0)
        compiler_png_path = output_base_path / "hello_compiler.png"
        with open(compiler_png_path, "wb") as png_file:
            png_file.write(png_result)
        print(f"✓ Compiler class usage successful: {compiler_png_path}")
        
        # Query something with proper error handling
        try:
            values = json.loads(typst.query(str(hello_typ_path), 
                                          "<note>", 
                                          field="value", 
                                          one=True))
            query_results_path = output_base_path / "query_results.json"
            with open(query_results_path, "w", encoding="utf-8") as query_file:
                json.dump(values, query_file, indent=2)
            print(f"✓ Query successful and saved: {query_results_path}")
        except json.JSONDecodeError as json_error:
            print(f"⚠ Query JSON decode failed: {json_error}")
        except Exception as query_error:
            print(f"⚠ Query failed: {query_error}")
            
    except FileNotFoundError as file_error:
        print(f"✗ File not found: {file_error}")
    except PermissionError as permission_error:
        print(f"✗ Permission denied: {permission_error}")
    except Exception as compilation_error:
        print(f"✗ Compilation error: {compilation_error}")


if __name__ == "__main__":
    compile_typst_examples()