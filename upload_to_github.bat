@echo off
title Push StudyVerse Platform to GitHub
echo ======================================================================
echo           Pushing StudyVerse AI to GitHub
echo ======================================================================
echo.

git init
git branch -M main
git config user.name "divyakumari1107"
git config user.email "divyakumari1107@users.noreply.github.com"

git remote remove origin 2>nul
git remote add origin https://github.com/divyakumari1107/StudyVerse-Platform.git

echo.
echo Adding files to Git staging...
git add .

echo.
echo Committing files...
git commit -m "feat: complete StudyVerse AI real-time collaborative virtual study metaverse"

echo.
echo Pushing to GitHub (https://github.com/divyakumari1107/StudyVerse-Platform.git)...
git push -u origin main

echo.
echo ======================================================================
echo Done! If prompted, authenticate with your GitHub credentials or PAT.
echo ======================================================================
pause
