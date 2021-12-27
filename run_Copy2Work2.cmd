@echo off
set CODE=D:/work_haiou/branch/sanguo_wechat/src
set GUI=./fabu
set XML=./assets
python Copy2Work2.py --type 1 --pkg common --code %CODE% --gui %GUI% --xml %XML%
echo %ERRORLEVEL%
rem echo fuckyou
pause