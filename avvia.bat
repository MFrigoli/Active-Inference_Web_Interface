@echo off
title Railway Active Inference
cd /d "%~dp0"
echo.
echo  =========================================
echo   Railway Active Inference - Demo Web
echo  =========================================
echo.
echo  Avvio in corso...
echo  Il browser si apre automaticamente.
echo.
echo  Per fermare il server: chiudi questa finestra.
echo.
streamlit run app_streamlit.py
pause
