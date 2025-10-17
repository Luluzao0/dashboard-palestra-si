@echo off
REM Script para iniciar o Dashboard

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          Dashboard - Análise Palestra SI                       ║
echo ║                                                                ║
echo ║  Iniciando Streamlit...                                       ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

python -m streamlit run SCRIPTS/dashboard_palestra.py

echo.
echo ❌ Dashboard finalizado.
pause
