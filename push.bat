@echo off
cd /d %~dp0
git add .
git commit --amend -m Initial
git push -u origin master --force
pause
