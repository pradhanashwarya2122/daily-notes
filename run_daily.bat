@echo off
echo ========================================
echo DAILY NOTES COMMIT SYSTEM
echo ========================================
echo Starting: %date% %time%

cd C:\Users\Hp\Downloads\daily-notes

REM Set LLM environment variable
set FANCY_JOB_USE_LLM=true

REM Run the script
python update_number.py

REM Log the result
if %errorlevel%==0 (
    echo %date% %time% - SUCCESS >> logs\run_log.txt
    echo [SUCCESS] Commit created successfully
) else (
    echo %date% %time% - ERROR (code: %errorlevel%) >> logs\run_log.txt
    echo [ERROR] Something went wrong
)

echo ========================================
echo COMPLETE
echo ========================================