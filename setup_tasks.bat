@echo off
echo ========================================
echo SETTING UP PERMANENT TASKS
echo ========================================

cd C:\Users\Hp\Downloads\daily-notes

REM Create logs folder
mkdir logs 2>nul

REM MAIN TASK: Runs daily at 9:00 AM
schtasks /create /tn "Daily Notes Update" /tr "C:\Users\Hp\Downloads\daily-notes\run_daily.bat" /sc daily /st 09:00 /ru "SYSTEM" /f

REM BACKUP TASK: Runs at 12:00 PM (in case first one fails)
schtasks /create /tn "Daily Notes Update - Backup" /tr "C:\Users\Hp\Downloads\daily-notes\run_daily.bat" /sc daily /st 12:00 /ru "SYSTEM" /f

REM EVENING TASK: Runs at 6:00 PM
schtasks /create /tn "Daily Notes Update - Evening" /tr "C:\Users\Hp\Downloads\daily-notes\run_daily.bat" /sc daily /st 18:00 /ru "SYSTEM" /f

REM WEEKLY HEALTH CHECK: Every Sunday at 10:00 AM
schtasks /create /tn "Daily Notes Health Check" /tr "python C:\Users\Hp\Downloads\daily-notes\system_health_check.py" /sc weekly /d SUN /st 10:00 /ru "SYSTEM" /f

echo ========================================
echo TASKS CREATED SUCCESSFULLY!
echo ========================================
schtasks /query | findstr "Daily Notes"
pause