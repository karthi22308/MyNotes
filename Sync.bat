@echo off
REM Change to your repo directory
cd /d C:\MyNotes

REM Add all changes
git add .

REM Ask for a commit message
set /p user_comment=Enter commit message (leave empty to use date): 

REM Get current date in dd/MM format and store in a variable
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do (
    set day=%%a
    set month=%%b
    set year=%%c
)

REM Detect if Windows date format is dd/MM/yyyy or MM/dd/yyyy
if %day% gtr 12 (
    set commit_date=%day%/%month%
) else (
    set commit_date=%month%/%day%
)

REM Check if user gave a comment
if "%user_comment%"=="" (
    git commit -m "commit on %commit_date%"
) else (
    git commit -m "%user_comment%"
)

REM Push to remote
git push

pause
