@echo off
python --version
IF ERRORLEVEL 1 (
    echo Command "python" not found. Trying "py"...
    py --version
    IF ERRORLEVEL 1 (
        echo Python is not installed. Please install Python and try again.
        exit /b
    )
)

pip --version
IF ERRORLEVEL 1 (
    echo Command "pip" not found. Trying "py -m pip"...
    py -m pip --version
    IF ERRORLEVEL 1 (
        echo pip is not installed. Attempting to install pip...
        py -m ensurepip --default-pip
        IF ERRORLEVEL 1 (
            echo Failed to install pip. Please install it manually.
            exit /b
        )
    )
)

pip install -r requirements.txt
IF ERRORLEVEL 1 (
    echo Failed to use pip. Trying "py -m pip"...
    py -m pip install -r requirements.txt
    IF ERRORLEVEL 1 (
        echo Failed to install required packages. Please check your requirements.txt.
        exit /b
    )
)

python main.py
IF ERRORLEVEL 1 (
    echo Command "python" failed. Trying "py"...
    py main.py
    IF ERRORLEVEL 1 (
        cls
        echo Failed to run the Python script. Ensure Python is installed and properly configured.
        exit /b
    )
)
