# HaiouWorkTool  
Egret+FairyGUI项目相关的工作脚本  
python3.7  

----

### FGUICodeTool.py
把FairyGUI发布的Egret代码文件做二次精简，减少编译代码量，主要用途在于微信小游戏压缩代码
#### 使用方法
```cmd
python FGUICodeTool.py --source xxx --output xxx
```
```yaml
参数说明：
--source FairyGUI工程发布目录
--output 重新输出的发布目录
```

---

### Copy2Work.py
复制发布的bin和altas文件到指定的工作目录
#### 使用方法
```cmd
python Copy2Work.py --pkg xxx,xxx --source xxx --to xxx
```
```yaml
参数说明：
--pkg（可选） 指定的包名称列表，用逗号分隔，默认为空则为输出所有包
--source fui工程的发布目录
--to 输出的目录
```