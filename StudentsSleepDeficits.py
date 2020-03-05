import pandas as pd
import plotly
from plotly.offline import plot, iplot
import plotly.graph_objs as go
import datadotworld as dw

results = dw.query(
	'makeovermonday/2020w9', 
    'SELECT * FROM week9mm')
df = results.dataframe

trace1 = go.Bar(name='Hours Needed', x=df['grade'], y=df['hours_needed'])
trace2 = go.Bar(name='Hours Averaged', x=df['grade'], y=df['hours_averaged'])
data = [trace1, trace2]

fig = go.Figure(data= data)
fig.update_layout(title_text="Students' Sleep Deficits", yaxis_title = 'No. of Hours of Sleep')
fig.show()
