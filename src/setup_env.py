import os
import subprocess
import sys
import shutil

def create_virtual_env(env_name="venv"):
    """
    Creates a virtual environment and installs libraries from requirements.txt.
    Handles existing virtual environments.
    """
    # Check if the environment folder already exists
    if os.path.exists(env_name):
        print(f"Virtual environment '{env_name}' already exists.")
        action = input("Do you want to (R)Reuse, (D)Delete and recreate, or (E)Exit? ").strip().lower()

        if action == "r":
            print(f"Reusing existing virtual environment '{env_name}'.")
        elif action == "d":
            print(f"Deleting and recreating virtual environment '{env_name}'...")
            shutil.rmtree(env_name)
            subprocess.run([sys.executable, "-m", "venv", env_name], check=True)
            print(f"Virtual environment '{env_name}' recreated successfully.")
        elif action == "e":
            print("Exiting without changes.")
            return
        else:
            print("Invalid option. Exiting.")
            return
    else:
        # Create virtual environment
        print(f"Creating virtual environment: {env_name}")
        subprocess.run([sys.executable, "-m", "venv", env_name], check=True)
        print(f"Virtual environment '{env_name}' created successfully.")

    # Install requirements
    requirements_file = "requirements.txt"
    pip_executable = os.path.join(env_name, "Scripts", "pip")
    if os.path.exists(requirements_file):
        print("Installing libraries from requirements.txt...")
        subprocess.run([pip_executable, "install", "-r", requirements_file], check=True)
        print("Libraries installed successfully.")
    else:
        print(f"No {requirements_file} found. Skipping library installation.")

if __name__ == "__main__":
    create_virtual_env()
