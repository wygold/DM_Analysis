__author__ = 'ywang'


from xlwt import *
import ConfigParser
import os
from db_utility import db_utility
from io_utility import io_utility
import logging
from logging import handlers
from collections import OrderedDict
from property_utility import property_utility
logger = ''


def initialize_log( log_level = 'INFO', log_file = None):
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    if logger.handlers == []:
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


#1 Total number of datamart tables fields for each datamart table. If more than 100, list out as red, if it is more than 50
def check_total_datamart_table_field_number(input_directory,input_file, max_datamart_fields) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_total_datamart_table_field_number on file %s%s with max field %i.',input_directory,input_file,max_datamart_fields)

    result=[['Datamart table fields exceeds '+str(max_datamart_fields)]]
    result.append(['    Datamart table name    ','Field count'])
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

    result=[['Datamart tables with no index']]
    result.append(['  Datamart table name  ','Index count'])
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


#create the content page
def create_content_page(sheet_names,work_books_content):

    logger = logging.getLogger(__name__)
    logger.info('Start to run create_content_page for %s sheets.',len(sheet_names))

    result = [['Sheets:']]

    i = 1

    for sheet_name in sheet_names:
        work_sheet_content=work_books_content[sheet_name]
        work_sheet_description = work_sheet_content[0][0]
        result.append([sheet_name,work_sheet_description])
        i = i + 1

    logger.info('End running create_content_page for %s sheets.',len(sheet_names))
    return result


def run(reload_check_button_status=None,log_dropdown_status=None):
    #define properties folder
    property_directory=os.getcwd()+'\\properties\\'
    parameter_file='parameters.txt'

    property_util = property_utility()
    parameters = property_util.parse_property_file(property_directory,parameter_file)

    #define sql files
    query_dm_sql='query_dm_config.sql'

    #define input files
    dm_config_file = 'source.csv'

    #define property files
    mxDbsource_file=parameters['database']['mx_db_config_file']

    #define output file
    final_result_file = parameters['datamart table']['output_file_name']

    #define log file
    log_file = parameters['datamart table']['log_file_name']


    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
    max_datamart_fields = config.getint('datamart table', 'max_number_fields')
    reload_data = config.getboolean('general', 'reload_data')

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
    logger.info('Start to run datamart_table_analysis.py.')

    if (reload_check_button_status is None and reload_data) or (reload_check_button_status):
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
    work_books_content = OrderedDict()
    work_sheet_names = []

    #check Total number of dynamic tables fields for each dynamic table.
    result=check_total_datamart_table_field_number(input_directory,dm_config_file,max_datamart_fields)
    work_sheet_name='Fields_Check'
    work_books_content[work_sheet_name]=result
    work_sheet_names.append(work_sheet_name)

    #2 inconsistence field selection between dynamic table and datamart table
    result=check_inconsistent_datamart_table_field(input_directory,dm_config_file)
    work_sheet_name='#_Fields_REP_Vs_Dyn'
    work_books_content[work_sheet_name]=result
    work_sheet_names.append(work_sheet_name)

    #3 datamart table shall have at least 1 index
    result=check_index(input_directory,dm_config_file)
    work_sheet_name='No_Indexed_Tables'
    work_books_content[work_sheet_name]=result
    work_sheet_names.append(work_sheet_name)

    #create content sheet
    result=create_content_page(work_sheet_names,work_books_content)
    work_sheet_name='Content'
    work_book=io_util.add_content_worksheet(result,work_book, work_sheet_name)

    sheet_sequence = 0
    for work_sheet_name, result in work_books_content.iteritems():
        preview_sheet= ''
        next_sheet = ''
        if sheet_sequence == 0 :
            preview_sheet='Content'
        else:
            preview_sheet = work_sheet_names[sheet_sequence-1]

        if sheet_sequence == len(work_sheet_names) - 1:
            next_sheet = None
        else:
            next_sheet = work_sheet_names[sheet_sequence + 1]

        work_book=io_util.add_worksheet(result,work_book, work_sheet_name,False, preview_sheet,next_sheet)

        sheet_sequence = sheet_sequence + 1


    #output the work_book
    io_util.save_workbook(work_book,output_directory+final_result_file)
    logger.info('End running datamart_table_analysis.py.')

if __name__ == "__main__":
    run()