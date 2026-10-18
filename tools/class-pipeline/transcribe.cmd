@echo off
rem One command: transcribe.cmd "C:\path\to\lecture.mp4" [-Notes] [-Cpu]
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0transcribe.ps1" %*
