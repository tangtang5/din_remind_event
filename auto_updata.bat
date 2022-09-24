echo on
set CurrentPath=%~dp0
::获取当前bat的路径，但是还需要获取上一级路径，需要拆散，重新拼接字符
set P1Path=
set P2Path=

:begin
for /f "tokens=1,* delims=\" %%i in ("%CurrentPath%") do (set content=%%i&&set CurrentPath=%%j)
if "%P1Path%%content%\" == "%~dp0" goto end
 
set P2Path=%P1Path%
set P1Path=%P1Path%%content%\
 
goto begin
 
:end
echo BatPath=%~dp0
echo P1Path=%P1Path%


echo ==============cutting line============== > %P1Path%commit.txt
::两个>表示在后追加，一个的话代表清除文件中原有的内容后再写入

set d=%date:~0,10%
:: 这里的两个冒号是注释

::%date:~x,y%以及%time:~x,y%
::说明：   x是开始位置，y是取得字符数
set t=%time:~0,8%

echo %d% %t% auto commit start... >>%P1Path%commit.txt
::%xy%引用变量xy

for /d %%i in (%P1Path%*) do (
cd %%i
IF EXIST .git (
echo %%i >> %P1Path%commit.txt
git add -A >> %P1Path%commit.txt
git commit -m "bat script auto commit" >>%P1Path%commit.txt
git pull >> %P1Path%commit.txt
git push >> %P1Path%commit.txt
echo ---------------------------------------- >> %P1Path%commit.txt
echo. >> %P1Path%commit.txt
)
cd ..
) 
echo ==============cutting line============== >>%filename%commit.txt


