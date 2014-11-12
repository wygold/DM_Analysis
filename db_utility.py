__author__ = 'ywang'


import cx_Oracle
import ConfigParser
import os
import xml.etree.ElementTree as ET


class db_utility:
    dbsource = ''
    connectionString = ''

    def set_dbsourcefile(self,sourcefile):
       self.dbsource = sourcefile

    def load_dbsourcefile(self, sourcefile) :
        if sourcefile is not None:
            tree = ET.parse(sourcefile)
        elif self.dbsourc is not None:
            tree = ET.parse(self.dbsource)
        else:
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
        return self.connectionString

    def prepare_sql(self,sql, sql_paramters):
        if sql_paramters is None:
            return sql

        for parameter_name, parameter_value in sql_paramters.iteritems():
            if sql.find('@'+parameter_name+':D'):
                formatted_value='to_date(\''+parameter_value+'\',\'YYYY-MM-DD\')'
                sql = sql.replace('@'+parameter_name+':D',formatted_value )
            if sql.find('@'+parameter_name+':C'):
                formatted_value='\''+parameter_value+'\''
                sql = sql.replace('@'+parameter_name+':C',formatted_value )
            if sql.find('@'+parameter_name+':N'):
                sql = sql.replace('@'+parameter_name+':D',formatted_value )
        return sql

    def execute_sql(self, sql, sql_paramters, connectionString, batch_mode = True):

        sql = self.prepare_sql(sql, sql_paramters)

        con = cx_Oracle.connect(connectionString)
        cur = con.cursor()
        cur.arraysize = 2000
        cur.execute(sql)

        result = []

        if batch_mode:
            rows = cur.fetchall()
            for row in rows:
                result.append(row)
        else :
            row = cur.fetchone()
            while row is not None:
                result.append(row)
                res = cur.fetchone()

        cur.close()
        con.close()
        return result


    def dump_output(self, sql, sql_paramters, connectionString, dump_file_name, batch_mode = True):

        sql = self.prepare_sql(sql, sql_paramters)

        con = cx_Oracle.connect(connectionString)
        cur = con.cursor()
        cur.arraysize = 2000
        cur.execute(sql)

        raw_file = open(dump_file_name, 'w+')

        if batch_mode:
            rows = cur.fetchall()
            for row in rows:
                for cell in row:
                    raw_file.write(str(cell))
                raw_file.write('\n')
        else :
            res = cur.fetchone()
            while res is not None:
                for field in res :
                    raw_file.write(str(field))
                raw_file.write('\n')
                res = cur.fetchone()

            raw_file.close()

        cur.close()
        con.close()

    def __init__(self):
        self.data = []

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
    output=db_util.execute_sql(sqlString,connectionString)
