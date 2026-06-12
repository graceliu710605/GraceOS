@echo off
chcp 65001 >nul
title 个人数字资产管家

cd /d "%~dp0"

echo.
echo ============================================
echo       个人数字资产管家
echo    Personal Digital Operating System
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+
    echo          https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found

:: Check dependencies
echo [INFO] Checking dependencies...
pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing dependencies...
    pip install streamlit pandas pywin32 -q
)

:: First-run check
if not exist "first_run_done" (
    echo.
    echo ============================================
    echo   First Run - Initial Setup
    echo ============================================
    echo.
    
    echo [STEP 1/4] Running software scanner...
    python -c "from scanners import software_scanner; software_scanner.scan()" 2>&1 | find "Found" >nul
    if %errorlevel% neq 0 (
        python -c "from scanners import software_scanner; software_scanner.scan()" 2>nul
    )
    echo [OK] Software scan done

    echo [STEP 2/4] Running disk scanner...
    python -c "from scanners import disk_scanner; disk_scanner.scan()" 2>nul
    echo [OK] Disk scan done

    echo [STEP 3/4] Importing data to database...
    python software_to_sqlite.py 2>nul
    python disk_to_sqlite.py 2>nul
    echo [OK] Data import done

    echo [STEP 4/4] Calculating initial health score...
    python -c "from analyzers.health_scorer import calculate; r=calculate(); print(f'Score: {r["total"]}/100')" 2>nul
    echo [OK] Initial score calculated

    :: Mark first run complete
    echo %date% %time% > first_run_done
    
    echo.
    echo [DONE] Initial setup complete!
    echo.
)

echo [INFO] Starting GraceOS Dashboard...
echo.
echo    Open in browser: http://localhost:8501
echo    Press Ctrl+C to stop
echo.
start "" http://localhost:8501
streamlit run dashboard.py --server.port 8501
