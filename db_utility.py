__author__ = 'ywang'


import cx_Oracle
import ConfigParser
import os
import xml.etree.ElementTree as ET
import logging
from logging import handlers

class db_utility:
    dbsource = ''
    connectionString = ''

    logger = ''

    def initialize_log(self,log_level = logging.DEBUG, log_file = None):
        self.logger = logging.getLogger(__name__)

        if self.logger.handlers == []:
        # create a file handler
            if log_file is None:
                handler = logging.handlers.RotatingFileHandler('db_utlity.log',maxBytes=1024)
            else:
                handler = logging.handlers.RotatingFileHandler(log_file,maxBytes=1024)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            self.logger.setLevel(log_level)
            handler.setLevel(log_level)


            # add the handlers to the logger
            self.logger.addHandler(handler)

    def set_log_level(self, log_level= logging.DEBUG):
        for handler in self.logger.handlers:
            handler.setLevel(log_level)


    def set_dbsourcefile(self,sourcefile):
        self.logger.debug('Set db source file '+sourcefile)
        self.dbsource = sourcefile

    def load_dbsourcefile(self, sourcefile) :
        self.logger.debug('Parse dbsource file %s for connection string. ',sourcefile)

        if sourcefile is not None:
            self.logger.info('Using passed in dbsource file: %s', sourcefile)
            tree = ET.parse(sourcefile)
        elif self.dbsource is not None:
            self.logger.info('Using default dbsource file: %s', self.dbsource)
            tree = ET.parse(self.dbsource)
        else:
            self.logger.warning('dbsource file does not exist!')
            return -1

        root = tree.getroot()
        dbServerType= tree.find('./MxAnchors/MxAnchor/DbServerType')
        dbHostName= tree.find('./MxAnchors/MxAnchor/DbHostName')
        dbServerPortNumber=tree.find('./MxAnchors/MxAnchor/DbServerPortNumber')
        dbServerOrServiceName=tree.find('./MxAnchors/MxAnchor/DbServerOrServiceName')
        dbUser=tree.find('./MxAnchors/MxAnchor/DbDefaultCredential/DbUser')
        dbPassword=tree.find('./MxAnchors/MxAnchor/DbDefaultCredential/DbUser')

        self.connectionString=dbUser.text+'/'+dbPassword.text+'@'+dbHostName.text+':'+dbServerPortNumber.text\
                         +'/'+dbServerOrServiceName.text

        self.logger.debug('connectionString parsed is : %s', self.connectionString)

        return self.connectionString

    def prepare_sql(self,sql, sql_paramters):
        self.logger.debug('Start to prepare SQL to be executed.')
        self.logger.debug('SQL to prepare \n %s', sql)
        if sql_paramters is None:
            return sql

        for parameter_name, parameter_value in sql_paramters.iteritems():
            self.logger.debug('Start to mapping sql_paramter %s with value %s.',parameter_name,parameter_value)
            if sql.find('@'+parameter_name+':D'):
                formatted_value='to_date(\''+parameter_value+'\',\'YYYY-MM-DD\')'
                sql = sql.replace('@'+parameter_name+':D',formatted_value )
            if sql.find('@'+parameter_name+':C'):
                formatted_value='\''+parameter_value+'\''
                sql = sql.replace('@'+parameter_name+':C',formatted_value )
            if sql.find('@'+parameter_name+':N'):
                sql = sql.replace('@'+parameter_name+':D',formatted_value )
        self.logger.debug('End SQL prepartion.')
        return sql

    def execute_sql(self, sql, sql_paramters, connectionString, batch_mode = True):
        self.logger.info('Start to execute SQL.')
        sql = self.prepare_sql(sql, sql_paramters)
        con = cx_Oracle.connect(connectionString)
        cur = con.cursor()
        cur.arraysize = 2000
        self.logger.debug('SQL to execute: \n %s', sql)
        cur.execute(sql)

        result = []

        if batch_mode:
            self.logger.info('Execute sql in batch')
            rows = cur.fetchall()
            for row in rows:
                result.append(row)
        else :
            self.logger.info('Execute sql in line by line')
            row = cur.fetchone()
            while row is not None:
                result.append(row)
                res = cur.fetchone()

        cur.close()
        con.close()
        self.logger.info('End execute SQL.')
        return result


    def dump_output(self, sql, sql_paramters, connectionString, dump_file_name, batch_mode = True):
        self.logger.info('Start to write result to file %s.',dump_file_name)
        sql = self.prepare_sql(sql, sql_paramters)

        con = cx_Oracle.connect(connectionString)
        cur = con.cursor()
        cur.arraysize = 2000
        self.logger.debug('SQL for file dump: \n %s', sql)
        cur.execute(sql)

        self.logger.info('Open dump file: %s',dump_file_name)
        raw_file = open(dump_file_name, 'w+')

        if batch_mode:
            self.logger.info('Execute sql in batch')
            rows = cur.fetchall()
            for row in rows:
                for cell in row:
                    raw_file.write(str(cell))
                raw_file.write('\n')
        else :
            self.logger.info('Execute sql in line by line')
            res = cur.fetchone()
            while res is not None:
                for field in res :
                    raw_file.write(str(field))
                raw_file.write('\n')
                res = cur.fetchone()

            raw_file.close()

        cur.close()
        con.close()
        self.logger.info('End write file.')

    def __init__(self, log_level=logging.DEBUG, log_file=None):
        self.initialize_log(log_level,log_file)
        self.logger.debug('Initialize db_utility class')


if __name__ == "__main__":
    #define directories
    input_directory = os.getcwd() + '\Input\\'
    output_directory = os.getcwd() + '\Output\\'
    sql_directory = os.getcwd() + '\SQLs\\'
    property_directory = os.getcwd() + '\properties\\'


    #define sql files
    query_ps_time_sql = 'query_processing_script_time.sql'

    #define input files
    ps_exuection_time_file = 'ps_execution_time.csv'

    #define property files
    parameter_file = 'parameters.txt'
    mxDbsource_file = 'dbsource.mxres'


    #define output file
    final_result_file = 'analyze_performance.xls'

    #read in property file
    config = ConfigParser.RawConfigParser()
    config.read(property_directory + parameter_file)
    period_days = config.getint('performance', 'period_days')
    time_alert_processing_script = config.get('performance', 'time_alert_processing_script')
    time_alert_batch_feeder = config.get('performance', 'time_alert_batch_feeder')
    time_alert_batch_extraction =config.get('performance', 'time_alert_batch_extraction')
    start_date = config.get('performance', 'start_date')
    end_date = config.get('performance', 'end_date')

    db_util = db_utility()

    sqlfile = open(sql_directory+query_ps_time_sql, 'r+')

    sqlString= ''
    for line in sqlfile:
        sqlString = sqlString + line

    sql_paramters = dict()
    sql_paramters['START_DATE'] = start_date
    sql_paramters['END_DATE'] = end_date

    connectionString = db_util.load_dbsourcefile(property_directory + mxDbsource_file)
    db_util.dump_output(sqlString,sql_paramters, connectionString, input_directory + 'aaa.csv')
    output=db_util.execute_sql(sqlString,sql_paramters,connectionString)
