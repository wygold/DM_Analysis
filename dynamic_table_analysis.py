__author__ = 'ywang'


from xlwt import *
import ConfigParser
import os
from db_utility import db_utility
from io_utility import io_utility
from property_utility import property_utility
import logging
from logging import handlers
from operator import itemgetter, attrgetter, methodcaller

logger = ''


def initialize_log( log_level = 'INFO', log_file =None ):
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
    result.append(['Dynamic table name','Category','Dynamic table type','Direct DB access Parser functions (*TBLFIELD, *TABLE) used times'])
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
    result=[['Dynamic tables''s sensitivity flag can be disabled']]
    result.append(['    Dynamic table name     ','Category'])

    for line in raw_file:
        fields = line.split(' | ')
        logger.debug('Dynamic table %s under category %s is setting sensitivy flag incorreclty.',fields[0].strip(),fields[1].strip())
        result.append([fields[0].strip(),fields[1].strip()])

    logger.info('End running check_compute_sensitivity_flag on file %s%s.',input_directory,input_file)
    return result

#	5. Check if simulation viewer used is correct set to consolidated or detailed mode with dynamic table build on
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
            logger.debug('Simulation viewer context for viewer %s is %s, its build on is %s',
                         dynamic_tables[dynamic_table_name][2],sim_context[dynamic_tables[dynamic_table_name][2]][1],dynamic_tables[dynamic_table_name][3] )
            if (sim_context[dynamic_tables[dynamic_table_name][2]][1]==1 and dynamic_tables[dynamic_table_name][3]=='Consolidated DBF')\
                or (sim_context[dynamic_tables[dynamic_table_name][2]][1]==2 and dynamic_tables[dynamic_table_name][3]=='Detailed DBF'):
                logger.debug('Problem dynamic_tables is %s ',dynamic_tables[dynamic_table_name][2])
                result.append(dynamic_tables[dynamic_table_name])
        else :
            logger.warning('sim_context_file does not have simulation viewer %s',dynamic_tables[dynamic_table_name][2])
    final_result=[['Dynamic table with wrong build on mode']]
    final_result.append(['Dynamic table name','Category','Simulation name','Build on mode'])
    final_result.extend(result)

    logger.info('End running check_sim_view_mode on file %s%s and %s.',input_directory,source_file,simulation_context_file)
    return final_result

#summary of how dynamic table fields are referenced by datamart tables
def check_dynamic_table_field_reference_summary(input_directory,source_file) :

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_dynamic_table_field_reference_summary on file %s%s.',input_directory,source_file)

    table_fields = dict()

    dm_definition_file_point= open(input_directory+source_file, 'r')

    #retrieve table field name and its total number referenced
    for line in dm_definition_file_point:
        fields = line.split(' | ')

        field_name= fields[0].strip()
        max_length= fields[1].strip()
        precision= fields[2].strip()
        data_type= fields[3].strip()
        table_name= fields[4].strip()
        dyn_table= fields[5].strip()
        dyn_table_category= fields[6].strip()
        dyn_table_type= fields[7].strip()

        print dyn_table_type

        key = field_name + ' | ' + dyn_table_type

        if not table_fields.has_key(key):
            #table_fields[field_name]=[table_name]
            table_fields[key] = 1
        else:
            #table_fields[field_name].append(table_name)
            table_fields[key] = table_fields[key] + 1

    final_result=[['Summary of dynamic table field reference']]
    final_result.append(['Dynamic table field','Dynamic table type', '# of reference'])

    result=[]

    for field_key, table_count in table_fields.iteritems():
        field_name, dyn_table_type=field_key.split(' | ')
        temp = [field_name,dyn_table_type,table_count]
        result.append(temp)

    #sort the result
    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(2),reverse=True)

    final_result.extend(sorted_result)

    logger.info('End running check_dynamic_table_field_reference_summary on file %s%s.',input_directory,source_file)
    return final_result

#detail of how dynamic table fields are referenced by datamart tables
def check_dynamic_table_field_reference_detail(input_directory,source_file) :

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_dynamic_table_field_reference_summary on file %s%s.',input_directory,source_file)

    dm_definition_file= open(input_directory+source_file, 'r')

    table_fields = dict()

    final_result=[['Summary of dynamic table field reference']]
    final_result.append(['Dynamic table field','Dynamic table category','Dynamic table','Dynamic table type','Datamart table'])

    result=[]

    for line in dm_definition_file:
        fields = line.split(' | ')

        field_name= fields[0].strip()
        max_length= fields[1].strip()
        precision= fields[2].strip()
        data_type= fields[3].strip()
        table_name= fields[4].strip()
        dyn_table= fields[5].strip()
        dyn_table_category= fields[6].strip()
        dyn_table_type= fields[7].strip()


        if not table_fields.has_key(field_name):
            table_fields[field_name]=[[dyn_table_category,dyn_table,dyn_table_type,table_name]]
        else:
            table_fields[field_name].append([dyn_table_category,dyn_table,dyn_table_type,table_name])

    for field_name, table_definition in table_fields.iteritems():
        for table in table_definition:
            dyn_table_category,dyn_table,dyn_table_type,table_name= table
            temp = [field_name,dyn_table_category,dyn_table,dyn_table_type,table_name]
            result.append(temp)

    #sort the result
    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(0,1),reverse=False)

    final_result.extend(sorted_result)

    logger.info('End running check_dynamic_table_field_reference_summary on file %s%s.',input_directory,source_file)
    return final_result

def run(reload_check_button_status=None,log_dropdown_status=None):

    #define properties folder
    property_directory=os.getcwd()+'\\properties\\'
    parameter_file='parameters.txt'

    property_util = property_utility()
    parameters = property_util.parse_property_file(property_directory,parameter_file)

    #define sql files
    query_dm_sql='query_dm_config.sql'
    query_sensi_sql='query_sensitivity_flag.sql'
    query_simulation_context_sql = 'query_simulation_context.sql'
    query_dm_defintion_sql = 'query_dm_definition.sql'

    #define input files
    dm_config_file = 'source.csv'
    sensi_file='computer_sensitivity_check.csv'
    sim_file='simulation_context.csv'
    dm_defintion_file = 'dm_definition.csv'

    #define property files
    mxDbsource_file=parameters['database']['mx_db_config_file']

    #define output file
    final_result_file = parameters['dynamic table']['output_file_name']

    #define log file
    log_file = parameters['dynamic table']['log_file_name']

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
    max_dynamic_number_fields = config.getint('dynamic table', 'max_number_fields')
    max_dynamic_number_hfields = config.getint('dynamic table', 'max_number_h_fields')
    max_dynamic_number_db_access_hfields = config.getint('dynamic table', 'max_number_db_access_h_fields')
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
    logger.info('Start to run dynamic_table_analysis.py.')

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


        #prepare dm defintion SQLs to be run
        sqlfile = open(sql_directory+query_dm_defintion_sql, 'r+')
        sqlString= ''
        for line in sqlfile:
            sqlString = sqlString + line

        #prepare sql paramaters, the paramaters are defined according to MX format @:paramater_name:N/D/C
        sql_paramters = dict()

        #dump file
        db_util.dump_output(sqlString, None, connectionString, input_directory + dm_defintion_file)

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

    #summary of how dynamic table fields are referenced by datamart tables
    result=check_dynamic_table_field_reference_summary(input_directory,dm_defintion_file)
    work_sheet_name='Field_Reference_Summary'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)


    #detail of how dynamic table fields are referenced by datamart tables
    result=check_dynamic_table_field_reference_detail(input_directory,dm_defintion_file)
    work_sheet_name='Field_Reference_Detail'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)


    #output the work_book
    io_util.save_workbook(work_book,output_directory+final_result_file)
    logger.info('End running dynamic_table_analysis.py.')

if __name__ == "__main__":
    run()