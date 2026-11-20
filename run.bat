@echo off
title StudyVerse AI - Virtual Study Platform
echo ======================================================================
echo           Starting StudyVerse AI Virtual Study Metaverse
echo ======================================================================
echo.

echo [1/3] Building and starting Docker containers...
docker compose up -d --build

echo.
echo [2/3] Waiting for Backend API and Nginx Ingress...
timeout /t 5 /nobreak >nul

echo.
echo [3/3] Opening StudyVerse in your default browser...
start http://localhost:3030

echo.
echo ======================================================================
echo StudyVerse is running at: http://localhost:3030
echo To run automated tests: python test_studyverse.py
echo To view logs: docker compose logs -f
echo To stop: docker compose down
echo ======================================================================
pause
