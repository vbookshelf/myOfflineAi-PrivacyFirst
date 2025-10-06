@echo off
echo ============================================
echo   Starting myOfflineAi (Privacy-First AI)
echo ============================================

REM Ensure script runs from the repo folder
cd /d %~dp0

REM --- Check for Ollama ---
where ollama >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Ollama is not installed.
    echo Please install from: https://ollama.com/download
    pause
    exit /b
)

REM --- Check for uv ---
where uv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] 'uv' is not installed.
    echo See: https://docs.astral.sh/uv/getting-started/installation
    pause
    exit /b
)

REM --- Create venv if missing ---
IF NOT EXIST .venv (
    echo [INFO] Creating Python 3.10 environment via uv...
    uv venv --python 3.10
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create Python 3.10 environment via uv.
        pause
        exit /b
    )
)

REM --- Activate venv ---
call .venv\Scripts\activate

REM --- Lock & Sync dependencies ---
echo [INFO] Updating lockfile...
uv lock
if %ERRORLEVEL% neq 0 (
    echo [ERROR] uv failed to update lockfile
    pause
    exit /b
)

echo [INFO] Syncing dependencies...
uv sync
if %ERRORLEVEL% neq 0 (
    echo [ERROR] uv failed to sync dependencies
    pause
    exit /b
)

REM --- Launch app ---
echo [INFO] Launching app...
python app.py

pause
