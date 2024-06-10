import subprocess
import sys
from configs import testing #type:ignore

def install_requirements():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")
        sys.exit(1)

if __name__ == '__main__':    
    # Install requirements if in production mode
    if testing == 0:
        install_requirements()

    from home.home_controller import main  # Import after installation
    main()
