__author__ = 'ywang'


import cx_Oracle
import ConnectDB
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

def initialize_log(self, log_level=None, log_path='Logs\\'):
    self.logger = logging.getLogger(__name__)
    self.logger.setLevel(logging.DEBUG)

    # create a file handler
    handler = logging.handlers.RotatingFileHandler(log_path + 'dynamic_table_analysis.log', maxBytes=1024)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if log_level is not None:
        handler.setLevel(log_level)
    else:
        handler.setLevel(self.log_level)

    # add the handlers to the logger
    self.logger.addHandler(handler)


def set_log_level(self, log_level):
    for handler in self.logger.handlers:
        if log_level is not None:
            handler.setLevel(log_level)
        else:
            handler.setLevel(self.log_level)


# Total number of dynamic tables fields for each dynamic table. If more than 100, list out as red, if it is more than 50
def check_total_dynamic_table_field_number(input_directory,input_file, max_dynamic_number_fields) :
    raw_file= open(input_directory+input_file, 'r')
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

    return result

#	2. Number of horizontal fields. List more than 10 horizontal fields
def check_total_dynamic_table_horizontal_field_number(input_directory,input_file,max_dynamic_number_hfields) :
    raw_file= open(input_directory+input_file, 'r')
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

    return result

#	3. Check if any *TBLFIELD, *TABLE is used
def check_total_dynamic_table_db_access_horizontal_field_number(input_directory,input_file,max_dynamic_number_db_access_hfields) :
    raw_file= open(input_directory+input_file, 'r')
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

    return result


#	4. Check if sensitivy flag is disabled for dynamic table that not select any S_* fields
def check_compute_sensitivity_flag(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')
    result=[['Dynamic tables which sensitivity compute flag can be disabled']]
    result.append(['Dynamic table name','Category'])

    for line in raw_file:
        fields = line.split(' | ')
        result.append([fields[0].strip(),fields[1].strip()])
    return result


if __name__ == "__main__":
    #define directories
    input_directory=os.getcwd()+'\Input\\'
    output_directory=os.getcwd()+'\Output\\'
    sql_directory=os.getcwd()+'\SQLs\\'
    property_directory=os.getcwd()+'\\properties\\'

    #define sql files
    query_dm_sql='query_dm_config.sql'
    query_sensi_sql='query_sensitivity_flag.sql'

    #define input files
    dm_config_file = 'source.csv'
    sensi_file='computer_sensitivity_check.csv'

    #define property files
    parameter_file='parameters.txt'
    mxDbsource_file='dbsource.mxres'

    #define output file
    final_result_file = 'analyze_dynamic_table.xls'

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
    max_dynamic_number_fields = config.getint('dynamic table', 'max_number_fields')
    max_dynamic_number_hfields = config.getint('dynamic table', 'max_number_h_fields')
    max_dynamic_number_db_access_hfields = config.getint('dynamic table', 'max_number_db_access_h_fields')

    #prepare conncection string
    connectionString = ConnectDB.loadMXDBSourcefile(property_directory + mxDbsource_file)

    #Generate input files
    sqlfile1 = open(sql_directory+query_dm_sql, 'r+')
    #generate_raw_file(connectionString,sqlfile1,input_directory,dm_config_file)

    sqlfile2 = open(sql_directory+query_sensi_sql, 'r+')
    #generate_raw_file(connectionString,sqlfile2,input_directory,sensi_file)


    #prepare connection string
    db_util = db_utility()
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

    #create io_class
    io_util= io_utility()

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
    work_sheet_name='Sensi_flag_Check'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #output the work_book
    io_util.save_workbook(work_book,output_directory+final_result_file)



