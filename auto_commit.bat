@echo off

set /p message="Enter your commit message: "


git add .
git commit -m "%message%"
git push -u origin master

timeout /t 6 /nobreak

cls