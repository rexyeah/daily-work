import dryscrape
#from bs4 import BeautifulSoup as bs

FUTURE_URL = 'http://www.taifex.com.tw/chinese/3/7_12_3.asp'
STOCK_URL = 'http://www.tse.com.tw/ch/trading/exchange/MI_MARGN/MI_MARGN.php'

session = dryscrape.Session()


# FI: Foreign Investor(s)
# IT: Investment Trust
# DL: Dealer
TXF_FI_OI = 0
TXF_IT_OI = 0
TXF_DL_OI = 0


#response = session.body()
#html = bs(response, 'html.parser')


def get_FUTURE_OI(session, types):
    script_str='document.querySelector(' \
    '"table .table_f tr:nth-child({types}) td:nth-child(12)"' \
    ').innerText'.format(types={
        'TXF':6,
        'EXF':9,
        'FXF':12
        }[types]
    )
    return int(session.eval_script(script_str).replace(',', ''))


def get_loan(session, types):
    script_str = 'document.querySelectorAll("table")[3]' \
        '.querySelector("tbody tr:nth-child({types}) td:nth-child(6)")' \
        '.innerText'.format(types={
            'margin_loan': 1,
            'stock_loan': 2,
            'margin': 3
        }[types]
    )
    return int(session.eval_script(script_str).replace(',', ''))


# The balance of margin loan and stock loan

session.visit(STOCK_URL)
MARGIN_LOAN = get_loan(session, 'margin_loan')
STOCK_LOAN = get_loan(session, 'stock_loan')
MARGIN = get_loan(session, 'margin')

session.visit(FUTURE_URL)
TXF_FI_OI=get_FUTURE_OI(session, 'TXF')

print MARGIN_LOAN, STOCK_LOAN, MARGIN
print TXF_FI_OI
