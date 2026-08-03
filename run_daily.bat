@echo off
cd C:\Users\Hp\Downloads\daily-notes

REM Run with LLM
set FANCY_JOB_USE_LLM=true
python update_number.py

REM Or run without LLM
REM python update_number.py

echo %date% %time% - Daily update completed >> logs\run_log.txt