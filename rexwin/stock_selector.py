'''
generate YESWIN DDE code in a time.
TODO: Check website datetime info and download the latest xls file
'''

# v 1. download xls file
# v 2. convert the xls file to a csv file
# v 3. remove the xls file
# 4. copy data from the stock.csv to the money.xls
# 5. Update the xls DDE link and filter the stock

import os
import unicodecsv
import wget
import xlrd
import xlwt

BASE_DIR = '/home/linrex/Dropbox'
SF_XLS = os.path.join(BASE_DIR, 'sf.xls')
SF_CSV = os.path.join(BASE_DIR, 'sf.csv')
SELECTED_CSV = os.path.join(BASE_DIR, 'sf_selected.csv')


def download_sf_excel():
    wget.download(
        url='https://www.taifex.com.tw/chinese/2/2_stockinfo.xls',
        out=SF_XLS
    )


def convert_excel_to_csv():
    wb = xlrd.open_workbook(SF_XLS)
    sh = wb.sheet_by_name('STF&STO')
    csv_file = open(SF_CSV, 'wb')
    wr = unicodecsv.writer(csv_file, quoting=unicodecsv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))
    csv_file.close()
    os.remove(SF_XLS)


def convert_csv_to_yeswin_dde():
    sf = open(SF_CSV)
    sf_data = ''
    for s in sf:
        if "2000.0" in s.strip():
            code = s.strip().split(',')[2][1:5]
            if code.isdigit():
                sf_data += "{code}," \
                    "=YES|DQ!'{code}.Name'," \
                    "=YES|DQ!'{code}.Price'," \
                    "=YES|DQ!'{code}.Open'," \
                    "=YES|DQ!'{code}.High'," \
                    "=YES|DQ!'{code}.Low'," \
                    "=YES|DQ!'{code}.Amount'," \
                    "=YES|DQ!'{code}.ChangePercent'\n".format(code=code)
    sf.close()
    f = open(SELECTED_CSV, 'w')
    f.write(sf_data)
    f.close()
    os.remove(SF_CSV)

download_sf_excel()
convert_excel_to_csv()
convert_csv_to_yeswin_dde()
