@echo off
powershell -Command "Get-Content sdtp/socket_messages.log -Wait -Tail 10"
pause
