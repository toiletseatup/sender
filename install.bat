@echo off
echo Installing necessary libraries and dependencies...

REM Install Python dependencies
pip install pdfkit
pip install smtplib
pip install email

REM Ensure wkhtmltopdf is installed
echo Checking if wkhtmltopdf is installed...
where wkhtmltopdf >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo wkhtmltopdf is not installed. Please download and install it from https://wkhtmltopdf.org/downloads.html
    pause
    exit /b
)

REM Provide a message indicating successful setup
echo All necessary libraries and dependencies have been installed.
pause
