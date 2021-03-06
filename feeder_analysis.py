__author__ = 'ywang'

from xlwt import *
import ConfigParser
import os
from db_utility import db_utility
from io_utility import io_utility
import logging
from logging import handlers
from property_utility import property_utility
from operator import itemgetter, attrgetter, methodcaller
from collections import OrderedDict
from analyze_report import analyze_report

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


#1 Check if batch of feeder with same label of data has same historization and data computed by several batch and Data(published/private)
def check_dataset_consistency(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_dataset_consistency on file %s%s.',input_directory,input_file)

    final_result=[['Batch of feeders have possible wrong dataset settings marked as inconsistent in last column']]
    final_result.append(['Label of Data','Batch of feeders','Historisation','Private','Data Computed by Several Batches','Setting is correct'])
    result=[]
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
            temp = [batch_contents[0],batch_name,batch_contents[1],batch_contents[2],batch_contents[3],batch_contents[4]]
            result.append(temp)


    #sort the result
    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(0),reverse=False)
    final_result.extend(sorted_result)

    logger.info('End running check_total_datamart_table_field_number on file %s%s.',input_directory,input_file)
    return final_result

#2 Check if same feeder are used in different batch feeder
def check_duplicate_of_feeders(input_directory,input_file,max_reference=1) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_duplicate_of_feeders in different batch of feeder on file %s%s.',input_directory,input_file)

    final_result=[['Details of table feeders referenced by more than '+str(max_reference)+' batch of feeders']]
    final_result.append(['Feeder','Batch of feeder','Description','Global filter','Label of data','Last Execution Date'])
    result=[]

    feeders = dict()
    batch_execution_time = dict()
    batch_feeder_desc = dict()
    global_filter_label=dict()
    label_of_data = dict()

    for line in raw_file:
        fields = line.split(' | ')

        object_type=fields[23].strip()

        if object_type == 'FEEDERS' :
            feeder_name=fields[15].strip()
            batch_feeder_name=fields[2].strip()
            current_batch_feeder_desc=fields[44].strip()
            batch_last_execution_date = fields[4].strip()
            current_global_filter_label = fields[45].strip()
            current_label_of_data= fields[14].strip()

            logger.debug('Checking feeder: %s, batch feeder: %s, last excution time: %s.',feeder_name,batch_feeder_name,batch_last_execution_date)
            if not feeders.has_key(feeder_name) :
                feeders[feeder_name]=[batch_feeder_name]
            else :
                if batch_feeder_name not in feeders[feeder_name] and batch_feeder_name<>'':
                    feeders[feeder_name].append(batch_feeder_name)

            global_filter_label[batch_feeder_name]=current_global_filter_label
            label_of_data[batch_feeder_name]=current_label_of_data
            batch_execution_time[batch_feeder_name]=batch_last_execution_date
            batch_feeder_desc[batch_feeder_name] = current_batch_feeder_desc


    for feeder_name, feeder_content in feeders.iteritems():
        logger.debug('Number of batch feeders is %i that has same feeder %s.',len(feeder_content),feeder_name)
        if len(feeder_content) >= max_reference :
            for batch_feeder_name in feeder_content :
                if batch_feeder_name <> '':
                    temp = [feeder_name, batch_feeder_name, batch_feeder_desc[batch_feeder_name],global_filter_label[batch_feeder_name], label_of_data[batch_feeder_name],batch_execution_time[batch_feeder_name]]
                    result.append(temp)

    #sort the result
    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(0),reverse=False)
    final_result.extend(sorted_result)

    logger.info('End running check_duplicate_of_feeders on file %s%s.',input_directory,input_file)
    return final_result


#2.1 Check if same datamart are used in different single feeder
def check_duplicate_of_dm_table(input_directory,input_file,max_reference=1) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_duplicate_of_dm_table in different batch of feeder on file %s%s.',input_directory,input_file)

    final_result=[['Details of datamart tables referenced by more than '+str(max_reference-1)+' table feeders']]
    final_result.append(['DM Table Name','Feeder name','Description','Last Execution Date'])
    result=[]

    dm_tables = dict()
    feeder_execution_time = dict()
    feeder_desc = dict()

    for line in raw_file:
        fields = line.split(' | ')

        object_type=fields[23].strip()

        if object_type == 'FEEDERS' :
            dm_tables_name=fields[24].strip()
            feeder_name=fields[15].strip()
            current_feeder_desc=fields[43].strip()
            feeder_last_execution_date = fields[17].strip()
            logger.debug('Checking dm table: %s, feeder: %s, last excution time: %s.',dm_tables_name,feeder_name,feeder_last_execution_date)
            if not dm_tables.has_key(dm_tables_name) :
                dm_tables[dm_tables_name]=[feeder_name]
            else :
                if feeder_name not in dm_tables[dm_tables_name] and feeder_name<>'':
                    dm_tables[dm_tables_name].append(feeder_name)
            feeder_execution_time[feeder_name]=feeder_last_execution_date
            feeder_desc[feeder_name]=current_feeder_desc

    for dm_tables_name, dm_tables_content in dm_tables.iteritems():
        logger.debug('Number of feeders is %i that has same datamart table %s.',len(dm_tables_content),dm_tables_name)
        if len(dm_tables_content) >= max_reference :
            for feeder_name in dm_tables_content :
                if feeder_name <> '':
                    temp = [dm_tables_name, feeder_name,feeder_desc[feeder_name], feeder_execution_time[feeder_name]]
                    result.append(temp)

    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(0),reverse=False)
    final_result.extend(sorted_result)

    logger.info('End running check_duplicate_of_dm_table on file %s%s.',input_directory,input_file)
    return final_result

#2.2 Check if same batch feeder are defined in different processing script
def check_duplicate_of_batch_feeder(input_directory,input_file,ps_exuection_time_file,max_reference=1) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_duplicate_of_batch_feeder in different batch of feeder on file %s%s.',input_directory,input_file)

    result=[['Batch of Feeder referenced in more than ' + str(max_reference -1 ) + ' processing scripts']]
    result.append(['Batch of Feeder','Entity','Processing Script','Last execution date'])

    batch_feeders = dict()
    ps_exeuction_date = dict()
    batch_entity = dict()

    for line in raw_file:
        fields = line.split(' | ')

        object_type=fields[23].strip()

        if object_type == 'FEEDERS' :
            batch_feeder_name=fields[2].strip()
            processing_script_name=fields[0].strip()
            current_batch_entity = fields[46].strip()
            logger.debug('Checking batch feeder: %s in processing script: %s.',batch_feeder_name,processing_script_name)
            if not batch_feeders.has_key(batch_feeder_name) :
                batch_feeders[batch_feeder_name]=[processing_script_name]
                batch_entity[batch_feeder_name]=current_batch_entity
            else :
                if processing_script_name not in batch_feeders[batch_feeder_name] and processing_script_name<>'':
                    batch_feeders[batch_feeder_name].append(processing_script_name)


    #get exucution time
    ps_exuection_file= open(input_directory+ps_exuection_time_file, 'r')
    for line in ps_exuection_file:
        fields = line.split(' | ')
        script_name = fields[2].strip()
        computing_date = fields[1].strip()

        if ps_exeuction_date.has_key(script_name):
            ps_exeuction_date[script_name]=computing_date


    for batch_feeder_name, batch_feeder_content in batch_feeders.iteritems():
        if len(batch_feeder_content) >= max_reference:
            for processing_script_name in batch_feeder_content :
                if processing_script_name <> '' :
                    if ps_exeuction_date.has_key(processing_script_name):
                        temp = [batch_feeder_name,batch_entity[batch_feeder_name], processing_script_name,ps_exeuction_date[processing_script_name]]
                        result.append(temp)
                    else :
                        temp = [batch_feeder_name,batch_entity[batch_feeder_name], processing_script_name,'']
                        result.append(temp)

    logger.info('End running check_duplicate_of_batch_feeder on file %s%s.',input_directory,input_file)
    return result

#2.0 Give summary of duplicate checking for dm table
def check_duplicate_dm_table_summary(input_directory,input_file,ps_exuection_time_file,max_reference=1) :
    logger = logging.getLogger(__name__)
    logger.info('Start to run check_duplicate_dm_table_summary in different batch of feeder on file %s%s.',input_directory,input_file)

    logger.info('Process how datamart tables are refernced by feeders')

    final_result=[['Summary of datamart tables referenced by more than '+str(max_reference -1)+' table feeders']]
    final_result.append(['Name of Datamart table','# of Referenced feeders'])
    result=[]
    dm_tables_result=check_duplicate_of_dm_table(input_directory,input_file,max_reference)

    dm_tables=dict()
    for i in range(2,len(dm_tables_result)):
        dm_table_name=dm_tables_result[i][0]
        if not dm_tables.has_key(dm_table_name):
            dm_tables[dm_table_name]=1
        else:
            dm_tables[dm_table_name] = dm_tables[dm_table_name]+1

    for dm_table_name, feeder_counter in dm_tables.iteritems():
        temp = [dm_table_name, int(feeder_counter)]
        result.append(temp)


    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(1),reverse=True)
    final_result.extend(sorted_result)

    logger.info('End running check_duplicate_dm_table_summary on file %s%s.',input_directory,input_file)
    return final_result




#2.009 Give summary of how many tables referenced in a feeder
def check_feeder_summary(input_directory,input_file,ps_exuection_time_file,max_reference=1) :
    logger = logging.getLogger(__name__)
    logger.info('Start to run check_feeder_summary in different batch of feeder on file %s%s.',input_directory,input_file)

    final_result=[['Summary of table feeders that are feeding more than '+ str(max_reference-1) +' datamart table(s)']]

    logger.info('Process how many datamart tables are used in a single feeder')
    final_result.append(['Name of feeders','# of underlying dm tables'])
    result=[]
    feeders_result=check_number_of_tables_in_feeder(input_directory,input_file,max_reference)

    feeders=dict()

    for i in range(2,len(feeders_result)):
        feeder_name=feeders_result[i][0]
        if not feeders.has_key(feeder_name):
            feeders[feeder_name]=1
        else:
            feeders[feeder_name] = feeders[feeder_name]+1

    for feeder_name, dm_table_contents in feeders.iteritems():
        temp = [feeder_name, int(dm_table_contents)]
        result.append(temp)

    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(1),reverse=True)
    final_result.extend(sorted_result)

    logger.info('End running check_duplicate_feeder_summary on file %s%s.',input_directory,input_file)
    return final_result

def check_number_of_tables_in_feeder(input_directory,input_file,max_reference=1) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_number_of_tables_in_feeder in different batch of feeder on file %s%s.',input_directory,input_file)

    result=[['Details of table feeders that are feeding more than '+str(max_reference-1)+' datamart table(s)']]
    result.append(['Feeder','DM Table','Last Execution Date'])

    feeders = dict()
    feeder_execution_times = dict()

    for line in raw_file:
        fields = line.split(' | ')

        object_type=fields[23].strip()

        if object_type == 'FEEDERS' :
            dm_table = fields[24].strip()
            feeder_name=fields[15].strip()
            feeder_execution_time = fields[16].strip()

            logger.debug('Checking feeder: %s, dm table : %s, last excution time: %s.',feeder_name,dm_table,feeder_execution_time)
            if not feeders.has_key(feeder_name) :
                feeders[feeder_name]=[dm_table]
            else :
                if dm_table not in feeders[feeder_name] and dm_table<>'':
                    feeders[feeder_name].append(dm_table)

            feeder_execution_times[feeder_name]=feeder_execution_time

    for feeder_name, feeder_content in feeders.iteritems():
        logger.debug('Number of dm table is %i that has same feeder %s.',len(feeder_content),feeder_name)
        if len(feeder_content) >= max_reference :
            for dm_table_name in feeder_content :
                if dm_table_name <> '':
                    temp = [feeder_name, dm_table_name, feeder_execution_times[feeder_name]]
                    result.append(temp)

    logger.info('End running check_number_of_tables_in_feeder on file %s%s.',input_directory,input_file)
    return result

#2.01 Give summary of duplicate checking for feeder
def check_duplicate_feeder_summary(input_directory,input_file,ps_exuection_time_file,max_reference=1) :
    logger = logging.getLogger(__name__)
    logger.info('Start to run check_duplicate_feeder_summary in different batch of feeder on file %s%s.',input_directory,input_file)

    final_result=[['Summary of table feeders referenced by more than '+str(max_reference-1)+' batch of feeders']]

    logger.info('Process how feeders are refernced by batch feeders')
    final_result.append(['Name of feeders','# of Referenced Batch feeders'])
    result=[]
    feeders_result=check_duplicate_of_feeders(input_directory,input_file,max_reference)

    feeders=dict()
    for i in range(2,len(feeders_result)):
        feeder_name=feeders_result[i][0]
        if not feeders.has_key(feeder_name):
            feeders[feeder_name]=1
        else:
            feeders[feeder_name] = feeders[feeder_name]+1

    for feeder_name, batch_feeder_counter in feeders.iteritems():
        temp = [feeder_name, int(batch_feeder_counter)]
        result.append(temp)

    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(1),reverse=True)
    final_result.extend(sorted_result)

    logger.info('End running check_duplicate_feeder_summary on file %s%s.',input_directory,input_file)
    return final_result

#2.02 Give summary of duplicate checking for batch feeder
def check_duplicate_batch_feeder_summary(input_directory,input_file,ps_exuection_time_file,max_reference=1) :
    logger = logging.getLogger(__name__)
    logger.info('Start to run check_duplicate_batch_feeder_summary in different batch of feeder on file %s%s.',input_directory,input_file)

    final_result=[['Summary of batch of feeders referenced by more than '+str(max_reference-1)+' processing script(s)']]

    logger.info('Process how batch feeders are referenced by processing scripts')
    final_result.append(['Name of batch feeders','# of Referenced Processing scripts'])

    result=[]

    batch_feeders_result=check_duplicate_of_batch_feeder(input_directory,input_file,ps_exuection_time_file,max_reference)

    batch_feeders=dict()
    for i in range(2,len(batch_feeders_result)):
        batch_feeder_name = batch_feeders_result[i][0]
        if not batch_feeders.has_key(batch_feeder_name):
            batch_feeders[batch_feeder_name]=1
        else:
            batch_feeders[batch_feeder_name] = batch_feeders[batch_feeder_name]+1

    for batch_feeder_name, processing_script_counter in batch_feeders.iteritems():
        temp = [batch_feeder_name, int(processing_script_counter)]
        result.append(temp)

    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(1),reverse=True)
    final_result.extend(sorted_result)

    logger.info('End running check_duplicate_batch_feeder_summary on file %s%s.',input_directory,input_file)
    return final_result

#3 Check scanner engine usage
def check_scanner_engine_usage(input_directory,input_file,scanner_engine_enabled_dynamic_table) :

    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_scanner_engine_usage for batch of feeder on file %s%s.',input_directory,input_file)

    final_result=[['Usage of scanner engines in batch of feeders']]
    final_result.append(['Batch of feeder','Dynamic table type','Template','Process number','Batch type','Batch size' ,'Retries','Retries batch size'])
    result=[]
    engine_usage = dict()
    dynamic_table_types=dict()


    for line in raw_file:
        fields = line.split(' | ')
        dynamic_table_type=fields[28].strip()
        batch_feeder_name=fields[2].strip()
        engine_number =fields[12].strip()
        engine_size = fields[47].strip()
        engine_type = fields[48].strip()
        engine_name = fields[49].strip()
        engine_retry_time =  fields[50].strip()
        engine_retry_threshold = fields[51].strip()

        logger.debug('Checking batch feeder %s, dynamic table type %s, engine number %s ',batch_feeder_name,fields[27].strip(), engine_number)

        if dynamic_table_type in scanner_engine_enabled_dynamic_table and batch_feeder_name<>'' :
            engine_usage[batch_feeder_name]=[engine_name,engine_number,engine_type,engine_size,engine_retry_time,engine_retry_threshold]
            dynamic_table_types[batch_feeder_name]=dynamic_table_type

    for batch_feeder_name, engine_details in engine_usage.iteritems():
        temp = [batch_feeder_name,dynamic_table_types[batch_feeder_name], engine_details[0],int(engine_details[1]),engine_details[2],engine_details[3],engine_details[4],engine_details[5]]
        result.append(temp)


    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(3,0),reverse=False)
    final_result.extend(sorted_result)

    logger.info('End running check_scanner_engine_usage on file %s%s.',input_directory,input_file)
    return final_result


#4. check number of feeders in a batch, shall not be too many!
def check_number_of_feeder_in_batch(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_number_of_feeder_in_batch for batch of feeder on file %s%s.',input_directory,input_file)

    final_result=[['Number of table feeders for each batch of feeders']]
    final_result.append(['Batch of feeders','Number of Feeders (BoF size)'])
    result=[]

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
        temp = [batch_feeder_name,(len(single_feeders))]
        result.append(temp)

    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(1),reverse=True)
    final_result.extend(sorted_result)

    logger.info('End running check_number_of_feeder_in_batch on file %s%s.',input_directory,input_file)
    return final_result

#5 check_filter_conflict between dynamic table default settings and global filter
def check_filter_conflict(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_filter_conflict for batch of feeder on file %s%s.',input_directory,input_file)

    result=[['Chain of filters from Dynamic table to Batch of feeders']]
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


#check dynamic table reference number
def check_dynamic_table_post_filter(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_dynamic_table_post_filter on file %s%s.',input_directory,input_file)

    final_result=[['Dynamic tables with post-filter defined']]
    final_result.append(['Batch of feeder name','Dynamic table name','Category','Post-filter'])
    result = []

    batch_feeders = dict()

    for line in raw_file:
        fields = line.split(' | ')

        batch_feeder = fields[2].strip()
        dynamic_table = fields[26].strip()
        dynamic_table_category = fields[27].strip()
        dynamic_table_post_filter = fields[41].strip()

        if batch_feeder<>'' and dynamic_table_post_filter<>'':
            batch_feeders[batch_feeder]=[dynamic_table,dynamic_table_category,dynamic_table_post_filter ]

    for batch_feeder, post_filter_details in batch_feeders.iteritems():
         result.append([batch_feeder,post_filter_details[0],post_filter_details[1],post_filter_details[2]])


    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(0),reverse=False)
    final_result.extend(sorted_result)

    logger.info('End running check_dynamic_table_post_filter on file %s%s.',input_directory,input_file)
    return final_result

#check dynamic table reference number
def check_batch_feeder_computing_dates(input_directory,input_file) :
    raw_file= open(input_directory+input_file, 'r')

    logger = logging.getLogger(__name__)
    logger.info('Start to run check_batch_feeder_computing_dates on file %s%s.',input_directory,input_file)

    final_result=[['Batch of feeder running on more than 1 computing date']]
    final_result.append(['Batch of feeder name','Computing date 0','Computing date 1','Computing date 2'])
    result = []

    batch_feeders = dict()

    for line in raw_file:
        fields = line.split(' | ')

        batch_feeder = fields[2].strip()
        computing_dates = fields[6].strip().split(' ,')

        if batch_feeder<>'' and len(computing_dates)==3:
            if computing_dates[1] <>'NS' or computing_dates[0] <>'NS' :
                batch_feeders[batch_feeder]=[computing_dates[0],computing_dates[1],computing_dates[2]]

    for batch_feeder, computing_dates in batch_feeders.iteritems():
         result.append([batch_feeder,computing_dates[0],computing_dates[1],computing_dates[2]])


    logger.debug('Sort the result')
    sorted_result = sorted(result,key=itemgetter(0),reverse=False)
    final_result.extend(sorted_result)

    logger.info('End running check_batch_feeder_computing_dates on file %s%s.',input_directory,input_file)
    return final_result


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

def run(reload_check_button_status=None,log_dropdown_status=None, core_analysis = None, work_books_content = None):
    #define properties folder
    property_directory=os.getcwd()+'\\properties\\'
    parameter_file='parameters.txt'

    property_util = property_utility()
    parameters = property_util.parse_property_file(property_directory,parameter_file)


    #define sql files
    query_dm_sql='query_dm_config.sql'

    #define input files
    dm_config_file = 'source.csv'

    #define sql files
    query_ps_time_sql='query_processing_script_time.sql'

    #define input files
    ps_exuection_time_file = 'ps_execution_time.csv'

    #define property files
    mxDbsource_file=parameters['database']['mx_db_config_file']

    #define output file
    final_result_file = parameters['feeder']['output_file_name']

    #define log file
    log_file = parameters['feeder']['log_file_name']

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
    reload_data = parameters['general']['reload_data']
    start_date = parameters['performance']['start_date']
    end_date = parameters['performance']['end_date']
    raw_data_ouput = config.getboolean('general', 'raw_data_ouput')
    analyze_template_file = parameters['analyze report']['analyze_template_file_name']
    if core_analysis == None :
        max_reference = config.getint('feeder', 'max_reference')
    else :
        max_reference = config.getint('core', 'max_reference')

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
        db_type = db_util.db_type
        #prepare datamart configuration SQLs to be run
        sqlfile = open(sql_directory+db_type+'\\'+query_dm_sql, 'r+')
        sqlString= ''
        for line in sqlfile:
            sqlString = sqlString + line

        #prepare sql paramaters, the paramaters are defined according to MX format @:paramater_name:N/D/C
        sql_paramters = dict()

        #dump file
        db_util.dump_output(sqlString, None, connectionString, input_directory + dm_config_file)


    if (reload_check_button_status is None and reload_data) or (reload_check_button_status):
        #prepare connection string
        db_util = db_utility(log_level,log_directory+log_file)
        connectionString = db_util.load_dbsourcefile(property_directory + mxDbsource_file)

        #prepare SQLs to be run
        sqlfile = open(sql_directory+db_type+'\\'+query_ps_time_sql, 'r+')
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
    if work_books_content == None:
        work_books_content = OrderedDict()
    work_sheet_names = []

    #2.0 Give summary of duplicate checking
    if core_analysis == None or 'Summary_REP_TAB' in core_analysis :
        result=check_duplicate_dm_table_summary(input_directory,dm_config_file,ps_exuection_time_file,max_reference)
        work_sheet_name='Summary_REP_TAB'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)


    #2.1. Check if same table is defined in 2 feeder.
    if core_analysis == None or 'REP_TAB_VS_T_FEED' in core_analysis :
        result=check_duplicate_of_dm_table(input_directory,dm_config_file,max_reference)
        work_sheet_name='REP_TAB_VS_T_FEED'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #2.009 Give summary of how many tables referenced in a feeder
    if core_analysis == None or 'Summary_T_FEED_1' in core_analysis :
        result=check_feeder_summary(input_directory,dm_config_file,ps_exuection_time_file,max_reference)
        work_sheet_name='Summary_T_FEED_1'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)



    #2.0091 Check if same feeder is defined in 2 batches.
    if core_analysis == None or 'T_FEED_VS_DM' in core_analysis :
        result=check_number_of_tables_in_feeder(input_directory,dm_config_file,max_reference)
        work_sheet_name='T_FEED_VS_DM'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #2.01 Give summary of duplicate checking
    if core_analysis == None or 'Summary_T_FEED_2' in core_analysis :
        result=check_duplicate_feeder_summary(input_directory,dm_config_file,ps_exuection_time_file,max_reference)
        work_sheet_name='Summary_T_FEED_2'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #2. Check if same feeder is defined in 2 batches.
    if core_analysis == None or 'T_FEED_VS_BOF' in core_analysis :
        result=check_duplicate_of_feeders(input_directory,dm_config_file,max_reference)
        work_sheet_name='T_FEED_VS_BOF'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #2.01 Give summary of duplicate checking
    if core_analysis == None or 'Summary_BOF' in core_analysis :
        result=check_duplicate_batch_feeder_summary(input_directory,dm_config_file,ps_exuection_time_file,max_reference)
        work_sheet_name='Summary_BOF'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #2.2. Check if same batch feeder is defined in 2 processing scripts.
    if core_analysis == None or 'BOF_VS_PS' in core_analysis :
        result=check_duplicate_of_batch_feeder(input_directory,dm_config_file,ps_exuection_time_file,max_reference)
        work_sheet_name='BOF_VS_PS'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #3 Check scanner engine usage
    if core_analysis == None or 'Scanner_Engine' in core_analysis :
        result=check_scanner_engine_usage(input_directory,dm_config_file, parameters['scanner engine']['eligible_dynamic_tables'])
        work_sheet_name='Scanner_Engine'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #4. check number of feeders in a batch, shall not be too many!
    if core_analysis == None or 'BOF_SIZE' in core_analysis :
        result=check_number_of_feeder_in_batch(input_directory,dm_config_file)
        work_sheet_name='BOF_SIZE'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #5 check_filter_conflict between dynamic table default settings and global filter
    if core_analysis == None or 'Filter_conflict' in core_analysis :
        result=check_filter_conflict(input_directory,dm_config_file)
        work_sheet_name='Filter_conflict'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #1. check dataset_consistency.
    if core_analysis == None or 'Dataset_consistency' in core_analysis :
        result=check_dataset_consistency(input_directory,dm_config_file)
        work_sheet_name='Dataset_consistency'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #6. check post filter defined in dynamic table
    if core_analysis == None or 'Post_filter' in core_analysis :
        result=check_dynamic_table_post_filter(input_directory,dm_config_file)
        work_sheet_name='Post_filter'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)

    #6. check post filter defined in dynamic table
    if core_analysis == None or 'Computing_dates' in core_analysis :
        result=check_batch_feeder_computing_dates(input_directory,dm_config_file)
        work_sheet_name='Computing_dates'
        work_books_content[work_sheet_name]=result
        work_sheet_names.append(work_sheet_name)


    #create content sheet
    if core_analysis == None :
        result=create_content_page(work_sheet_names,work_books_content)
        work_sheet_name='Content'
        work_book=io_util.add_content_worksheet(result,work_book, work_sheet_name)

    sheet_sequence = 0

    if core_analysis == None :
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

            if raw_data_ouput:
                work_book=io_util.add_raw_worksheet(result,work_book, work_sheet_name,True)
            else :
                analyze_rep = analyze_report()
                analyze_result = analyze_rep.generate_report_content([work_sheet_name], property_directory, analyze_template_file)
                work_book=io_util.add_worksheet(result,work_book, work_sheet_name,True, preview_sheet,next_sheet,'Review: '+analyze_result[work_sheet_name][2])

            sheet_sequence = sheet_sequence + 1


    #output the work_book
    if core_analysis == None :
        io_util.save_workbook(work_book,output_directory+final_result_file)
        logger.info('End running datamart_table_analysis.py.')
    else :
        return work_books_content

if __name__ == "__main__":
    run()