@echo off
title Online Study Hub - Virtual Learning Platform
echo ======================================================================
echo           Starting Online Study Hub Platform
echo ======================================================================
echo.

echo [1/3] Building and starting Docker containers...
docker compose up -d --build

echo.
echo [2/3] Waiting for Backend API and Nginx Ingress...
timeout /t 5 /nobreak >nul

echo.
echo [3/3] Opening Online Study Hub in your default browser...
start http://localhost:3030

echo.
echo ======================================================================
echo Online Study Hub is running at: http://localhost:3030
echo To run automated tests: python test_studyhub.py
echo To view logs: docker compose logs -f
echo To stop: docker compose down
echo ======================================================================
pause
