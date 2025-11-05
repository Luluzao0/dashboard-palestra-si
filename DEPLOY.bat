@echo off
chcp 65001 >nul
cls
echo ==========================================
echo    DEPLOY GLOBAL - Dashboard Palestra
echo ==========================================
echo.
echo Instalando dependências...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo Erro ao instalar dependências
    pause
    exit /b 1
)
echo ✓ Dependências OK
echo.
echo Executando Deploy Global...
python DEPLOY_GLOBAL.py
pause
