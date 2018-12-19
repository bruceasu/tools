@echo off
set MYSQL_HOME=C:\Program Files\MySQL\MySQL Server 5.5
set PATH=%PATH%;%MYSQL_HOME%\bin
set USER=root
set PASSWD=root
set DB=freeib
set HOST=127.0.0.1
rem set HOST=172.30.6.55
set PORT=3306


set CMD=mysql -h %HOST% -P %PORT% -D %DB%  -u %USER% -p%PASSWD%
echo %CMD%
%CMD%
