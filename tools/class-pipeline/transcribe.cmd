@echo off
rem transcribe.cmd [video or folder] [-Notes] [-Cpu] [-Rebuild]   (no path = everything new in "class material")
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0transcribe.ps1" %*
