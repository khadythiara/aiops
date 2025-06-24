@echo off
set count=0
set max=20

:loop
curl -s http://localhost:8000/analyze >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ ML API is up!
    exit /B 0
) else (
    echo ⏳ Waiting for ML API...
    timeout /T 5 >nul
    set /A count+=1
    if %count% LSS %max% goto loop
    echo ❌ Timeout: ML API is still not responding.
    exit /B 1
)
