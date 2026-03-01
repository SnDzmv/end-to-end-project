@echo off


set CONDA_EXE=%USERPROFILE%\miniconda3\Scripts\conda.exe


set ENV_NAME=week1_env


set SCRIPT_DIR=%~dp0


set ERROR_OCCURRED=


if not exist "%CONDA_EXE%" (
    echo [ERROR] Conda not found! Install Miniconda first.
    pause
    exit /b 1
)


echo Creating environment %ENV_NAME%...
%CONDA_EXE% create -y -n %ENV_NAME% python=3.11
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create environment.
    set ERROR_OCCURRED=1
)


echo Installing dependencies from requirements.txt...
%CONDA_EXE% run -n %ENV_NAME% python -m pip install --upgrade pip
%CONDA_EXE% run -n %ENV_NAME% python -m pip install --upgrade --force-reinstall -r "%SCRIPT_DIR%requirements.txt"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    set ERROR_OCCURRED=1
)


echo.
if defined ERROR_OCCURRED (
    echo [ERROR] One or more steps failed. Check above messages.
) else (
    echo [OK] Environment and dependencies are ready!
)

echo.
echo Press any key to exit...
pause >nul
exit /b 0
