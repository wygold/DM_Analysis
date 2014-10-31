__author__ = 'ywang'


import cx_Oracle
import ConnectDB
import string
import xlrd
from xlwt import *


def generate_raw_file(connectionString,sqlfile, input_directory):
    sqlString = []

    for line in sqlfile:
        sqlString.append(line)
    #print "".join(sqlString)

    con = cx_Oracle.connect(connectionString)
    cur = con.cursor()
    cur.execute("".join(sqlString))

    res = cur.fetchone()
    raw_file = open(input_directory+'\source.csv', 'w+')
    while res is not None:
        for field in res :
            raw_file.write(str(field))
            raw_file.write(' | ')
        raw_file.write('\n')
        res = cur.fetchone()

    raw_file.close()
    cur.close()
    con.close()

def read_raw_file(input_directory) :
    raw_file= open(input_directory+'\source.csv', 'r')
    for line in raw_file:
        fields = line.split(' | ')
        print fields[26]+'   '+fields[27]+'   '+fields[28]+'   '

def check_total_dynamic_table_field_number(input_directory) :
    raw_file= open(input_directory+'\source.csv', 'r')
    result=[['Number of Dynamic table fields that exceeds 100']]
    result.append(['Dynamic table name','Category','Dynamic table type','Field count'])
    previous_dynamic_tables = []
    for line in raw_file:
        fields = line.split(' | ')

        if fields[29].strip()<>'' and int(fields[29])>100 :
        #    result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
            if (fields[26].strip()+fields[27].strip()) not in previous_dynamic_tables :
                result.append([fields[26].strip(),fields[27].strip(),fields[28].strip(),fields[29].strip()])
                previous_dynamic_tables.append(fields[26].strip()+fields[27].strip())

    return result

def format_excel():
    fnt2 = Font()
    fnt2.name = 'Arial'
    fnt2.colour_index = 20
    fnt2.bold = False

    borders = Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    return fnt2,borders

def write_to_output_file(result, output_directory, work_book, work_sheet_name):

    ws = work_book.add_sheet(work_sheet_name)

    contentstyle = XFStyle()
    contentstyle.font,contentstyle.borders = format_excel()

    TABLE_HEADER_FORMAT = easyxf(
                 'font: bold 1, name Tahoma, height 160;'
                 'align: vertical center, horizontal center, wrap on;'
                 'borders: left thin, right thin, top thin, bottom thin;'
                 'pattern: pattern solid, pattern_fore_colour yellow, pattern_back_colour yellow'
                 )

    TITLE_FORMAT = easyxf(
                 'font: bold 1, name Tahoma, height 300;'
                 'align: vertical center, horizontal center, wrap on;'
                 'borders: left thin, right thin, top thin, bottom thin;'
                 'pattern: pattern solid, pattern_fore_colour gray25, pattern_back_colour gray25'
                 )

    i = 0
    j = 0

    ws.col(i).width = 0x0d00 + i

    for row in result:
        for cell in row:
            if j < 12 and ws.col(j).width < len(cell)*300 :
                ws.col(j).width = len(cell)*320
            if i == 0 :
                ws.write(i, j, str(cell),TITLE_FORMAT)
            elif i == 1 :
                ws.write(i, j, str(cell),TABLE_HEADER_FORMAT)
            else :
                ws.write(i, j, str(cell),contentstyle)
            j = j + 1
        j = 0
        i = i + 1
    return work_book

if __name__ == "__main__":

    mxDbsourcefile=('D:\Dropbox\Project\DM_Analysis\properties\dbsource.mxres')
    input_directory=('D:\Dropbox\Project\DM_Analysis\Input\\')
    output_directory=('D:\Dropbox\Project\DM_Analysis\Output\\')
    connectionString = ConnectDB.loadMXDBSourcefile('D:\Dropbox\Project\DM_Analysis\properties\dbsource.mxres')

    sqlfile = open('D:\Dropbox\Project\DM_Analysis\SQLs\qurey_dm_config.txt', 'r+')

    #generate_raw_file(connectionString,sqlfile,input_directory)

    work_book = Workbook()

    result=check_total_dynamic_table_field_number(input_directory)
    work_sheet_name='Field_Check'
    work_book=write_to_output_file(result, output_directory, work_book, work_sheet_name)


    work_book.save(output_directory+'\\analyze_output.xls')



