@echo off
node "%~dp0run.cjs" %*
exit /b %errorlevel%
