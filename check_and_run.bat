@echo off
cd C:\Users\Hp\Downloads\daily-notes

echo [CHECK] Verifying system...

REM Check if number.txt exists
if not exist number.txt (
    echo [FIX] Creating number.txt
    echo 0 > number.txt
)

REM Check if git repository is clean
git status --porcelain > temp.txt
findstr /C:"number.txt" temp.txt > nul
if %errorlevel%==0 (
    echo [FIX] Uncommitted changes found, committing...
    python update_number.py
)

del temp.txt

REM Run the main script
echo [RUN] Executing daily update...
call run_daily.bat

echo [DONE] Check complete at %date% %time%