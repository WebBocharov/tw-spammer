@echo off

if exist venv/ (
    echo "Activating the virtual environment"
    .\venv\Scripts\activate

    echo "Installing dependencies"
    pip install -r requirements.txt

    echo "Starting the application"
    python main.py
) else (
    echo "Installing a virtual environment"
    pip install virtualenv

    echo "Creating a virtual environment"
    python -m venv venv

    echo "Activating the virtual environment"
    .\venv\Scripts\activate

    echo "Installing dependencies"
    pip install -r requirements.txt

    echo "Starting the application"
    python main.py
)

pause