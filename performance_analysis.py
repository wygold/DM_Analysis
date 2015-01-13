__author__ = 'ywang'

import string
from xlwt import *
import ConfigParser
import os
import datetime
import math
from operator import itemgetter, attrgetter, methodcaller
from db_utility import db_utility
from io_utility import io_utility
import logging
from logging import handlers
from property_utility import property_utility

logger = ''

def initialize_log( log_level = 'INFO', log_file = None):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # create a file handler
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(log_level)

    # add the handlers to the logger
    logger.addHandler(handler)

def set_log_level( log_level):
    logger = logging.getLogger(__name__)
    for handler in logger.handlers:
        if log_level is not None:
            handler.setLevel(log_level)
        else:
            handler.setLevel(log_level)


def analyze_processing_script_total_time(input_directory, input_file,time_alert_processing_script,period_days):
    logger = logging.getLogger(__name__)
    logger.info('Start to run analyze_processing_script_total_time on file %s%s',input_directory, input_file)
    raw_file= open(input_directory+input_file, 'r')
    final_result=[['DM processing scripts listed according to execution time']]
    final_result.append(['MX Date','System Date','Script name','Execution time', 'Highlight'])
    result = []

    for line in raw_file:
        fields = line.split(' | ')

        current_result = [fields[0], fields[1],fields[2], fields[10]]
        logger.debug('Raw line: %s',fields)
        logger.debug('Processed line: %s',current_result)

        for one_result in result :
            if one_result[0] == current_result[0] and one_result[1] == current_result[1] and one_result[2] == current_result[2]:
                logger.debug('Combine different feeders/extraction in same processing script for %s', one_result[2])
                one_result[3] = add_time(one_result[3],current_result[3])
                #because current result is already merged, so set it to None
                current_result = None
                break

        if current_result <> None :
            logger.debug('Final processing for: %s',current_result)
            result.append(current_result)

    #sort the result
    logger.debug('Sort the result')

    filtered_result = []
    if len(result) > 0:
        sorted_result = sorted(result,key=itemgetter(0,1,3),reverse=True)

        #apply period days
        current_day =  datetime.datetime.strptime(sorted_result[0][0], '%Y-%m-%d %H:%M:%S').date()


        #filtering the data according to the date
        logger.info('Filtering the result old than : %s days',period_days)
        for result in sorted_result:
            result_date =  datetime.datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S').date()
            if result_date > current_day - datetime.timedelta(days=period_days):
                filtered_result.append(result)

        #highlight the data according to time alert
        logger.debug('Highlight the result running longer than : %s',time_alert_processing_script)
        for one_result in filtered_result:
            if one_result[3] > time_alert_processing_script:
                one_result.append('True')
            else:
                one_result.append('False')

    #append with head and title
    final_result.extend(filtered_result)

    logger.info('End to run analyze_processing_script_total_time.')
    return final_result

def analyze_processing_script_breakdown(input_directory, input_file,time_alert_batch_feeder
                                        ,time_alert_batch_extraction,period_days ):
    logger = logging.getLogger(__name__)
    logger.info('Start to run analyze_processing_script_breakdown on file %s%s.',input_directory, input_file)
    raw_file= open(input_directory+input_file, 'r')
    final_result=[['DM processing scripts listed according to execution time']]
    final_result.append(['MX Date','System Date','Script name','DM_OBJECT_NAME','M_STEP','M_USER','M_GROUP'
        ,'M_DESK','CPU_TIME','IO_TIME','TOTAL_TIME','OBJECT_TYPE', 'Highlight'])

    result = []
    for line in raw_file:
        fields = line.split(' | ')
        logger.debug('line appended: %s',fields)
        result.append(fields)

    filtered_result = []

    if len(result) > 0 :
        #sort the result
        logger.info('Sort the result.')
        sorted_result = sorted(result,key=itemgetter(0,1,10),reverse=True)

        #highlight rows according to time alert
        logger.info('Highlight the batch of feeder running longer than : %s',time_alert_batch_feeder)
        logger.info('Highlight the batch of extraction running longer than : %s',time_alert_batch_extraction)
        for one_result in sorted_result:
            if (one_result[11].rstrip('\n').rstrip() =='REP_BATCHES_FEED' and one_result[10] > time_alert_batch_feeder) \
                    or (one_result[11].rstrip('\n').rstrip() =='REP_BATCHES_EXT' and one_result[10] > time_alert_batch_extraction) :
                one_result.append('True')
            else:
                one_result.append('False')

        #apply period days
        logger.info('Filtering the result old than : %s days',period_days)
        current_day =  datetime.datetime.strptime(sorted_result[0][0], '%Y-%m-%d %H:%M:%S').date()


        for result in sorted_result:
            result_date =  datetime.datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S').date()
            if result_date > current_day - datetime.timedelta(days=period_days):
                filtered_result.append(result)

        #append with head and title
    final_result.extend(filtered_result)

    logger.info('End running analyze_processing_script_breakdown.')
    return final_result

#add up time A and time B
def add_time(ta,tb):
    logger = logging.getLogger(__name__)
    logger.debug('Start to run add_time.')
    logger.debug('Add %s and %s.', ta, tb)
    ta_hour,ta_min, ta_sec = string.split(ta,":")
    tb_hour,tb_min, tb_sec = string.split(tb,":")
    sec = int(ta_sec) + int(tb_sec)
    min = int(ta_min) + int(tb_min) + math.floor(sec/60)
    hour =  int(ta_hour) + int(tb_hour) + math.floor(sec/60)
    sum_time = str(int(hour%24)).rjust(2, '0')+':'+str(int(min%60)).rjust(2, '0')+':'+str(int(sec%60)).rjust(2, '0')
    logger.debug('%s + %s = %s', ta, tb, sum_time)
    logger.debug('End running add_time.')
    return sum_time

def run(reload_check_button_status=None,log_dropdown_status=None):
    #define properties folder
    property_directory=os.getcwd()+'\\properties\\'
    parameter_file='parameters.txt'

    property_util = property_utility()
    parameters = property_util.parse_property_file(property_directory,parameter_file)

    #define sql files
    query_ps_time_sql='query_processing_script_time.sql'

    #define input files
    ps_exuection_time_file = 'ps_execution_time.csv'

    #define property files
    mxDbsource_file=parameters['database']['mx_db_config_file']

    #define output file
    final_result_file = parameters['performance']['output_file_name']

    #define log file
    log_file = parameters['performance']['log_file_name']

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
    period_days = config.getint('performance', 'period_days')
    start_date = config.get('performance', 'start_date')
    end_date = config.get('performance', 'end_date')
    time_alert_processing_script = config.get('performance', 'time_alert_processing_script')
    time_alert_batch_feeder = config.get('performance', 'time_alert_batch_feeder')
    time_alert_batch_extraction =config.get('performance', 'time_alert_batch_extraction')

    #define directories
    input_directory=os.getcwd()+'\\'+config.get('general', 'input_directory')+'\\'
    output_directory=os.getcwd()+'\\'+config.get('general', 'output_directory')+'\\'
    sql_directory=os.getcwd()+'\\'+config.get('general', 'sql_directory')+'\\'
    log_directory =os.getcwd()+'\\'+config.get('log', 'log_directory')+'\\'

    if log_dropdown_status is None :
        log_level = config.get('log', 'log_level')
    else:
        log_level = log_dropdown_status
    initialize_log(log_level,log_directory+log_file)

    logger = logging.getLogger(__name__)
    logger.info('Start to run performance_analysis.py.')

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
    reload_data = config.getboolean('general', 'reload_data')

    if (reload_check_button_status is None and reload_data) or (reload_check_button_status):
        #prepare connection string
        db_util = db_utility(log_level,log_directory+log_file)
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

    #create io_class
    io_util= io_utility(log_level,log_directory+log_file)

    #workbook for output result
    work_book = Workbook()

    #Get processing script overall performance
    result=analyze_processing_script_total_time(input_directory,ps_exuection_time_file
                                                ,time_alert_processing_script, period_days)
    work_sheet_name='Processing script performance'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name, True)

    #Get processing script detailed performance
    result=analyze_processing_script_breakdown(input_directory, ps_exuection_time_file,
                                               time_alert_batch_feeder,time_alert_batch_extraction,period_days)
    work_sheet_name='Processing script detailed'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name, True)

    #output the work_book
    io_util.save_workbook(work_book,output_directory+final_result_file)
    logger.info('end running performance_analysis.py.')

if __name__ == "__main__":
    run()