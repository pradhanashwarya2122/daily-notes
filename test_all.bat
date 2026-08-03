@echo off
echo ========================================
echo  DAILY NOTES COMMIT SYSTEM TEST
echo ========================================
echo.

echo [1/6] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo ✓ Python is installed
echo.

echo [2/6] Checking required files...
if exist update_number.py (
    echo ✓ update_number.py exists
) else (
    echo ✗ update_number.py NOT FOUND
)
if exist number.txt (
    echo ✓ number.txt exists
) else (
    echo ✗ number.txt NOT FOUND
)
echo.

echo [3/6] Testing without LLM...
set FANCY_JOB_USE_LLM=false
python update_number.py
if errorlevel 1 (
    echo ✗ Test failed
) else (
    echo ✓ Test passed
)
echo.

echo [4/6] Testing with LLM...
set FANCY_JOB_USE_LLM=true
python update_number.py
if errorlevel 1 (
    echo ✗ Test failed
) else (
    echo ✓ Test passed
)
echo.

echo [5/6] Checking git status...
git status
echo.

echo [6/6] Checking commit history...
git log --oneline -3
echo.

echo ========================================
echo  TEST COMPLETE
echo ========================================
pause