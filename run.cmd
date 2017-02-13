@ECHO OFF

setlocal

set ORACLE_HOME=instantclient_11_2
SET PATH=instantclient_11_2;%PATH%

if exist OCI.dll del OCI.dll

main.exe

pause