import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import date

url = "https://www.worldometers.info/coronavirus/"
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'lxml')
table = soup.find('table', class_='table').find('tbody')

A=[]
B=[]
C=[]
D=[]

for row in table.find_all('tr'):
    cells = row.find_all('td')
    A.append(cells[0].find(text=True))
    B.append(cells[1].find(text=True))
    C.append(cells[3].find(text=True))
    D.append(cells[6].find(text=True))

df=pd.DataFrame(A,columns=['Country, Other'])
df['Total Cases']=B
df['Total Deaths']=C
df['Total Recovered'] =D

df.replace(',','', regex=True, inplace=True)
df.replace(' ',0, inplace=True)
df.loc[df['Country, Other'] == 0, 'Country, Other'] = ' Diamond Princess '
df[['Total Cases','Total Deaths','Total Recovered']] = df[['Total Cases','Total Deaths','Total Recovered']].apply(pd.to_numeric)

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.075,
    subplot_titles=("Table of Worldwide COVID-19 Cases","Top 10 Cases Outside China"),
    specs=[[{"type": "table"}], [{"type": "bar"}]])

fig.add_trace (go.Table(
	header=dict(values=list(df.columns),
                fill_color='lightsteelblue',
                line_color='black',
                align=['left','center'],
                font_size=14,
   				height=30),
    cells=dict(values=[df['Country, Other'], df['Total Cases'], df['Total Deaths'], df['Total Recovered']],
               fill_color='white',
               line_color='black',
               align=['left','center'],
               font_size=12,
   			   height=30)),
    row=1, col=1)

fig.add_trace (go.Bar(
        x=df[1:11]["Country, Other"],
        y=df[1:11]["Total Cases"],
        name="Total Cases", text= df[1:11]["Total Cases"], textposition='auto'
    ),
    row=2, col=1)

fig.add_trace (go.Bar(
        x=df[1:11]["Country, Other"],
        y=df[1:11]["Total Deaths"],
        name="Total Deaths", text= df[1:11]["Total Deaths"], textposition='outside'
    ),
    row=2, col=1)

fig.add_trace (go.Bar(
        x=df[1:11]["Country, Other"],
        y=df[1:11]["Total Recovered"],
        name="Total Recovered", text= df[1:11]["Total Recovered"], textposition='outside'
    ),
    row=2, col=1)

today = date.today()

fig.update_layout(title_text="Countries/Clusters Affected by COVID-19 Cases as of " + today.strftime("%d %b %Y"))
fig.show()

df.to_csv('Covid19Tally.csv', index=False)