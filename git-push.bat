@echo off
cd /d %~dp0
git add .
git commit --amend -m "Initial commit"
git push -u origin master --force
pause
