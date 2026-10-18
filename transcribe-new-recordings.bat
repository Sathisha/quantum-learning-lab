@echo off
rem Double-click: transcribe every new recording in class-material (already-done ones are skipped).
rem Or drag a video or a folder onto this file to process just that.
title Class recordings: transcribe
cd /d "%~dp0"

docker info >NUL 2>&1
if errorlevel 1 (
  echo Docker Desktop is not running. Start it, wait until it shows "Engine running", then try again.
  echo.
  pause
  exit /b 1
)

call "%~dp0tools\class-pipeline\transcribe.cmd" %*

echo.
echo Finished. Results are in the .processed folder next to each recording.
echo Next: tell Claude "process this week's class material".
pause
