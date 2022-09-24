echo on
echo ==============cutting line============== > D:\004-python-demo\din\commit.txt
::两个>表示在后追加，一个的话代表清除文件中原有的内容后再写入

set d=%date:~0,10%
:: 这里的两个冒号是注释

::%date:~x,y%以及%time:~x,y%
::说明：   x是开始位置，y是取得字符数
set t=%time:~0,8%

echo %d% %t% auto commit start... >>D:\004-python-demo\din\commit.txt
::%xy%引用变量xy

for /d %%i in (D:\004-python-demo\din\*) do (
cd %%i
IF EXIST .git (
echo %%i >> D:\004-python-demo\din\commit.txt
git add -A >> D:\004-python-demo\din\commit.txt
git commit -m "bat script auto commit" >>D:\004-python-demo\din\commit.txt
git pull >> D:\004-python-demo\din\commit.txt
git push >> D:\004-python-demo\din\commit.txt
echo ---------------------------------------- >> D:\004-python-demo\din\commit.txt
echo. >> D:\004-python-demo\din\commit.txt
)
cd ..
) 
echo ==============cutting line============== >>D:\004-python-demo\din\commit.txt


