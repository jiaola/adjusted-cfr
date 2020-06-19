import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px

def adjusted_cfr():

    url = 'https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/Race-Ethnicity.aspx'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    headers = ['Total', None, '0-17', '18-34', '35-49', '50-64', '64-79', '80+']
    tables = soup.find_all(class_='ms-rteTable-4')
    cal = {}
    c = {}
    f = {}
    for i in range(8):
        header = headers[i]
        if header is None:
            continue
        table = tables[i]
        cr = []
        fr = []
        for j, row in enumerate(table.find('tbody').find_all('tr')):
            if j not in [1, 2, 3, 4, 9]:
                continue
            cols = row.find_all('td')
            cr.append(int(cols[1].text.strip('\u200b').replace(',', '')))
            fr.append(int(cols[3].text.strip('\u200b').replace(',', '')))
        c[header] = cr
        f[header] = fr

    cases = pd.DataFrame.from_dict(c, orient='index', columns=['Hispanic', 'White', 'Asian', 'Black', 'Total'])
    deaths = pd.DataFrame.from_dict(f, orient='index', columns=['Hispanic', 'White', 'Asian', 'Black', 'Total'])
    print(cases)
    print(deaths)

    cfr = deaths / cases
    print(cfr)
    adjusted_deaths = cfr.multiply(cases['Total'], axis='index')
    adjusted_deaths = adjusted_deaths.drop(['Total'])
    adjusted_deaths.loc['Total'] = adjusted_deaths.sum()
    print(adjusted_deaths)

    ajusted_cfr = adjusted_deaths.divide(cases['Total'], axis='index')
    print(ajusted_cfr)

    df = pd.melt(pd.DataFrame([cfr.loc['Total', 'Hispanic':'Black']]))
    df = df.rename(columns={'variable': 'Race', 'value': 'CFR'})
    df['Group'] = 'Reported'

    adf = pd.melt(pd.DataFrame([ajusted_cfr.loc['Total', 'Hispanic':'Black']]))
    adf = adf.rename(columns={'variable': 'Race', 'value': 'CFR'})
    adf['Group'] = 'Adjusted'

    df = pd.concat([df, adf])

    # df = pd.DataFrame(ts, columns=['Race', 'CFR', 'Group'])
    fig = px.bar(df, x='Race', y='CFR', color='Group', barmode='group')
    return fig, cases, deaths, cfr, ajusted_cfr


# Calculate the total

