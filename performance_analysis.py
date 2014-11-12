__author__ = 'ywang'

import cx_Oracle

import string
from xlwt import *
import ConfigParser
import os
import datetime
import math
from operator import itemgetter, attrgetter, methodcaller
from db_utility import db_utility
import io_utility

def analyze_processing_script_total_time(input_directory, input_file,time_alert_processing_script,period_days):
    raw_file= open(input_directory+input_file, 'r')
    final_result=[['DM processing scripts listed according to execution time']]
    final_result.append(['MX Date','System Date','Script name','Execution time'])
    result = []
    for line in raw_file:
        fields = line.split(' | ')
        current_result = [fields[0], fields[1],fields[2], fields[10]]

        for one_result in result :
            if one_result[0] == current_result[0] and one_result[1] == current_result[1] and one_result[2] == current_result[2]:
                one_result[3] = add_time(one_result[3],current_result[3])
                current_result = None
                break

        if current_result <> None :
            result.append(current_result)

    #sort the result
    sorted_result = sorted(result,key=itemgetter(0,1,3),reverse=True)

    #apply period days
    current_day =  datetime.datetime.strptime(sorted_result[0][0], '%Y-%m-%d %H:%M:%S').date()
    filtered_result = []

    for result in sorted_result:
        result_date =  datetime.datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S').date()
        if result_date > current_day - datetime.timedelta(days=period_days):
            filtered_result.append(result)

    for one_result in filtered_result:
        if one_result[3] > time_alert_processing_script:
            one_result.append('True')
        else:
            one_result.append('False')

    #append with head and title
    final_result.extend(filtered_result)
    return final_result

def analyze_processing_script_breakdown(input_directory, input_file,time_alert_batch_feeder
                                        ,time_alert_batch_extraction,period_days ):
    raw_file= open(input_directory+input_file, 'r')
    final_result=[['DM processing scripts listed according to execution time']]
    final_result.append(['MX Date','System Date','Script name','DM_OBJECT_NAME','M_STEP','M_USER','M_GROUP'
        ,'M_DESK','CPU_TIME','IO_TIME','TOTAL_TIME','OBJECT_TYPE'])

    result = []
    for line in raw_file:
        fields = line.split(' | ')
        result.append(fields)

    #sort the result
    sorted_result = sorted(result,key=itemgetter(0,1,10),reverse=True)

    for one_result in sorted_result:
        if (one_result[11].rstrip('\n').rstrip() =='REP_BATCHES_FEED' and one_result[10] > time_alert_batch_feeder) \
                or (one_result[11].rstrip('\n').rstrip() =='REP_BATCHES_EXT' and one_result[10] > time_alert_batch_extraction) :
            one_result.append('True')
        else:
            one_result.append('False')

    #apply period days
    current_day =  datetime.datetime.strptime(sorted_result[0][0], '%Y-%m-%d %H:%M:%S').date()
    filtered_result = []

    for result in sorted_result:
        result_date =  datetime.datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S').date()
        if result_date > current_day - datetime.timedelta(days=period_days):
            filtered_result.append(result)

    #append with head and title
    final_result.extend(filtered_result)
    return final_result

#add up time A and time B
def add_time(ta,tb):
    ta_hour,ta_min, ta_sec = string.split(ta,":")
    tb_hour,tb_min, tb_sec = string.split(tb,":")
    sec = int(ta_sec) + int(tb_sec)
    min = int(ta_min) + int(tb_min) + math.floor(sec/60)
    hour =  int(ta_hour) + int(tb_hour) + math.floor(sec/60)
    sum_time = str(int(hour%24)).rjust(2, '0')+':'+str(int(min%60)).rjust(2, '0')+':'+str(int(sec%60)).rjust(2, '0')
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
    period_days = config.getint('performance', 'period_days')
    start_date = config.get('performance', 'start_date')
    end_date = config.get('performance', 'end_date')
    time_alert_processing_script = config.get('performance', 'time_alert_processing_script')
    time_alert_batch_feeder = config.get('performance', 'time_alert_batch_feeder')
    time_alert_batch_extraction =config.get('performance', 'time_alert_batch_extraction')

    #prepare connection string
    db_util = db_utility()
    connectionString = db_util.load_dbsourcefile(property_directory + mxDbsource_file)

    #prepare SQLs to be run
    sqlfile = open(sql_directory+query_ps_time_sql, 'r+')
    sqlString= ''
    for line in sqlfile:
        sqlString = sqlString + line

    #prepare sql paramaters, the paramaters are defined according to MX format @:paramater_name:N/D/C
    sql_paramters = dict()
    sql_paramters['START_DATE'] = start_date
    sql_paramters['END_DATE'] = end_date

    #dump file
    db_util.dump_output(sqlString, sql_paramters, connectionString, input_directory + ps_exuection_time_file)

    #workbook for output result
    work_book = Workbook()

    #Get processing script overall performance
    result=analyze_processing_script_total_time(input_directory,ps_exuection_time_file
                                                ,time_alert_processing_script, period_days)
    work_sheet_name='Processing script performance'
    work_book=io_utility.add_worksheet(result,work_book, work_sheet_name, True)

    #Get processing script detailed performance
    result=analyze_processing_script_breakdown(input_directory, ps_exuection_time_file,
                                               time_alert_batch_feeder,time_alert_batch_extraction,period_days)
    work_sheet_name='Processing script detailed'
    work_book=io_utility.add_worksheet(result,work_book, work_sheet_name, True)

    #output the work_book
    io_utility.save_workbook(work_book,output_directory+final_result_file)


