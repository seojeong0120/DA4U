@echo off
chcp 65001 > nul
echo.
echo ============================================================
echo 📦 Installing Dependencies - Conda Base Environment
echo ============================================================
echo.

cd /d "%~dp0"

REM Activate conda base
echo 🐍 Activating conda base environment...
call conda activate base

echo.
echo 📥 Installing Python packages...
pip install -r requirements.txt

echo.
echo ✅ All dependencies installed successfully!
echo.
echo Next steps:
echo   1. Run setup_env.bat to configure API keys
echo   2. Run run_all.bat to start the system
echo.
pause

