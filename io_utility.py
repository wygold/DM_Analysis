__author__ = 'ywang'

from xlwt import *


#define format for excel file
TABLE_HEADER_FORMAT = easyxf(
    'font: bold 1, name Tahoma, height 160;'
    'align: vertical center, horizontal center, wrap on;'
    'borders: left thin, right thin, top thin, bottom thin;'
    'pattern: pattern solid, pattern_fore_colour yellow, pattern_back_colour yellow'
)

TITLE_FORMAT = easyxf(
    'font: bold 1, name Tahoma, height 220;'
    'align: vertical center, horizontal center, wrap on;'
    'borders: left thin, right thin, top thin, bottom thin;'
    'pattern: pattern solid, pattern_fore_colour gray25, pattern_back_colour gray25'
)

TEXT_FORMAT = easyxf(
    'font: bold 1, name Roma, height 160;'
    'align: vertical center, horizontal center, wrap on;'
    'borders: left thin, right thin, top thin, bottom thin;'
    'pattern: pattern solid, pattern_fore_colour white, pattern_back_colour gray25'
)

HIGHLIGHTED_TEXT_FORMAT = easyxf(
    'font: bold 1, name Roma, height 160;'
    'align: vertical center, horizontal center, wrap on;'
    'borders: left thin, right thin, top thin, bottom thin;'
    'pattern: pattern solid, pattern_fore_colour red, pattern_back_colour gray25'
)

def read_txt(filename):
    pass

def write_txt(filename):
    pass

def read_csv(filename):
    pass

def write_csv(content, filename):
    pass

def add_worksheet(content, workbook, sheetname, highlighted=False):
    ws = workbook.add_sheet(sheetname)

    i = 0
    j = 0
    title = ''

    if highlighted==False:
        for row in content:
            for cell in row:
                if i >= 1 and j < 12 and ws.col(j).width < len(cell) * 300:
                    ws.col(j).width = len(cell) * 320
                if i == 0:
                    title = str(cell)
                elif i == 1:
                    if j == 0:
                        ws.write_merge(0, 0, 0, len(row) - 1, title, TITLE_FORMAT)
                    ws.write(i, j, str(cell), TABLE_HEADER_FORMAT)
                else:
                    ws.write(i, j, str(cell), TEXT_FORMAT)
                j = j + 1
        j = 0
        i = i + 1
    else:
        for row in content:
            highlighted = row[-1]
            for cell in row:
                if i>=1 and j < 12 and ws.col(j).width < len(cell)*300 :
                    ws.col(j).width = len(cell)*320
                if i == 0 :
                    title = str(cell)
                elif i == 1 :
                    if j ==  0:
                        ws.write_merge(0,0,0,len(row)-1, title,TITLE_FORMAT)
                    ws.write(i, j, str(cell),TABLE_HEADER_FORMAT)
                elif j == len(row) - 1:
                    break
                elif highlighted=='True':
                    ws.write(i, j, str(cell),HIGHLIGHTED_TEXT_FORMAT)
                else:
                    ws.write(i, j, str(cell),TEXT_FORMAT)
                j = j + 1
            j = 0
            i = i + 1

    return workbook

def save_workbook(workbook,output_file):
    workbook.save(output_file)


