@echo off
REM Change directory to the location of Redis
cd "C:\Program Files\Redis"

REM Start Redis server
start redis-server.exe redis.windows.conf

REM Optional: Run Redis CLI in a separate command prompt
REM Uncomment the line below if you want to open the CLI
REM start redis-cli.exe

REM Pause to keep the window open (optional)
pause