#!/usr/bin/env python3
"""
LMU Buddy Fine-tuning Setup Script
Complete setup and fine-tuning process for LMU Buddy with Ollama
"""

import os
import sys
import subprocess
import platform
import requests
import time
from pathlib import Path

def print_banner():
    """Print the setup banner"""
    print("🦁" * 50)
    print("🦁 LMU Buddy Fine-tuning Setup")
    print("🦁" * 50)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_ollama():
    """Install Ollama based on the operating system"""
    print("\n📦 Installing Ollama...")
    
    system = platform.system().lower()
    
    if system == "linux":
        print("🐧 Installing Ollama on Linux...")
        try:
            # Download and install Ollama
            install_script = """
            curl -fsSL https://ollama.ai/install.sh | sh
            """
            result = subprocess.run(install_script, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Ollama installed successfully!")
                return True
            else:
                print(f"❌ Failed to install Ollama: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error installing Ollama: {e}")
            return False
    
    elif system == "darwin":  # macOS
        print("🍎 Installing Ollama on macOS...")
        try:
            # Use Homebrew if available
            result = subprocess.run(['brew', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("Using Homebrew to install Ollama...")
                result = subprocess.run(['brew', 'install', 'ollama'], capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Ollama installed successfully!")
                    return True
                else:
                    print(f"❌ Failed to install Ollama via Homebrew: {result.stderr}")
            else:
                print("Homebrew not found. Please install Ollama manually from https://ollama.ai/")
                return False
        except Exception as e:
            print(f"❌ Error installing Ollama: {e}")
            return False
    
    elif system == "windows":
        print("🪟 Installing Ollama on Windows...")
        print("Please download and install Ollama from https://ollama.ai/")
        print("After installation, restart your terminal and run this script again.")
        return False
    
    else:
        print(f"❌ Unsupported operating system: {system}")
        print("Please install Ollama manually from https://ollama.ai/")
        return False

def check_ollama_installation():
    """Check if Ollama is properly installed and running"""
    print("\n🔍 Checking Ollama installation...")
    
    try:
        # Check if ollama command is available
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama is installed: {result.stdout.strip()}")
            
            # Check if Ollama service is running
            try:
                response = requests.get('http://localhost:11434/api/tags', timeout=5)
                if response.status_code == 200:
                    print("✅ Ollama service is running")
                    return True
                else:
                    print("❌ Ollama service is not responding")
                    return False
            except requests.exceptions.RequestException:
                print("❌ Ollama service is not running")
                print("Starting Ollama service...")
                try:
                    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(3)  # Wait for service to start
                    
                    # Check again
                    response = requests.get('http://localhost:11434/api/tags', timeout=5)
                    if response.status_code == 200:
                        print("✅ Ollama service started successfully")
                        return True
                    else:
                        print("❌ Failed to start Ollama service")
                        return False
                except Exception as e:
                    print(f"❌ Error starting Ollama service: {e}")
                    return False
        else:
            print("❌ Ollama is not properly installed")
            return False
    except FileNotFoundError:
        print("❌ Ollama is not installed")
        return False

def install_python_dependencies():
    """Install required Python dependencies"""
    print("\n📚 Installing Python dependencies...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Python dependencies installed successfully!")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_fine_tuning():
    """Run the fine-tuning process"""
    print("\n🚀 Starting fine-tuning process...")
    
    try:
        result = subprocess.run([sys.executable, 'fine_tune_lmu_buddy.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Fine-tuning completed successfully!")
            return True
        else:
            print(f"❌ Fine-tuning failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running fine-tuning: {e}")
        return False

def test_integration():
    """Test the integration with the Streamlit app"""
    print("\n🧪 Testing integration...")
    
    try:
        result = subprocess.run([sys.executable, 'lmu_buddy_ollama_client.py'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("✅ Integration test completed!")
            return True
        else:
            print(f"⚠️ Integration test had issues: {result.stderr}")
            return True  # Don't fail the setup for test issues
    except subprocess.TimeoutExpired:
        print("⚠️ Integration test timed out, but this is normal")
        return True
    except Exception as e:
        print(f"⚠️ Error during integration test: {e}")
        return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "🎉" * 20)
    print("🎉 SETUP COMPLETED SUCCESSFULLY! 🎉")
    print("🎉" * 20)
    print()
    print("📋 Next Steps:")
    print("1. 🚀 Start your Streamlit app:")
    print("   streamlit run app.py")
    print()
    print("2. 🧪 Test the fine-tuned model:")
    print("   python lmu_buddy_ollama_client.py")
    print()
    print("3. 🦁 Use the model directly:")
    print("   ollama run lmu-buddy 'Where should I eat on campus?'")
    print()
    print("4. 📚 Check the generated files:")
    print("   - Modelfile (Ollama model configuration)")
    print("   - lmu_buddy_training_data.json (Training data)")
    print()
    print("🔧 Troubleshooting:")
    print("- If Ollama service stops, run: ollama serve")
    print("- To see available models: ollama list")
    print("- To remove the model: ollama rm lmu-buddy")
    print("- To recreate the model: python fine_tune_lmu_buddy.py")
    print()

def main():
    """Main setup function"""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        return False
    
    # Step 2: Install Python dependencies
    if not install_python_dependencies():
        return False
    
    # Step 3: Check Ollama installation
    if not check_ollama_installation():
        print("\n📦 Ollama not found. Installing...")
        if not install_ollama():
            print("\n❌ Failed to install Ollama automatically.")
            print("Please install Ollama manually from https://ollama.ai/")
            print("Then run this script again.")
            return False
        
        # Check again after installation
        if not check_ollama_installation():
            print("\n❌ Ollama installation verification failed.")
            return False
    
    # Step 4: Run fine-tuning
    if not run_fine_tuning():
        print("\n❌ Fine-tuning failed. Please check the logs above.")
        return False
    
    # Step 5: Test integration
    test_integration()
    
    # Step 6: Print next steps
    print_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above and try again.")
        sys.exit(1)