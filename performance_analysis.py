__author__ = 'ywang'

import cx_Oracle
import ConnectDB
import string
import xlrd
from xlwt import *
import ConfigParser
import os
import time
from time import gmtime, strftime
import math

def generate_raw_file(connectionString,sqlfile, input_directory, input_file):
    sqlString = []

    for line in sqlfile:
        sqlString.append(line)
    #print "".join(sqlString)

    con = cx_Oracle.connect(connectionString)
    cur = con.cursor()
    cur.execute("".join(sqlString))

    res = cur.fetchone()
    raw_file = open(input_directory+'\\'+input_file, 'w+')
    while res is not None:
        for field in res :
            raw_file.write(str(field))
            raw_file.write(' | ')
        raw_file.write('\n')
        res = cur.fetchone()

    raw_file.close()
    cur.close()
    con.close()

def analyze_processing_script_total_time(input_directory, input_file):
    raw_file= open(input_directory+input_file, 'r')
    result=[['DM processing scripts listed according to execution time']]
    result.append(['MX Date','System Date','Script name','Execution time'])

    for line in raw_file:
        fields = line.split(' | ')
        current_result = [fields[0], fields[1],fields[2], time.strptime(fields[10],"%H:%M:%S")]

        for one_result in result :
            if one_result[0] == current_result[0] and one_result[1] == current_result[1] and one_result[2] == current_result[2]:
                one_result[2] = add_time(one_result[3],current_result[3])
                current_result = None
                break

        if current_result <> None :
            result.append(current_result)

    print result
    return result

def add_time(time_a,time_b):
    sum_time = time_a
    sec = time_a.tm_sec + time_b.tm_sec
    min = time_a.tm_min + time_b.tm_min + math.floor(sec/60)
    hour = time_a.tm_hour + time_b.tm_hour + math.floor(sec/60)
    sum_time = time.strptime(str(int(hour%24))+':'+str(int(min%60))+':'+str(int(sec%60)),"%H:%M:%S")
    return sum_time




if __name__ == "__main__":

    #define directories
    input_directory=os.getcwd()+'\Input\\'
    output_directory=os.getcwd()+'\Output\\'
    sql_directory=os.getcwd()+'\SQLs\\'
    property_directory=os.getcwd()+'\properties\\'

    #define sql files
    query_ps_time_sql='query_processing_script_time.sql'

    #define input files
    ps_exuection_time_file = 'ps_execution_time.csv'

    #define property files
    parameter_file='parameters.txt'
    mxDbsource_file='dbsource.mxres'

    #define output file
    final_result_file = 'analyze_performance.xls'

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)

    #prepare connection string
    connectionString = ConnectDB.loadMXDBSourcefile(property_directory + mxDbsource_file)


    sqlfile = open(sql_directory+query_ps_time_sql, 'r+')
    #generate_raw_file(connectionString,sqlfile,input_directory,ps_exuection_time_file)

    analyze_processing_script_total_time(input_directory,ps_exuection_time_file)
