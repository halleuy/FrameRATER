import subprocess
import sys
import os
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(message):
    """Print a formatted header."""
    print(f"\n{BLUE}{'='*70}")
    print(f"{message}")
    print(f"{'='*70}{RESET}\n")

def print_step(step_num, total_steps, description):
    """Print step information."""
    print(f"{YELLOW}[Step {step_num}/{total_steps}] {description}{RESET}")

def run_script(script_name, step_num, total_steps):
    """Run a Python script and handle errors."""
    print_step(step_num, total_steps, f"Running {script_name}...")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"{GREEN}✅ {script_name} completed successfully{RESET}\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}❌ Error running {script_name}{RESET}")
        print(f"{RED}Exit code: {e.returncode}{RESET}\n")
        return False
    except FileNotFoundError:
        print(f"{RED}❌ Error: {script_name} not found{RESET}\n")
        return False

def check_prerequisites():
    """Check if required input files exist."""
    print_header("Checking Prerequisites")
    
    project_dir = Path(__file__).parent.parent
    
    required_files = [
        (project_dir / "00_data" / "raw", "PDF files"),
        (project_dir / "00_data" / "framework_mapping.csv", "Framework mapping"),
        (project_dir / "00_data" / "labels.csv", "Expert labels"),
        (project_dir / "02_freq-analysis" / "dimension_weights.csv", "Dimension weights"),
    ]
    
    all_exist = True
    for file_path, description in required_files:
        if file_path.exists():
            print(f"  {GREEN}✓{RESET} {description}: {file_path}")
        else:
            print(f"  {RED}✗{RESET} {description}: {file_path} NOT FOUND")
            all_exist = False
    
    return all_exist

def main():
    """Run the complete Stage 03 pipeline."""
    
    print_header("🚀 STAGE 03: ML-MODEL PIPELINE")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    print(f"Working directory: {script_dir}\n")
    
    # Check prerequisites
    if not check_prerequisites():
        print(f"\n{RED}❌ Missing required input files. Cannot proceed.{RESET}")
        print(f"\nPlease ensure:")
        print(f"  1. Stage 01 (preprocess) has been completed")
        print(f"  2. Stage 02 (freq-analysis) has been completed")
        print(f"  3. Expert labels exist in 00_data/labels.csv")
        sys.exit(1)
    
    # Define pipeline steps
    scripts = [
        ("main.py", "Generate NLP-based dimension scores"),
        ("calibrate.py", "Calibrate scores against expert labels"),
        ("calibrate_svr.py", "Apply SVR-based calibration"),
        ("composite_score_calculator.py", "Calculate final composite scores"),
    ]
    
    total_steps = len(scripts)
    
    print_header("Starting Pipeline Execution")
    
    # Run each script in sequence
    for i, (script_name, description) in enumerate(scripts, 1):
        if not run_script(script_name, i, total_steps):
            print(f"\n{RED}{'='*70}")
            print(f"❌ Pipeline failed at step {i}: {script_name}")
            print(f"{'='*70}{RESET}\n")
            sys.exit(1)
    
    # Success!
    print_header("✅ PIPELINE COMPLETED SUCCESSFULLY")
    
    # Show output files
    results_dir = script_dir / "results"
    if results_dir.exists():
        print("Generated output files:")
        output_files = sorted(results_dir.glob("*.csv")) + sorted(results_dir.glob("*.txt")) + sorted(results_dir.glob("*.json"))
        for f in output_files:
            print(f"  📄 {f.name}")
    
    print(f"\n{GREEN}Stage 03 ML-Model scoring complete!{RESET}")
    print(f"Results saved to: {results_dir}\n")

if __name__ == "__main__":
    main()
