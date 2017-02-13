set curr_path="D:\DEVTOOLS\Oracle-InstanceClient\instantclient_11_2"
SET PATH=%curr_path% 
SET TNS_ADMIN=%curr_path%
SET LD_LIBRARY_PATH=%curr_path%
SET SQLPATH=%curr_path%

echo Working path: %curr_path%

sqlplus /nolog
