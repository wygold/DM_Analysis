__author__ = 'ywang'


import string
import xlrd
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


# Total number of dynamic tables fields for each dynamic table. If more than 100, list out as red, if it is more than 50
def check_total_dynamic_table_field_number(input_directory,input_file, max_dynamic_number_fields) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_total_dynamic_table_field_number on file %s%s with max field %i.',input_directory,input_file,max_dynamic_number_fields)

    result=[['Number of Dynamic table fields that exceeds '+str(max_dynamic_number_fields)]]
    result.append(['Dynamic table name','Category','Dynamic table type','Field count'])
    previous_dynamic_tables = []
    for line in raw_file:
        fields = line.split(' | ')

        if fields[29].strip()<>'' and int(fields[29])> max_dynamic_number_fields :
            #    result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
            if (fields[26].strip()+fields[27].strip()) not in previous_dynamic_tables :
                result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
                previous_dynamic_tables.append(fields[26].strip()+fields[27].strip())
                logger.debug('Dynamic table %s@%s has total field %s. It will be recorded',fields[26].strip(),fields[27].strip(),fields[29].strip())
    logger.info('End running check_total_dynamic_table_field_number on file %s%s with max field %i.',input_directory,input_file,max_dynamic_number_fields)
    return result

#	2. Number of horizontal fields. List more than 10 horizontal fields
def check_total_dynamic_table_horizontal_field_number(input_directory,input_file,max_dynamic_number_hfields) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_total_dynamic_table_horizontal_field_number on file %s%s with max field %i.',input_directory,input_file,max_dynamic_number_hfields)

    result=[['Number of Dynamic table horizontal fields that exceeds '+str(max_dynamic_number_hfields)]]
    result.append(['Dynamic table name','Category','Dynamic table type','Horizontal Field count'])
    previous_dynamic_tables = []
    for line in raw_file:
        fields = line.split(' | ')

        if fields[30].strip()<>'' and int(fields[30])>max_dynamic_number_hfields :
        #    result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
            if (fields[26].strip()+fields[27].strip()) not in previous_dynamic_tables :
                result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[30].strip()])
                previous_dynamic_tables.append(fields[26].strip()+fields[27].strip())

    logger.info('End running check_total_dynamic_table_horizontal_field_number on file %s%s with max field %i.',input_directory,input_file,max_dynamic_number_hfields)
    return result

#	3. Check if any *TBLFIELD, *TABLE is used
def check_total_dynamic_table_db_access_horizontal_field_number(input_directory,input_file,max_dynamic_number_db_access_hfields) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_total_dynamic_table_db_access_horizontal_field_number on file %s%s with max field %i.',input_directory,input_file,max_dynamic_number_db_access_hfields)

    result=[['Number of Dynamic table horizontal fields that access database which exceeds '+str(max_dynamic_number_db_access_hfields)]]
    result.append(['Dynamic table name','Category','Dynamic table type','Direct DB access Parser function used times'])
    previous_dynamic_tables = []
    for line in raw_file:
        fields = line.split(' | ')

        if fields[31].strip()<>'' and int(fields[31])>max_dynamic_number_db_access_hfields :
        #    result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
            if (fields[26].strip()+fields[27].strip()) not in previous_dynamic_tables :
                result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[31].strip()])
                previous_dynamic_tables.append(fields[26].strip()+fields[27].strip())

    logger.info('End running check_total_dynamic_table_db_access_horizontal_field_number on file %s%s with max field %i.',input_directory,input_file,max_dynamic_number_db_access_hfields)
    return result


#	4. Check if sensitivy flag is disabled for dynamic table that not select any S_* fields
def check_compute_sensitivity_flag(input_directory,input_file) :

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_compute_sensitivity_flag on file %s%s.',input_directory,input_file)

    raw_file= open(input_directory+input_file, 'r')
    result=[['Dynamic tables which sensitivity compute flag can be disabled']]
    result.append(['Dynamic table name','Category'])

    for line in raw_file:
        fields = line.split(' | ')
        logger.debug('Dynamic table %s under category %s is setting sensitivy flag incorreclty.',fields[0].strip(),fields[1].strip())
        result.append([fields[0].strip(),fields[1].strip()])

    logger.info('End running check_compute_sensitivity_flag on file %s%s.',input_directory,input_file)
    return result

#	5. Check if simulation viweer used is correct set to consolidated or detailed mode
def check_sim_view_mode(input_directory,source_file, simulation_context_file) :

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_sim_view_mode on file %s%s and %s.',input_directory,source_file,simulation_context_file)

    dynamic_tables = dict()
    sim_context = dict()
    result = []

    dm_config_file= open(input_directory+source_file, 'r')
    sim_context_file = open(input_directory+simulation_context_file, 'r')

    for line in dm_config_file:
        fields = line.split(' | ')
        if fields[28].strip() == 'Simulation':
            logger.debug('Found dynamic table %s under %s with viewer %s as %s',fields[26].strip(), fields[27].strip(), fields[42].strip(), fields[33].strip())
            dynamic_tables[fields[26].strip() + fields[27].strip()]=[fields[26].strip(), fields[27].strip(), fields[42].strip(), fields[33].strip()]

    #if simulation is only for detailed: mode is 1
    #if simulation is only for consolidated: mode is 2
    #if simulation is for both detailed: and consolidated:mode is 3

    for line in sim_context_file:
        fields = line.split(' | ')
        if fields[0].strip() == 'Detailed simulation' or fields[0].strip() == 'Consolidated simulation':
            if fields[1].strip() in sim_context.keys() :
                sim_context[fields[1].strip()]=[fields[0].strip(),3]
            else :
                if fields[0].strip() == 'Detailed simulation':
                    sim_context[fields[1].strip()]=[fields[0].strip(),1]
                if fields[0].strip() == 'Consolidated simulation':
                    sim_context[fields[1].strip()]=[fields[0].strip(),2]

    for dynamic_table_name in dynamic_tables.keys():
        logger.debug('Dynamic table key is %s',dynamic_table_name)
        logger.debug('Dynamic table viewer is %s',dynamic_tables[dynamic_table_name][2])
        if dynamic_tables[dynamic_table_name][2] in sim_context.keys() :
            if sim_context[dynamic_tables[dynamic_table_name][2]]==1 and dynamic_tables[dynamic_table_name][3]=='Consolidated DBF'\
                or sim_context[dynamic_tables[dynamic_table_name][2]]==2 and dynamic_tables[dynamic_table_name][3]=='Detailed DBF':
                result.append(dynamic_tables[dynamic_table_name][2])
        else :
            logger.warning('sim_context_file does not have simulation viewer %s',dynamic_tables[dynamic_table_name][2])
    final_result=[['Dynamic table with wrong build on mode']]
    final_result.append(['Dynamic table name','Category','Simulation name','Build on mode'])

    logger.info('End running check_sim_view_mode on file %s%s and %s.',input_directory,source_file,simulation_context_file)
    return final_result

if __name__ == "__main__":
    #define directories
    input_directory=os.getcwd()+'\Input\\'
    output_directory=os.getcwd()+'\Output\\'
    sql_directory=os.getcwd()+'\SQLs\\'
    property_directory=os.getcwd()+'\\properties\\'
    log_directory =os.getcwd()+'\Logs\\'

    #define sql files
    query_dm_sql='query_dm_config.sql'
    query_sensi_sql='query_sensitivity_flag.sql'
    query_simulation_context_sql = 'query_simulation_context.sql'

    #define input files
    dm_config_file = 'source.csv'
    sensi_file='computer_sensitivity_check.csv'
    sim_file='simulation_context.csv'

    #define property files
    parameter_file='parameters.txt'
    mxDbsource_file='dbsource.mxres'

    #define output file
    final_result_file = 'analyze_dynamic_table.xls'

    #define log file
    log_file = 'dynamic_table_analysis.log'

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
    max_dynamic_number_fields = config.getint('dynamic table', 'max_number_fields')
    max_dynamic_number_hfields = config.getint('dynamic table', 'max_number_h_fields')
    max_dynamic_number_db_access_hfields = config.getint('dynamic table', 'max_number_db_access_h_fields')
    reload_data = config.getboolean('general', 'reload_data')

    log_level = config.get('log', 'log_level')
    initialize_log(log_level,log_directory+log_file)

    logger = logging.getLogger(__name__)
    logger.info('Start to run dynamic_table_analysis.py.')

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

        #prepare sensitivities SQLs to be run
        sqlfile = open(sql_directory+query_sensi_sql, 'r+')
        sqlString= ''
        for line in sqlfile:
            sqlString = sqlString + line

        #prepare sql paramaters, the paramaters are defined according to MX format @:paramater_name:N/D/C
        sql_paramters = dict()

        #dump file
        db_util.dump_output(sqlString, None, connectionString, input_directory + sensi_file)

        #prepare simulation context SQLs to be run
        sqlfile = open(sql_directory+query_simulation_context_sql, 'r+')
        sqlString= ''
        for line in sqlfile:
            sqlString = sqlString + line

        #prepare sql paramaters, the paramaters are defined according to MX format @:paramater_name:N/D/C
        sql_paramters = dict()

        #dump file
        db_util.dump_output(sqlString, None, connectionString, input_directory + sim_file)

        logger.info('End executing SQL to load data from DB')

    #create io_class
    io_util= io_utility(log_level,log_directory+log_file)

    #workbook for output result
    work_book = Workbook()

    #check Total number of dynamic tables fields for each dynamic table.
    result=check_total_dynamic_table_field_number(input_directory,dm_config_file,max_dynamic_number_fields)
    work_sheet_name='Field_Check'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #check Number of horizontal fields
    result=check_total_dynamic_table_horizontal_field_number(input_directory,dm_config_file, max_dynamic_number_hfields)
    work_sheet_name='H_Field_Check'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #Check horizontal fields with *TBLFIELD and *TABLE
    result=check_total_dynamic_table_db_access_horizontal_field_number(input_directory,dm_config_file, max_dynamic_number_db_access_hfields)
    work_sheet_name='H_DB_Field_Check'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #check sensitivity flag can be disabled
    result=check_compute_sensitivity_flag(input_directory,sensi_file)
    work_sheet_name='Sensi_Flag_Check'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #check build on mode is correctly set
    result=check_sim_view_mode(input_directory,dm_config_file,sim_file)
    work_sheet_name='Build_Mode_Check'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #output the work_book
    io_util.save_workbook(work_book,output_directory+final_result_file)
    logger.info('End running dynamic_table_analysis.py.')


