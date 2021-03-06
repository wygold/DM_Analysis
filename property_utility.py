__author__ = 'ywang'

import ConfigParser
import os
import logging
from logging import handlers
from collections import OrderedDict

class property_utility:

    logger = ''

    def initialize_log(self, log_level = None, log_file =None ):
        logger = logging.getLogger(__name__)

        if log_level is None:
            logger.setLevel(logging.INFO)
        else :
            logger.setLevel(log_level)

        if logger.handlers == []:
            # create a file handler
            handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            if log_level is None:
                handler.setLevel(logging.INFO)
            else:
                handler.setLevel(log_level)

            # add the handlers to the logger
            logger.addHandler(handler)

    def set_log_level(self, log_level):
        logger = logging.getLogger(__name__)
        for handler in logger.handlers:
            if log_level is not None:
                handler.setLevel(log_level)
            else:
                handler.setLevel(log_level)

    def parse_property_file(self,property_file_dictory=None, property_file=None):
        parameters=OrderedDict()
        dynamic_table_parameters = OrderedDict()
        general_parameters = OrderedDict()
        datamart_table_parameters = OrderedDict()
        performance_parameters = OrderedDict()
        feeder_parameters = OrderedDict()
        log_parameters = OrderedDict()
        database_parameters = OrderedDict()
        scanner_engine_paramters = OrderedDict()
        analyze_report_parameters =  OrderedDict()
        core_parameters =  OrderedDict()

        #read in property file
        config = ConfigParser.RawConfigParser()
        if property_file_dictory is None or property_file is None :
            property_file_dictory = os.getcwd()+'\\Properties\\'
            property_file = 'parameters.txt'
            config.read(property_file_dictory + property_file)
        else :
            config.read(property_file_dictory + property_file)

        #read in log
        log_parameters['log_level'] = config.get('log', 'log_level')
        log_parameters['log_directory'] = config.get('log', 'log_directory')

        #define paramaters
        parameters['general'] = general_parameters
        parameters['dynamic table'] = dynamic_table_parameters
        parameters['datamart table'] = datamart_table_parameters
        parameters['performance'] = performance_parameters
        parameters['core'] = core_parameters
        parameters['feeder'] = feeder_parameters
        parameters['log'] = log_parameters
        parameters['database'] = database_parameters
        parameters['scanner engine'] = scanner_engine_paramters
        parameters['analyze report'] = analyze_report_parameters

        #read in preperties
        #read in general
        general_parameters['reload_data'] = config.getboolean('general', 'reload_data')
        general_parameters['input_directory'] = config.get('general', 'input_directory')
        general_parameters['output_directory'] = config.get('general', 'output_directory')
        general_parameters['sql_directory'] = config.get('general', 'sql_directory')
        general_parameters['raw_data_ouput'] = config.getboolean('general', 'raw_data_ouput')


        #read in dynamic table
        dynamic_table_parameters['max_number_fields'] = config.getint('dynamic table', 'max_number_fields')
        dynamic_table_parameters['max_number_h_fields']  = config.getint('dynamic table', 'max_number_h_fields')
        dynamic_table_parameters['max_number_db_access_h_fields']  = config.getint('dynamic table', 'max_number_db_access_h_fields')
        dynamic_table_parameters['max_dynamic_table_referenced']  = config.getint('dynamic table', 'max_dynamic_table_referenced')
        dynamic_table_parameters['output_file_name']  = config.get('dynamic table', 'output_file_name')
        dynamic_table_parameters['log_file_name']  = config.get('dynamic table', 'log_file_name')


        #read in datamart table
        datamart_table_parameters['max_number_fields'] = config.getint('datamart table', 'max_number_fields')
        datamart_table_parameters['output_file_name']  = config.get('datamart table', 'output_file_name')
        datamart_table_parameters['log_file_name']  = config.get('datamart table', 'log_file_name')

        #read in feeder
        feeder_parameters['output_file_name']  = config.get('feeder', 'output_file_name')
        feeder_parameters['log_file_name']  = config.get('feeder', 'log_file_name')
        feeder_parameters['max_reference']  = config.getint('feeder', 'max_reference')

        #read in performance
#       performance_parameters['period_days'] = config.getint('performance', 'period_days')
        performance_parameters['start_date'] = config.get('performance', 'start_date')
        performance_parameters['end_date'] = config.get('performance', 'end_date')
        performance_parameters['time_alert_processing_script'] = config.get('performance', 'time_alert_processing_script')
        performance_parameters['time_alert_batch_feeder'] = config.get('performance', 'time_alert_batch_feeder')
        performance_parameters['time_alert_batch_extraction'] =config.get('performance', 'time_alert_batch_extraction')
#       performance_parameters['time_filter_output'] =config.getboolean('performance', 'time_filter_output')
        performance_parameters['output_file_name']  = config.get('performance', 'output_file_name')
        performance_parameters['log_file_name']  = config.get('performance', 'log_file_name')



        #read in core config
        core_parameters['max_number_fields']  = config.get('core', 'max_number_fields')
        core_parameters['max_number_h_fields']  = config.get('core', 'max_number_h_fields')
        core_parameters['max_number_db_access_h_fields']  = config.get('core', 'max_number_db_access_h_fields')
        core_parameters['max_reference']  = config.get('core', 'max_reference')
        core_parameters['start_date']  = config.get('core', 'start_date')
        core_parameters['end_date']  = config.get('core', 'end_date')
        core_parameters['time_alert_processing_script']  = config.get('core', 'time_alert_processing_script')
        core_parameters['time_alert_batch_feeder']  = config.get('core', 'time_alert_batch_feeder')
        core_parameters['time_alert_batch_extraction']  = config.get('core', 'time_alert_batch_extraction')
        core_parameters['output_file_name']  = config.get('core', 'output_file_name')
        core_parameters['log_file_name']  = config.get('core', 'log_file_name')

        #read in db config
        database_parameters['db_config_folder']= config.get('database', 'db_config_folder')
        database_parameters['mx_db_config_file']= config.get('database', 'mx_db_config_file')
        database_parameters['dm_db_config_file']= config.get('database', 'dm_db_config_file')

        #read in analyze report
        analyze_report_parameters['log_file_name']= config.get('analyze report', 'log_file_name')
        analyze_report_parameters['analyze_template_file_name']= config.get('analyze report', 'analyze_template_file_name')

        #read in dynamic table type that can be enabled for scanner engine
        scanner_engine_paramters['eligible_dynamic_tables']= config.get('scanner engine', 'eligible_dynamic_tables').replace('\n','').split(',')

        return parameters

    def __init__(self, log_level=logging.INFO, log_file=None):
        pass

    def run(self):
        parameters = self.parse_property_file()

        for keys, content in parameters.iteritems():
            print '['+keys+']'
            for subkeys,subcontente in content.iteritems():
                print subkeys + ' = ' + str(subcontente)

        return parameters

if __name__ == "__main__":
    prop_util = property_utility()
    prop_util.run()