@echo off
title Logs CMD
powershell -Command "Get-Content sdtp/socket_messages.log -Wait -Tail 10"
pause
