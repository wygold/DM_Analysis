__author__ = 'ywang'

from xlwt import *
import ConfigParser
import os
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


#1 Check if batch of feeder with same label of data has same historization and data computed by several batch and Data(published/private)
def check_dataset_consistency(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_dataset_consistency on file %s%s.',input_directory,input_file)

    result=[['Batch of feeder has possible wrong dataset settings were marked as inconsistent in last column']]
    result.append(['Batch of feeder','Label of Data','Historisation','Private','Data Computed by Several Batch','Setting is correct'])
    batch_feeders_label = dict()


    for line in raw_file:
        fields = line.split(' | ')

        if fields[2].strip()<>'' and fields[14].strip() <>'' :
            data_label = fields[14].strip()

            if batch_feeders_label.has_key(data_label):
                batch_feeders=batch_feeders_label[data_label]
                logger.debug('Batch of feeder''s label is %s.',fields[14].strip())
                batch_feeders[fields[2].strip()]=[data_label,fields[10].strip(),fields[13].strip(),fields[11].strip()]
                logger.debug('Batch of feeder %s is added.',fields[2].strip())
                batch_feeders_label[fields[14].strip()]=batch_feeders
            else:
                batch_feeders = dict()
                logger.debug('New label of data found: %s.',data_label)
                batch_feeders[fields[2].strip()]=[data_label,fields[10].strip(),fields[13].strip(),fields[11].strip()]
                batch_feeders_label[data_label]=batch_feeders

    for data_label, batch_feeders in batch_feeders_label.iteritems():
        logger.debug('Checking: %s.',data_label)
        initial_historisation = None
        initial_several_batch = None
        initial_user_type = None

        for batch_name, batch_contents in batch_feeders.iteritems():
            current_historisation=batch_contents[0]
            current_several_batch =batch_contents[1]
            current_user_type = batch_contents[2]
            logger.debug('Current data set %s with historization: %s, Dataset shared: %s, User type: %s.',
                         data_label, current_historisation, current_several_batch, current_user_type )

            if initial_historisation is None :
                initial_historisation = current_historisation
                initial_several_batch = current_several_batch
                initial_user_type = current_user_type
                logger.debug('Set initial data set %s with historization: %s, Dataset shared: %s, User type: %s.',
                         data_label, initial_historisation, initial_several_batch, initial_user_type )

            if initial_historisation <> current_historisation or \
                            initial_several_batch <> current_several_batch or \
                            initial_user_type <> current_user_type :
                batch_contents.append("Inconsistent")
                logger.debug('Found inconsistent batch of feeder: %s',batch_name)
                batch_feeders[batch_name] = batch_contents
            else :
                batch_contents.append("OK")
                batch_feeders[batch_name] = batch_contents

    for data_label, batch_feeders in batch_feeders_label.iteritems():
        for batch_name, batch_contents in batch_feeders.iteritems():
            temp = [batch_name]+batch_contents
            result.append(temp)

    logger.info('End running check_total_datamart_table_field_number on file %s%s.',input_directory,input_file)
    return result

#2 Check if same feeder are used in different batch feeder
def check_duplicate_of_feeders(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_duplicate_of_feeders in different batch of feeder on file %s%s.',input_directory,input_file)

    result=[['Feeder that definded in multiple batches']]
    result.append(['Feeder','Batch of feeder','Last Execution Date'])

    feeders = dict()
    batch_execution_time = dict()

    for line in raw_file:
        fields = line.split(' | ')

        object_type=fields[23].strip()

        if object_type == 'FEEDERS' :
            feeder_name=fields[15].strip()
            batch_feeder_name=fields[2].strip()
            batch_last_execution_date = fields[4].strip()
            logger.debug('Checking feeder: %s, batch feeder: %s, last excution time: %s.',feeder_name,batch_feeder_name,batch_last_execution_date)
            if not feeders.has_key(feeder_name) :
                feeders[feeder_name]=[batch_feeder_name]
            else :
                if batch_feeder_name not in feeders[feeder_name] and batch_feeder_name<>'':
                    feeders[feeder_name].append(batch_feeder_name)
            batch_execution_time[batch_feeder_name]=batch_last_execution_date


    for feeder_name, feeder_content in feeders.iteritems():
        logger.debug('Number of batch feeders is %i that has same feeder %s.',len(feeder_content),feeder_name)
        if len(feeder_content) > 1 :
            for batch_feeder_name in feeder_content :
                if batch_feeder_name <> '':
                    temp = [feeder_name, batch_feeder_name, batch_execution_time[batch_feeder_name]]
                    result.append(temp)

    logger.info('End running check_duplicate_of_feeders on file %s%s.',input_directory,input_file)
    return result


#2.1 Check if same datamart are used in different single feeder
def check_duplicate_of_dm_table(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_duplicate_of_dm_table in different batch of feeder on file %s%s.',input_directory,input_file)

    result=[['Datamart tables that definded in multiple single feeders']]
    result.append(['DM Table Name','Feeder name','Last Execution Date'])

    dm_tables = dict()
    feeder_execution_time = dict()

    for line in raw_file:
        fields = line.split(' | ')

        object_type=fields[23].strip()

        if object_type == 'FEEDERS' :
            dm_tables_name=fields[24].strip()
            feeder_name=fields[15].strip()
            feeder_last_execution_date = fields[17].strip()
            logger.debug('Checking dm table: %s, feeder: %s, last excution time: %s.',dm_tables_name,feeder_name,feeder_last_execution_date)
            if not dm_tables.has_key(dm_tables_name) :
                dm_tables[dm_tables_name]=[feeder_name]
            else :
                if feeder_name not in dm_tables[dm_tables_name] and feeder_name<>'':
                    dm_tables[dm_tables_name].append(feeder_name)
            feeder_execution_time[feeder_name]=feeder_last_execution_date

    for dm_tables_name, dm_tables_content in dm_tables.iteritems():
        logger.debug('Number of feeders is %i that has same datamart table %s.',len(dm_tables_content),dm_tables_name)
        if len(dm_tables_content) > 1 :
            for feeder_name in dm_tables_content :
                if feeder_name <> '':
                    temp = [dm_tables_name, feeder_name, feeder_execution_time[feeder_name]]
                    result.append(temp)

    logger.info('End running check_duplicate_of_dm_table on file %s%s.',input_directory,input_file)
    return result

#2.2 Check if same batch feeder are defined in different processing script
def check_duplicate_of_batch_feeder(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_duplicate_of_batch_feeder in different batch of feeder on file %s%s.',input_directory,input_file)

    result=[['Batch of Feeder that definded in multiple processing scripts']]
    result.append(['Batch of Feeder','Processing Script'])

    batch_feeders = dict()

    for line in raw_file:
        fields = line.split(' | ')

        object_type=fields[23].strip()

        if object_type == 'FEEDERS' :
            batch_feeder_name=fields[2].strip()
            processing_script_name=fields[0].strip()
            logger.debug('Checking dm table: %s, feeder: %s.',batch_feeder_name,processing_script_name)
            if not batch_feeders.has_key(batch_feeder_name) :
                batch_feeders[batch_feeder_name]=[processing_script_name]
            else :
                if processing_script_name not in batch_feeders[batch_feeder_name] and processing_script_name<>'':
                    batch_feeders[batch_feeder_name].append(processing_script_name)


    for batch_feeder_name, batch_feeder_content in batch_feeders.iteritems():
        if len(batch_feeder_content) > 1 :
            for processing_script_name in batch_feeder_content :
                if processing_script_name <> '':
                    temp = [batch_feeder_name, processing_script_name]
                    result.append(temp)

    logger.info('End running check_duplicate_of_batch_feeder on file %s%s.',input_directory,input_file)
    return result

#2.0 Give summary of duplicate checking
def check_duplicate_summary(input_directory,input_file) :
    logger = logging.getLogger(__name__)
    logger.info('Start to run check_duplicate_summary in different batch of feeder on file %s%s.',input_directory,input_file)

    result=[['A summary of multi-referenced dm objects.']]

    logger.info('Process how datamart tables are refernced by feeders')
    result.append(['Name of Datamart table','# of Referenced feeders'])

    dm_tables_result=check_duplicate_of_dm_table(input_directory,input_file)

    dm_tables=dict()
    for i in range(2,len(dm_tables_result)):
        dm_table_name=dm_tables_result[i][0]
        if not dm_tables.has_key(dm_table_name):
            dm_tables[dm_table_name]=1
        else:
            dm_tables[dm_table_name] = dm_tables[dm_table_name]+1

    for dm_table_name, feeder_counter in dm_tables.iteritems():
        temp = [dm_table_name, str(feeder_counter)]
        result.append(temp)
    result.append(['    ','     '])

    logger.info('Process how feeders are refernced by batch feeders')
    result.append(['Name of feeders','# of Referenced Batch feeders'])

    feeders_result=check_duplicate_of_feeders(input_directory,input_file)

    feeders=dict()
    for i in range(2,len(feeders_result)):
        feeder_name=feeders_result[i][0]
        if not feeders.has_key(feeder_name):
            feeders[feeder_name]=1
        else:
            feeders[feeder_name] = feeders[feeder_name]+1

    for feeder_name, batch_feeder_counter in feeders.iteritems():
        temp = [feeder_name, str(batch_feeder_counter)]
        result.append(temp)
    result.append(['    ','    '])

    logger.info('Process how batch feeders are refernced by processing scripts')
    result.append(['Name of batch feeders','# of Referenced Batch feeders'])

    batch_feeders_result=check_duplicate_of_batch_feeder(input_directory,input_file)

    batch_feeders=dict()
    for i in range(2,len(batch_feeders_result)):
        batch_feeder_name = batch_feeders_result[i][0]
        if not batch_feeders.has_key(batch_feeder_name):
            batch_feeders[batch_feeder_name]=1
        else:
            batch_feeders[batch_feeder_name] = batch_feeders[batch_feeder_name]+1

    for batch_feeder_name, processing_script_counter in batch_feeders.iteritems():
        temp = [batch_feeder_name, str(processing_script_counter)]
        result.append(temp)


    logger.info('End running check_duplicate_summary on file %s%s.',input_directory,input_file)
    return result

#3 Check scanner engine usage
def check_scanner_engine_usage(input_directory,input_file) :
    scanner_engine_enabled_dynamic_table = ['DYN_TRNRP_CS',
        'DYN_TRNRP_DT',
        'DYN_TRNRP_MK',
        'DYN_TRNRP_MV',
        'DYN_TRNRP_PL',
        'DYN_TRNRP_SV',
        'DYN_TRNRP_XG',
        'Simulation',
        'PL VAR']

    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_scanner_engine_usage for batch of feeder on file %s%s.',input_directory,input_file)

    result=[['Batch of feeders'' scanner engine usage']]
    result.append(['Batch of feeder','Dynamic table type','Scanner engine number'])

    engine_usage = dict()
    dynamic_table_types=dict()

    for line in raw_file:
        fields = line.split(' | ')
        dynamic_table_type=fields[28].strip()
        batch_feeder_name=fields[2].strip()
        engine_number =fields[12].strip()

        logger.debug('Checking batch feeder %s, dynamic table type %s, engine number %s ',batch_feeder_name,fields[27].strip(), engine_number)

        if dynamic_table_type in scanner_engine_enabled_dynamic_table and batch_feeder_name<>'' :
            engine_usage[batch_feeder_name]=engine_number
            dynamic_table_types[batch_feeder_name]=dynamic_table_type

    for batch_feeder_name, engine_number in engine_usage.iteritems():
        temp = [batch_feeder_name,dynamic_table_types[batch_feeder_name], engine_number]
        result.append(temp)

    logger.info('End running check_scanner_engine_usage on file %s%s.',input_directory,input_file)
    return result


#4. check number of feeders in a batch, shall not be too many!
def check_number_of_feeder_in_batch(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_number_of_feeder_in_batch for batch of feeder on file %s%s.',input_directory,input_file)

    result=[['Number of feeders in a batch of feeders']]
    result.append(['Batch of feeder','Number of Feeder'])

    batch_feeders=dict()

    for line in raw_file:
        fields = line.split(' | ')
        batch_feeder_name=fields[2].strip()
        feeder_name = fields[15].strip()

        logger.debug('Checking batch feeder %s, feeder mame %s',batch_feeder_name, feeder_name)

        if batch_feeder_name <>'' :
            if not batch_feeders.has_key(batch_feeder_name) :
                single_feeders=set()
                single_feeders.add(feeder_name)
                batch_feeders[batch_feeder_name]=single_feeders
                logger.debug('Add feeder %s into batch feeder %s',feeder_name,batch_feeder_name)
            else :
                single_feeders = batch_feeders[batch_feeder_name]
                single_feeders.add(feeder_name)
                batch_feeders[batch_feeder_name]=single_feeders
                logger.debug('Add feeder %s into batch feeder %s',feeder_name,batch_feeder_name)

    for batch_feeder_name, single_feeders in batch_feeders.iteritems():
        temp = [batch_feeder_name,str(len(single_feeders))]
        result.append(temp)

    logger.info('End running check_number_of_feeder_in_batch on file %s%s.',input_directory,input_file)
    return result

#5 check_filter_conflict between dynamic table default settings and global filter
def check_filter_conflict(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_filter_conflict for batch of feeder on file %s%s.',input_directory,input_file)

    result=[['Filter confilict between default filter and global filter']]
    result.append(['Dynamic table','Default filter 1', 'Default filter 2', 'Default filter 3','Default filter 4','Batch feeder','Global filter 1','Global filter 2','Global filter 3'])

    for line in raw_file:
        fields = line.split(' | ')
        dynamic_table_name = fields[26].strip()
        #default_filter_1=fields[37].strip()
        default_filter_2=fields[38].strip()
        default_filter_3=fields[39].strip()
        default_filter_4=fields[40].strip()
        default_filter_5=fields[41].strip()

        batch_feeder_name=fields[2].strip()
        global_filter1=fields[7].strip()
        global_filter2=fields[8].strip()
        global_filter3=fields[9].strip()

        logger.debug('Checking batch feeder %s, dynamic table mame %s',batch_feeder_name, dynamic_table_name)
        if batch_feeder_name <>'' and dynamic_table_name<>'' and ( default_filter_2<>'' or default_filter_3<>'' or default_filter_4<>'' or default_filter_5<>'') and (global_filter1<>'' or global_filter2<>'' or global_filter3<>'') :
           result.append([dynamic_table_name,default_filter_2,default_filter_3,default_filter_4,default_filter_5,batch_feeder_name,global_filter1,global_filter2,global_filter3])

    logger.info('End running check_filter_conflict on file %s%s.',input_directory,input_file)
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
    final_result_file = parameters['feeder']['output_file_name']

    #define log file
    log_file = parameters['feeder']['log_file_name']

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
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

    #1. check dataset_consistency.
    result=check_dataset_consistency(input_directory,dm_config_file)
    work_sheet_name='Dataset_consistency'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #2.0 Give summary of duplicate checking
    result=check_duplicate_summary(input_directory,dm_config_file)
    work_sheet_name='Object_referred_Summary'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #2.1. Check if same table is defined in 2 feeder.
    result=check_duplicate_of_dm_table(input_directory,dm_config_file)
    work_sheet_name='DM_Table_Duplication'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #2. Check if same feeder is defined in 2 batches.
    result=check_duplicate_of_feeders(input_directory,dm_config_file)
    work_sheet_name='Feeder_Duplication'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #2.2. Check if same batch feeder is defined in 2 processing scripts.
    result=check_duplicate_of_batch_feeder(input_directory,dm_config_file)
    work_sheet_name='Batch_Feeder_Duplication'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #3 Check scanner engine usage
    result=check_scanner_engine_usage(input_directory,dm_config_file)
    work_sheet_name='Scanner_Engine'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)

    #4. check number of feeders in a batch, shall not be too many!
    result=check_number_of_feeder_in_batch(input_directory,dm_config_file)
    work_sheet_name='Feeder_number'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)


    #5 check_filter_conflict between dynamic table default settings and global filter
    result=check_filter_conflict(input_directory,dm_config_file)
    work_sheet_name='Filter_conflict'
    work_book=io_util.add_worksheet(result,work_book, work_sheet_name)


    #output the work_book
    io_util.save_workbook(work_book,output_directory+final_result_file)
    logger.info('End running datamart_table_analysis.py.')

if __name__ == "__main__":
    run()