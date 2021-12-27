@echo off
set CODE=I:/haiouQz/trunk/yxqz
set FGUI=I:/haiouQz/trunk/yxqzUI
rem python FGUICodeTool.py --source %FGUI%/output/uicode --output %CODE%/src/game/uicode
python publish.py --type 1 --code %CODE% --fgui %FGUI%
pause