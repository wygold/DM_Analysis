__author__ = 'ywang'

import ConfigParser
import os
import logging
from logging import handlers
from collections import OrderedDict
from property_utility import property_utility
import re


class analyze_report:

    logger = ''

    def initialize_log(self, log_level = None, log_file = None ):
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


    def generate_report_file(self,analyzed_list, analzye_template_directory=None, analyze_template_file=None):

        logger = logging.getLogger(__name__)
        logger.info('Start to run generate_report_file.')

        reports=OrderedDict()

        #read in template file
        config = ConfigParser.RawConfigParser()
        if analzye_template_directory is None or analyze_template_file is None :
            analzye_template_directory = os.getcwd()+'\\Properties\\'
            analyze_template_file = 'analyze_template.txt'
            config.read(analzye_template_directory + analyze_template_file)
        else :
            config.read(analzye_template_directory + analyze_template_file)

        #read in
        for analyzed_item in analyzed_list:
            type = config.get(analyzed_item, 'type')
            sheet = config.get(analyzed_item, 'sheet')
            description = config.get(analyzed_item, 'description')
            review = config.get(analyzed_item, 'review')

            logger.debug('Start to generate report for %s analyze %s.', type, analyzed_item)

            description=self.process_content_with_input_paramaters(type, description)
            review=self.process_content_with_input_paramaters(type, review)

            reports[analyzed_item] = [sheet,description,review]



    def process_content_with_input_paramaters(self, type, content, property_directory=None,parameter_file=None):

        if property_directory is None or parameter_file is None :
            #define properties folder
            property_directory=os.getcwd()+'\\properties\\'
            parameter_file='parameters.txt'

        property_util = property_utility()
        parameters = property_util.parse_property_file(property_directory,parameter_file)
        substitute_strings = dict()

        for word in re.split('[)]|\s|[(]|\'',content) :
            if str(word).startswith('@') :
                substitute_strings[word] = parameters[type][str(word).replace('@','')]

        for original, substitute in substitute_strings.iteritems():
            content = content.replace(str(original),str(substitute))

        #also replace \n to make carriage return work
        content = content.replace('\\n','\n')

        print content

        return content

    def __init__(self, log_level=logging.DEBUG, log_file=None):
        #define properties folder
        property_directory=os.getcwd()+'\\properties\\'
        parameter_file='parameters.txt'

        property_util = property_utility()
        parameters = property_util.parse_property_file(property_directory,parameter_file)

        #define log file
        log_file = parameters['analyze report']['log_file_name']
        log_directory =os.getcwd()+'\\'+parameters['log']['log_directory']+'\\'

        self.initialize_log(log_level,log_directory+log_file)

    def run(self):
        #define properties folder
        property_directory=os.getcwd()+'\\properties\\'
        parameter_file='parameters.txt'

        property_util = property_utility()
        parameters = property_util.parse_property_file(property_directory,parameter_file)

        #define log file
        log_file = parameters['dynamic table']['log_file_name']

        analyzed_list = ['Field_Check',
                         'H_Field_Check',
                         'H_DB_Field_Check',
                         'Sensi_Flag_Check',
                         'Build_Mode_Check',
                         'Field_Reference_Summary',
                         'Field_Reference_Detail',
                         'DM_TBL_Reference_Summary',
                         'DM_TBL_Reference_Detail']

        self.generate_report_file(analyzed_list)


if __name__ == "__main__":
    analyze_rep = analyze_report()
    analyze_rep.run()