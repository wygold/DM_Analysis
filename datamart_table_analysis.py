__author__ = 'ywang'


from xlwt import *
import ConfigParser
import os
from db_utility import db_utility
from io_utility import io_utility
import logging
from logging import handlers

log_level = logging.DEBUG
logger = ''


def initialize_log( log_level=None, log_file = None):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)



    # create a file handler
    handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if log_level is not None:
        handler.setLevel(log_level)
    else:
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


#1 Total number of datamart tables fields for each datamart table. If more than 100, list out as red, if it is more than 50
def check_total_datamart_table_field_number(input_directory,input_file, max_datamart_fields) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_total_datamart_table_field_number on file %s%s with max field %i.',input_directory,input_file,max_datamart_fields)

    result=[['Datamart table fields exceeds '+str(max_datamart_fields)]]
    result.append(['Datamart table name','Field count'])
    datamart_tables = dict()

    for line in raw_file:
        fields = line.split(' | ')

        if fields[24].strip()<>'' and int(fields[25])> max_datamart_fields :
            datamart_tables[fields[24].strip()]=fields[25]
            logger.debug('Datamart table %s has total field %s. It will be recorded',fields[24].strip(),fields[25].strip())

    for key, value in datamart_tables.iteritems():
        temp = [key,value]
        result.append(temp)

    logger.info('End running check_total_datamart_table_field_number on file %s%s with max field %i.',input_directory,input_file,max_datamart_fields)
    return result


#2 inconsistence field selection between dynamic table and datamart table, datamart has less fields
def check_inconsistent_datamart_table_field(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_inconsistent_datamart_table_field on file %s%s.',input_directory,input_file)

    result=[['Datamart table has less fields than dynamic table fields']]
    result.append(['Datamart table name','Field count', 'Dynamic table name','Category','Dynamic table field'])
    datamart_tables = dict()

    for line in raw_file:
        fields = line.split(' | ')
        datamart_table_name = fields[24].strip()
        dynamic_table_name = fields[26].strip()

        if datamart_table_name.strip()<>'' and dynamic_table_name<>'':
            datamart_table_field_count = int(fields[25])
            dynamic_table_category = fields[27].strip()
            dynamic_table_field_count = int(fields[29])
            if datamart_table_field_count < dynamic_table_field_count :
                datamart_tables[datamart_table_name]=[datamart_table_name,str(datamart_table_field_count),dynamic_table_name,dynamic_table_category,str(dynamic_table_field_count)]
                logger.debug('Datamart table %s (with %i) has less field than dynamic table %s (with %i). It will be recorded',
                             datamart_table_name,datamart_table_field_count, dynamic_table_name,dynamic_table_field_count)

    for key, value in datamart_tables.iteritems():
        temp = value
        result.append(temp)

    logger.info('End running check_inconsistent_datamart_table_field on file %s%s.',input_directory,input_file)
    return result


#3 If any index defined, otherwise need to add indeices to it
def check_index(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_index on file %s%s.',input_directory,input_file)

    result=[['Following Datamart table dose not have index']]
    result.append(['Datamart table name','Index count'])
    datamart_tables = dict()

    for line in raw_file:
        fields = line.split(' | ')
        datamart_table_name = fields[24].strip()
        if datamart_table_name<>'':
            datamart_index = fields[19].strip()
            if datamart_index == '' :
                datamart_tables[datamart_table_name]= '0'
            logger.debug('Datamart table %s do not have any index.',datamart_table_name)

    for key, value in datamart_tables.iteritems():
        temp = [key,value]
        result.append(temp)

    logger.info('End running check_index on file %s%s.',input_directory,input_file)
    return result

def run():
    #define directories
    input_directory=os.getcwd()+'\Input\\'
    output_directory=os.getcwd()+'\Output\\'
    sql_directory=os.getcwd()+'\SQLs\\'
    property_directory=os.getcwd()+'\\properties\\'
    log_directory =os.getcwd()+'\Logs\\'

    #define sql files
    query_dm_sql='query_dm_config.sql'

    #define input files
    dm_config_file = 'source.csv'

    #define property files
    parameter_file='parameters.txt'
    mxDbsource_file='dbsource.mxres'

    #define output file
    final_result_file = 'analyze_datamart_table.xls'

    #define log file
    log_file = 'datamart_table_analysis.log'

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
    max_datamart_fields = config.getint('datamart table', 'max_number_fields')
    reload_data = config.getboolean('general', 'reload_data')

    log_level = config.get('log', 'log_level')
    initialize_log(log_level,log_directory+log_file)

    logger = logging.getLogger(__name__)
    logger.info('Start to run datamart_table_analysis.py.')

    if reload_data is True:
        logger.info('Start to execute SQL to load data from DB')
        #prepare connection string
        db_util = db_utility(log_level,log_directory+log_file)
        connectionString = db_util.load_dbsourcefile(property_directory + mxDbsource_file)

        #prepare datamart configuration SQLs to be run
        sqlfile = open(sql_directory+query_dm_sql, 'r+')
        sqlString= ''
        for line in sqlfile:
            sqlString = sqlString + line

        #prepare sql paramaters, the paramaters are defined according to MX format @:paramater_name:N/D/C
        sql_paramters = dict()

        #dump file
        db_util.dump_output(sqlString, None, connectionString, input_directory + dm_config_file)

    #create io_class
    io_util= io_utility(log_level,log_directory+log_file)

    #workbook for output result
    work_book = Workbook()

    #check Total number of dynamic tables fields for each dynamic table.
    result=check_total_datamart_table_field_number(input_directory,dm_config_file,max_datamart_fields)
    work_sheet_name='Field_Check'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #2 inconsistence field selection between dynamic table and datamart table
    result=check_inconsistent_datamart_table_field(input_directory,dm_config_file)
    work_sheet_name='Field_Inconsistent'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #3 datamart table shall have at least 1 index
    result=check_index(input_directory,dm_config_file)
    work_sheet_name='No_Index_Table'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)


    #output the work_book
    io_util.save_workbook(work_book,output_directory+final_result_file)
    logger.info('End running datamart_table_analysis.py.')

if __name__ == "__main__":
    run()