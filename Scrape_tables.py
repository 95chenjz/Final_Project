import requests
import pandas as pd

from bs4 import BeautifulSoup

def get_prob_table(url):

    page = requests.get(url)
    html = page.content

    soup = BeautifulSoup(html, 'lxml')

    tables = soup.find_all('table',{'class':'wikitable'})
    tb = tables[3]

    df = pd.DataFrame(0,index = range(0,7),columns=['Expansion','Total','Common','Rare','Epic','Legendary',\
                      'Golden_Total','Golden_Common','Golden_Rare','Golden_Epic',\
                      'Golden_Legendary'])

    df.Expansion = [head.contents[0] for head in tb.find_all('th')[14:21]]

    for i, row in enumerate(tb.find_all('tr')[2:9]):
        tdx = [val for val in row.find_all('td')[1:]]
        df.iloc[i:i+1,1:] = [float(i.contents[0].strip().strip('%'))/100 for i in tdx]

    return df


url = 'https://hearthstone.gamepedia.com/Card_pack_statistics'
prob_table = get_prob_table(url)
