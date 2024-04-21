import sys
from main import LLM_Switcher, models # Replace 'your_main_script' with the actual name of your main script

def main():
    switcher = LLM_Switcher(models) # You need to define 'models' here or import it from your main script
    if '-v' in sys.argv:
        if switcher.last_used_model:
            print(f"Last used model: {switcher.last_used_model.name}")
        else:
            print("No model has been used yet.")
    else:
        print("Use the -v flag to see the last used model.")

if __name__ == "__main__":
    main()
