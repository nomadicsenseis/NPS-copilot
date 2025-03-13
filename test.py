# test_ollama.py
import requests
import json
import time

def list_models():
    """List all available models in Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print("Available models:")
                for model in models:
                    print(f"- {model['name']}")
            else:
                print("No models found. Use 'ollama pull <model>' to download a model.")
        else:
            print(f"Failed to list models: {response.text}")
    except Exception as e:
        print(f"Error listing models: {str(e)}")

def test_model(model_name="tinyllama"):
    """Test an Ollama model with a simple prompt"""
    prompt = "What is machine learning? Answer briefly."
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\nPrompt: {prompt}")
            print(f"Response from {model_name}:")
            print(result.get("response", "No response"))
        else:
            print(f"Query failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error testing model: {str(e)}")

if __name__ == "__main__":
    print("Checking Ollama service...")
    
    try:
        # Check if Ollama service is running
        response = requests.get("http://localhost:11434")
        print("✅ Ollama service is running")
    except requests.exceptions.ConnectionError:
        print("❌ Ollama service might not be running. Trying to start it...")
        import os
        os.system("ollama serve &")
        print("Waiting for service to start...")
        time.sleep(5)
    
    # List available models
    list_models()
    
    # Ask user if they want to pull a model
    model_choice = input("\nDo you want to pull a model? (yes/no): ")
    if model_choice.lower() in ["yes", "y"]:
        model_name = input("Enter model name (or press Enter for 'tinyllama'): ") or "tinyllama"
        print(f"Pulling {model_name} (this might take a few minutes)...")
        os.system(f"ollama pull {model_name}")
        
        # Test the model
        test_model(model_name)
    else:
        print("Skipping model pull.")