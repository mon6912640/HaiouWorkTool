@echo off
set CODE=D:/work_haiou/branch/sanguo_wechat
set FGUI=D:/work_haiou/client/sanguoUI
python publish.py --type 1 --code %CODE% --fgui %FGUI%
pause