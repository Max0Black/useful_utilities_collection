import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_step(title: str) -> None:
    print(f"\n==================================================")
    print(f">> {title}")
    print(f"==================================================")

def main() -> None:
    root_dir = Path(__file__).resolve().parent
    os.chdir(root_dir)

    print_step("Checking and updating dependencies...")
    # Determine the python executable to use (venv python if available)
    venv_python = root_dir / ".venv" / "Scripts" / "python.exe"
    if not venv_python.exists():
        venv_python = Path(sys.executable)
        print(f"[Warning] Virtual environment not found at .venv. Using system python: {venv_python}")
    else:
        print(f"[Info] Using virtual environment python: {venv_python}")

    # Ensure pip is up to date and requirements are installed
    try:
        print("Upgrading pip...")
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"])
        if (root_dir / "requirements.txt").exists():
            print("Installing requirements from requirements.txt...")
            subprocess.check_call([str(venv_python), "-m", "pip", "install", "-r", "requirements.txt"])
        print("Ensuring PyInstaller is installed...")
        subprocess.check_call([str(venv_python), "-m", "pip", "install", "pyinstaller"])
    except subprocess.CalledProcessError as e:
        print(f"[Error] Dependency installation failed: {e}")
        sys.exit(1)

    print_step("Running test suite...")
    tests_passed = True
    try:
        # Run python -m unittest discover tests
        # We use subprocess.run with check=False to inspect the return code
        result = subprocess.run([str(venv_python), "-m", "unittest", "discover", "tests"])
        if result.returncode != 0:
            tests_passed = False
    except Exception as e:
        print(f"[Error] Failed to execute test suite: {e}")
        tests_passed = False

    if not tests_passed:
        print("\n[Warning] One or more tests failed or crashed!")
        try:
            choice = input("Do you still want to build the executable? (y/N): ").strip().lower()
            if choice not in ("y", "yes"):
                print("[Info] Build aborted by user due to test failures.")
                sys.exit(1)
            print("[Info] Proceeding with build despite test failures...")
        except (EOFError, KeyboardInterrupt):
            print("\n[Info] Input interrupted. Build aborted due to test failures.")
            sys.exit(1)
    else:
        print("[Info] All tests passed successfully!")

    print_step("Cleaning old build files...")
    build_dir = root_dir / "build"
    dist_dir = root_dir / "dist"
    
    if build_dir.exists():
        print(f"Removing {build_dir}...")
        shutil.rmtree(build_dir, ignore_errors=True)
    if dist_dir.exists():
        print(f"Removing {dist_dir}...")
        shutil.rmtree(dist_dir, ignore_errors=True)

    print_step("Running PyInstaller to compile executable...")
    spec_file = root_dir / "UsefulUtilitiesCollection.spec"
    if not spec_file.exists():
        print("[Error] Spec file 'UsefulUtilitiesCollection.spec' not found!")
        sys.exit(1)

    try:
        # Run pyinstaller with the spec file using python -m PyInstaller
        print(f"Compiling with command: {venv_python} -m PyInstaller --clean -y {spec_file.name}")
        subprocess.check_call([str(venv_python), "-m", "PyInstaller", "--clean", "-y", spec_file.name])
        
        exe_path = dist_dir / "UsefulUtilitiesCollection.exe"
        if exe_path.exists():
            print_step("BUILD SUCCESSFUL!")
            print(f"Your standalone executable is ready at:")
            print(f"Location: {exe_path.resolve()}")
            print(f"Size: {exe_path.stat().st_size / (1024*1024):.2f} MB")
        else:
            print("[Error] PyInstaller completed, but the executable was not found.")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"[Error] PyInstaller build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
