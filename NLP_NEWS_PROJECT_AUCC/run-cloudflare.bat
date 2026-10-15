@echo off
node "%~dp0run.cjs" --cloudflare %*
exit /b %errorlevel%
