@echo off >nul 2>&1 
"%SYSTEMROOT%\system32\cacls.exe"  "%SYSTEMROOT%\system32\config\system" 
if '%errorlevel%' NEQ '0' (
goto UACPrompt 
) else ( goto gotAdmin )

:UACPrompt 
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs" 
echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs" 
exit /B 

:gotAdmin 
if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
pushd "%CD%" 
CD /D "%~dp0"

echo start redis
taskkill /fi "windowtitle eq redis-server"
start cmd /c C:\programs\redis-on-windows-latest\start-sever.bat

echo start MySQL
call C:\programs\shell\startMySQL.cmd

::: echo start kafka
::: taskkill /fi "windowtitle eq kafka"
::: start cmd /c C:\programs\kafka_2.11-0.10.0.0\start-kafka.bat

::: echo start zkserver
::: taskkill /fi "windowtitle eq zkServer"
::: start cmd /c C:\programs\apache-zookeeper-3.4.6\bin\zkServer.cmd

::: echo start RabbitMQ
::: call C:\programs\shell\startRabbitMQ.cmd

::: echo start oracle
::: net start OracleOraDB12Home2TNSListener
::: net start OracleRemExecServiceV2
::: net start OracleServiceORCL
::: net start OracleVssWriterORCL

pause