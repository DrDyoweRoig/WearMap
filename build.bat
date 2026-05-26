@echo off
echo ============================================
echo   Wearmap - Build Windows Executable
echo ============================================
echo.

echo [1/2] Installing dependencies...
pip install PyQt6 Pillow numpy openpyxl pyinstaller
echo.

echo [2/2] Building executable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "Wearmap" ^
    --icon "logo.ico" ^
    --collect-all PyQt6 ^
    main.py

echo.
if exist "dist\Wearmap.exe" (
    echo ============================================
    echo   Build successful!
    echo   Executable: dist\Wearmap.exe
    echo ============================================
) else (
    echo Build failed. Check errors above.
)
echo.
pause
