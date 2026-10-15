@echo off
setlocal
title Sentinel AI - Experimental Threshold 0.80
echo Sentinel AI -- Experimental Threshold 0.80
echo This is an unvalidated event-policy experiment. The frozen model is unchanged.

set "SENTINEL_EXPERIMENTAL_THRESHOLD=0.80"
set "SENTINEL_BACKEND_PORT=8010"
set "SENTINEL_FRONTEND_PORT=5180"
set "SENTINEL_DATABASE_URL=sqlite+pysqlite:///%~dp0backend/runtime/sentinel_exp_080.db"

call "%~dp0launch_sentinel_demo.cmd"
set "SENTINEL_EXPERIMENT_EXIT=%ERRORLEVEL%"
endlocal & exit /b %SENTINEL_EXPERIMENT_EXIT%
