@echo off
setlocal

set "ADDIN_NAME=CliffDrop"
set "SRC=%~dp0%ADDIN_NAME%"

:: --- Locate Fusion AddIns directory ---
set "DEST="
if exist "%APPDATA%\Autodesk\Autodesk Fusion\API\AddIns" (
    set "DEST=%APPDATA%\Autodesk\Autodesk Fusion\API\AddIns\%ADDIN_NAME%"
) else if exist "%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns" (
    set "DEST=%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\%ADDIN_NAME%"
)

if "%DEST%"=="" (
    echo.
    echo  ERROR: Could not find the Fusion AddIns directory.
    echo  Looked in:
    echo    %APPDATA%\Autodesk\Autodesk Fusion\API\AddIns
    echo    %APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns
    echo.
    echo  Make sure Autodesk Fusion is installed before running this script.
    echo.
    pause
    exit /b 1
)

echo.
echo  CliffDrop Installer
echo  ====================
echo  Source : %SRC%
echo  Target : %DEST%
echo.

:: --- Remove previous install ---
if exist "%DEST%" (
    echo  Removing previous installation...
    rmdir /s /q "%DEST%"
)

:: --- Copy add-in files ---
echo  Copying files...
xcopy /e /i /y /q "%SRC%" "%DEST%" >nul

if %ERRORLEVEL% neq 0 (
    echo  ERROR: File copy failed.
    pause
    exit /b 1
)

echo.
echo  Installation complete!
echo.
echo  Next steps:
echo    1. Open (or restart) Autodesk Fusion
echo    2. Go to UTILITIES tab ^> ADD-INS
echo    3. Find "CliffDrop" in the Add-Ins list and click Run
echo    4. The "Cycloidal Curve" command appears in SOLID ^> CREATE
echo.
pause
