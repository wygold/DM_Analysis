__author__ = 'ywang'

import dynamic_table_analysis
import datamart_table_analysis
import feeder_analysis
import performance_analysis
from analyze_report import analyze_report

from xlwt import *
import ConfigParser
import os
from io_utility import io_utility
from property_utility import property_utility
import logging
from logging import handlers
from operator import itemgetter, attrgetter, methodcaller
from collections import OrderedDict


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

def get_core_analysis_list( analzye_template_directory=None, analyze_template_file=None):
        logger = logging.getLogger(__name__)
        logger.info('Start to run get_core_analysis_list.')

        #read in analyze_template_file keywords
        logger.info('Start to run analyze_processing_script_total_time on file %s%s',analzye_template_directory, analyze_template_file)

        if analzye_template_directory is None or analyze_template_file is None :
            analzye_template_directory = os.getcwd()+'\\Properties\\'
            analyze_template_file = 'analyze_template.txt'

        raw_file= open(analzye_template_directory+analyze_template_file, 'r')

        keys = []

        for line in raw_file:
            if '[' in line:
                keys.append(line.replace('[','').replace(']','').replace('\n',''))

        #read in template file
        config = ConfigParser.RawConfigParser()
        config.read(analzye_template_directory + analyze_template_file)

        core_analysis = []

        for key in keys:
            if config.get(key, 'core') == 'True':
                print key
                core_analysis.append(key)

        return  core_analysis



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

    #define output file
    final_result_file = parameters['core']['output_file_name']

     #define log file
    log_file = parameters['core']['log_file_name']

    analyze_template_file =  parameters['analyze report']['analyze_template_file_name']

    raw_data_ouput = parameters['general']['raw_data_ouput']

    #define directories
    input_directory=parameters['general']['input_directory']+'\\'
    output_directory=parameters['general']['output_directory']+'\\'
    sql_directory=parameters['general']['sql_directory']+'\\'
    log_directory =parameters['log']['log_directory']+'\\'

    if log_dropdown_status is None :
        log_level = parameters['log']['log_level']
    else:
        log_level = log_dropdown_status
    initialize_log(log_level,log_directory+log_file)

    logger = logging.getLogger(__name__)
    logger.info('Start to run core_analysis.py.')

    #create io_class
    io_util= io_utility(log_level,log_directory+log_file)

    #workbook for output result
    work_book = Workbook()
    work_sheet_names = []

    core_analysis= get_core_analysis_list(property_directory, analyze_template_file)

    work_books_content = OrderedDict()
    work_books_content = dynamic_table_analysis.run(reload_check_button_status, log_dropdown_status, core_analysis,work_books_content)
    work_books_content=datamart_table_analysis.run(reload_check_button_status, log_dropdown_status, core_analysis,work_books_content)
    work_books_content=feeder_analysis.run(reload_check_button_status, log_dropdown_status, core_analysis,work_books_content)
    work_books_content=performance_analysis.run(reload_check_button_status, log_dropdown_status, core_analysis,work_books_content)

    for work_sheet_name, result in work_books_content.iteritems():
        work_sheet_names.append(work_sheet_name)

    result=create_content_page(work_sheet_names,work_books_content)
    work_sheet_name='Content'
    work_book=io_util.add_content_worksheet(result,work_book, work_sheet_name)


    sheet_sequence = 0
    for work_sheet_name, result in work_books_content.iteritems():
        if sheet_sequence == 0:
            preview_sheet = 'Content'
        else:
            preview_sheet = work_sheet_names[sheet_sequence - 1]

        if sheet_sequence == len(work_sheet_names) - 1:
            next_sheet = None
        else:
            next_sheet = work_sheet_names[sheet_sequence + 1]

        if raw_data_ouput:
            work_book = io_util.add_raw_worksheet(result, work_book, work_sheet_name, True)
        else:
            analyze_rep = analyze_report()
            analyze_result = analyze_rep.generate_report_content([work_sheet_name], property_directory,
                                                                 analyze_template_file)
            work_book = io_util.add_worksheet(result, work_book, work_sheet_name, True, preview_sheet, next_sheet,
                                              'Review: ' + analyze_result[work_sheet_name][2])

        sheet_sequence = sheet_sequence + 1


    io_util.save_workbook(work_book,output_directory+final_result_file)