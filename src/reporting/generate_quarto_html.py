import subprocess
import time
import os
import shutil
import psutil
import gc
from pathlib import Path


def force_terminate_process_tree():
    """
    Force terminate all Quarto-related processes and their children on Windows.
    """
    if os.name == 'nt':  # Windows only
        try:
            Process_Names_To_Kill = [
                'quarto.exe',
                'node.exe',
                'deno.exe',

                'pandoc.exe'
            ]
            
            for Process_Name in Process_Names_To_Kill:
                try:
                    # Use psutil for more reliable process management
                    for Process_Info in psutil.process_iter(['pid', 'name', 'cmdline']):
                        try:
                            if Process_Info.info['name'].lower() == Process_Name.lower():
                                # Check if it's related to Quarto
                                Cmdline_Str = ' '.join(Process_Info.info['cmdline'] or [])
                                if 'quarto' in Cmdline_Str.lower() or 'jupyter' in Cmdline_Str.lower():
                                    Process_Obj = psutil.Process(Process_Info.info['pid'])
                                    Process_Obj.terminate()
                                    print(f"🔄 Terminated {Process_Name} process (PID: {Process_Info.info['pid']})")
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            continue
                except Exception as process_kill_error:
                    print(f"⚠️ Could not kill {Process_Name}: {process_kill_error}")
            
            # Wait for processes to terminate
            time.sleep(5)
            
            # Force kill any remaining processes using taskkill
            for Process_Name in Process_Names_To_Kill:
                try:
                    subprocess.run(
                        ['taskkill', '/F', '/IM', Process_Name, '/T'],
                        capture_output=True,
                        timeout=10
                    )
                except Exception:
                    pass
            
            print("🔄 Process termination completed")
                        
        except Exception as process_error:
            print(f"⚠️ Process management warning: {process_error}")


def diagnose_quarto_environment() -> tuple[bool, str]:
    """
    Comprehensive diagnostic of Quarto environment and dependencies.
    
    Returns:
        tuple[bool, str]: Tuple of (environment_valid, diagnostic_message)
    """
    Diagnostic_Results = []
    Environment_Valid = True
    
    try:
        # Check Quarto installation
        try:
            Quarto_Version_Result = subprocess.run(
                ['quarto', '--version'],
                capture_output=True,
                text=True,
                timeout=15
            )
            if Quarto_Version_Result.returncode == 0:
                Quarto_Version = Quarto_Version_Result.stdout.strip()
                Diagnostic_Results.append(f"✅ Quarto installed: {Quarto_Version}")
            else:
                Diagnostic_Results.append(f"❌ Quarto version check failed: {Quarto_Version_Result.stderr}")
                Environment_Valid = False
        except FileNotFoundError:
            Diagnostic_Results.append("❌ Quarto not found in PATH")
            Environment_Valid = False
        except Exception as quarto_error:
            Diagnostic_Results.append(f"❌ Quarto check error: {quarto_error}")
            Environment_Valid = False
        
        # Check Python installation and packages
        try:
            Python_Version = subprocess.run(
                ['python', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if Python_Version.returncode == 0:
                Diagnostic_Results.append(f"✅ Python: {Python_Version.stdout.strip()}")
            else:
                Diagnostic_Results.append(f"⚠️ Python version check issue: {Python_Version.stderr}")
        except Exception as python_error:
            Diagnostic_Results.append(f"⚠️ Python check error: {python_error}")
        
        # Check required Python packages
        Required_Packages = ['numpy', 'matplotlib']
        for Package_Name in Required_Packages:
            try:
                Package_Check = subprocess.run(
                    ['python', '-c', f'import {Package_Name}; print(f"{Package_Name} available")'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if Package_Check.returncode == 0:
                    Diagnostic_Results.append(f"✅ Package {Package_Name}: Available")
                else:
                    Diagnostic_Results.append(f"❌ Package {Package_Name}: Not available")
                    Environment_Valid = False
            except Exception as package_error:
                Diagnostic_Results.append(f"⚠️ Package {Package_Name} check error: {package_error}")
        
        # Check Jupyter availability
        try:
            Jupyter_Check = subprocess.run(
                ['python', '-c', 'import jupyter; print("Jupyter available")'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if Jupyter_Check.returncode == 0:
                Diagnostic_Results.append("✅ Jupyter: Available")
            else:
                Diagnostic_Results.append("⚠️ Jupyter: Not available (may affect code execution)")
        except Exception as jupyter_error:
            Diagnostic_Results.append(f"⚠️ Jupyter check error: {jupyter_error}")
        
        # Check file system permissions
        try:
            Test_Dir = Path("outputs/reports")
            Test_Dir.mkdir(parents=True, exist_ok=True)
            Test_File = Test_Dir / "test_permissions.txt"
            Test_File.write_text("Test file")
            Test_File.unlink()
            Diagnostic_Results.append("✅ File system: Write permissions OK")
        except Exception as fs_error:
            Diagnostic_Results.append(f"❌ File system: Write permission error - {fs_error}")
            Environment_Valid = False
        
        Diagnostic_Message = "\n".join(Diagnostic_Results)
        return Environment_Valid, Diagnostic_Message
        
    except Exception as diagnostic_error:
        return False, f"Diagnostic error: {diagnostic_error}"


def validate_qmd_file_content(
    qmd_file_path: Path
) -> tuple[bool, str]:
    """
    Validate the content of the Quarto file for common issues.
    
    Args:
        qmd_file_path (Path): Path to the .qmd file
        
    Returns:
        tuple[bool, str]: Tuple of (content_valid, validation_message)
    """
    try:
        # Input validation
        if not qmd_file_path.exists():
            return False, f"File does not exist: {qmd_file_path}"
        
        # Read file content
        try:
            File_Content = qmd_file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            try:
                File_Content = qmd_file_path.read_text(encoding='latin-1')
            except Exception as encoding_error:
                return False, f"Cannot read file due to encoding issues: {encoding_error}"
        
        Validation_Issues = []
        Content_Valid = True
        
        # Check YAML header
        if not File_Content.startswith('---'):
            Validation_Issues.append("❌ Missing YAML header (should start with ---)")
            Content_Valid = False
        else:
            Validation_Issues.append("✅ YAML header present")
        
        # Check for required YAML fields
        Required_Yaml_Fields = ['title:', 'format:']
        for Required_Field in Required_Yaml_Fields:
            if Required_Field in File_Content:
                Validation_Issues.append(f"✅ YAML field {Required_Field} present")
            else:
                Validation_Issues.append(f"⚠️ YAML field {Required_Field} missing")
        
        # Check Python code blocks
        if '```{python}' in File_Content:
            Validation_Issues.append("✅ Python code blocks found")
            
            # Check for common syntax issues
            Python_Code_Blocks = []
            Lines_List = File_Content.split('\n')
            In_Python_Block = False
            Current_Block = []
            
            for Line_Content in Lines_List:
                if Line_Content.strip().startswith('```{python}'):
                    In_Python_Block = True
                    Current_Block = []
                elif Line_Content.strip() == '```' and In_Python_Block:
                    In_Python_Block = False
                    Python_Code_Blocks.append('\n'.join(Current_Block))
                elif In_Python_Block:
                    Current_Block.append(Line_Content)
            
            # Basic syntax validation for Python blocks
            for Block_Index, Code_Block in enumerate(Python_Code_Blocks):
                try:
                    compile(Code_Block, f'<code_block_{Block_Index}>', 'exec')
                    Validation_Issues.append(f"✅ Python code block {Block_Index + 1}: Syntax OK")
                except SyntaxError as syntax_error:
                    Validation_Issues.append(f"❌ Python code block {Block_Index + 1}: Syntax error - {syntax_error}")
                    Content_Valid = False
        else:
            Validation_Issues.append("⚠️ No Python code blocks found")
        
        # Check file size
        File_Size = qmd_file_path.stat().st_size
        if File_Size > 0:
            Validation_Issues.append(f"✅ File size: {File_Size} bytes")
        else:
            Validation_Issues.append("❌ File is empty")
            Content_Valid = False
        
        Validation_Message = "\n".join(Validation_Issues)
        return Content_Valid, Validation_Message
        
    except Exception as validation_error:
        return False, f"Validation error: {validation_error}"


def generate_html_from_quarto_enhanced(
    qmd_file_path: str,
    output_directory: str = "outputs/reports"
) -> tuple[bool, str]:
    """
    Generate HTML output from Quarto file with comprehensive error reporting.
    
    Args:
        qmd_file_path (str): Path to the .qmd file
        output_directory (str): Directory for output files
        
    Returns:
        tuple[bool, str]: Tuple of (success_flag, result_message)
    """
    try:
        print("🔍 STARTING COMPREHENSIVE QUARTO DIAGNOSTICS")
        print("=" * 60)
        
        # Input validation
        Qmd_File_Path = Path(qmd_file_path)
        if not Qmd_File_Path.exists():
            return False, f"Quarto file not found: {qmd_file_path}"
        
        if not Qmd_File_Path.suffix == '.qmd':
            return False, f"File must have .qmd extension: {qmd_file_path}"
        
        # Configuration validation - ensure output directory exists
        Output_Directory = Path(output_directory)
        Output_Directory.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Environment diagnostics
        print("📋 Step 1: Environment Diagnostics")
        print("-" * 30)
        Environment_Valid, Environment_Message = diagnose_quarto_environment()
        print(Environment_Message)
        
        if not Environment_Valid:
            return False, f"Environment validation failed:\n{Environment_Message}"
        
        # Step 2: File content validation
        print("\n📋 Step 2: QMD File Content Validation")
        print("-" * 30)
        Content_Valid, Content_Message = validate_qmd_file_content(Qmd_File_Path)
        print(Content_Message)
        
        if not Content_Valid:
            return False, f"File content validation failed:\n{Content_Message}"
        
        # Step 3: Pre-cleanup
        print("\n📋 Step 3: Pre-Generation Cleanup")
        print("-" * 30)
        force_terminate_process_tree()
        
        # Step 4: Prepare Quarto command with detailed logging
        print("\n📋 Step 4: Quarto Command Preparation")
        print("-" * 30)
        
        Quarto_Command = [
            'quarto', 'render', str(Qmd_File_Path),
            '--to', 'html',
            '--output-dir', str(Output_Directory),
            '--log-level', 'info',  # Detailed logging
            '--execute-debug'       # Debug mode for better error reporting
        ]
        
        print(f"🔧 Command: {' '.join(Quarto_Command)}")
        
        # Set environment variables for better debugging
        Env_Variables = os.environ.copy()
        if os.name == 'nt':  # Windows
            Env_Variables['QUARTO_LOG_LEVEL'] = 'DEBUG'
            Env_Variables['QUARTO_PRINT_STACK'] = 'true'
            Env_Variables['PYTHONPATH'] = str(Qmd_File_Path.parent.parent.parent)
        
        # Step 5: Execute Quarto with comprehensive error capture
        print("\n📋 Step 5: Quarto Execution")
        print("-" * 30)
        
        try:
            Creation_Flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            
            Quarto_Result = subprocess.run(
                Quarto_Command,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                check=False,
                env=Env_Variables,
                cwd=Qmd_File_Path.parent,  # Run from file directory
                creationflags=Creation_Flags if os.name == 'nt' else None
            )
            
            print(f"📊 Return code: {Quarto_Result.returncode}")
            
            # Always show output for debugging
            if Quarto_Result.stdout:
                print("📝 STDOUT:")
                print("-" * 20)
                print(Quarto_Result.stdout)
                print("-" * 20)
                
            if Quarto_Result.stderr:
                print("⚠️ STDERR:")
                print("-" * 20)
                print(Quarto_Result.stderr)
                print("-" * 20)
            
        except subprocess.TimeoutExpired:
            print("⏰ Quarto process timed out")
            force_terminate_process_tree()
            return False, "Quarto process timed out after 5 minutes"
        except Exception as subprocess_error:
            return False, f"Subprocess error: {subprocess_error}"
        
        # Step 6: Post-execution cleanup
        print("\n📋 Step 6: Post-Execution Cleanup")
        print("-" * 30)
        force_terminate_process_tree()
        time.sleep(2)
        
        # Step 7: Results validation
        print("\n📋 Step 7: Results Validation")
        print("-" * 30)
        
        if Quarto_Result.returncode == 0:
            # Look for generated HTML file
            Expected_Html_File = Output_Directory / f"{Qmd_File_Path.stem}.html"
            
            if Expected_Html_File.exists():
                File_Size = Expected_Html_File.stat().st_size
                print(f"✅ HTML generated successfully ({File_Size} bytes)")
                print(f"📁 Output saved to: {Expected_Html_File}")
                return True, str(Expected_Html_File)
            else:
                # List all files in output directory for debugging
                Output_Files = list(Output_Directory.glob("*"))
                Files_List = [f.name for f in Output_Files]
                return False, f"HTML file not found at expected location: {Expected_Html_File}\nFiles in output directory: {Files_List}"
        else:
            # Comprehensive error reporting
            Error_Details = []
            Error_Details.append(f"Quarto command failed with return code {Quarto_Result.returncode}")
            
            if Quarto_Result.stderr:
                Error_Details.append(f"Error output: {Quarto_Result.stderr}")
            if Quarto_Result.stdout:
                Error_Details.append(f"Standard output: {Quarto_Result.stdout}")
            
            Error_Details.append(f"Command executed: {' '.join(Quarto_Command)}")
            Error_Details.append(f"Working directory: {Qmd_File_Path.parent}")
            Error_Details.append(f"Output directory: {Output_Directory}")
            
            return False, "\n".join(Error_Details)
            
    except Exception as exc_error:
        return False, f"Unexpected error: {exc_error}"
    finally:
        # Final cleanup
        force_terminate_process_tree()


# Execute the generation following project standards
if __name__ == "__main__":
    # Define file paths following project standards
    Qmd_File_Path = "src/reporting/Example_One.qmd"
    Output_Directory = "outputs/reports"
    
    print("=" * 60)
    print("🚀 STARTING ENHANCED QUARTO HTML GENERATION")
    print("=" * 60)
    
    Success_Flag, Result_Message = generate_html_from_quarto_enhanced(Qmd_File_Path, Output_Directory)
    
    if Success_Flag:
        print("=" * 60)
        print("✅ QUARTO HTML GENERATION SUCCESSFUL")
        print("=" * 60)
        print(f"📄 Generated file: {Result_Message}")
        print(f"🌐 Open the HTML file in your browser to view the matplotlib polar plot")
        
        # Try to open the file location
        if os.name == 'nt':  # Windows
            try:
                subprocess.run(['explorer', '/select,', str(Result_Message)], check=False)
            except Exception:
                pass
    else:
        print("=" * 60)
        print("❌ QUARTO HTML GENERATION FAILED")
        print("=" * 60)
        print("Error Details:")
        print(Result_Message)
        print("\n💡 Troubleshooting suggestions:")
        print("   1. Check that all required Python packages are installed")
        print("   2. Verify Quarto is properly installed and in PATH")
        print("   3. Check file permissions and antivirus interference")
        print("   4. Try running as Administrator if on Windows")