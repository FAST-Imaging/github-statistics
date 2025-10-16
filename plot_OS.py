import matplotlib.pyplot as plt
import json
import pandas as pd
import calendar
from datetime import datetime
from style import set_style

set_style(plt)

year = datetime.now().year

with open(f'data/{year}-OS.json', 'r') as file:
    all_data = json.load(file)

fig, ax = plt.subplots(figsize=(10, 6))
previous = None
for OS in all_data.keys():
    data = all_data[OS]

    # Skip first date
    if year == 2025:
        first_date = sorted(data.keys())[0]
        del data[first_date]

    if len(data) == 0:
        continue

    # Per month
    df = pd.DataFrame({'date': pd.to_datetime(list(data.keys())),
                       'downloads': list(data.values())
                       })

    # Fill missing days with 0
    df = df.set_index('date')
    full_date_range = pd.date_range(start=pd.to_datetime(f'{year}-01-01'), end=pd.Timestamp.now(), freq='D')
    df = df.reindex(full_date_range, fill_value=0)

    df['month'] = df.index.to_period('M')
    df['month_name'] = df.index.strftime('%b')
    monthly_data = df.groupby('month')['downloads'].sum().reset_index()
    monthly_data = monthly_data.sort_values(by='month')
    monthly_data['month_name'] = monthly_data['month'].apply(lambda x: calendar.month_abbr[x.month])
    bars = ax.bar(monthly_data['month_name'], monthly_data['downloads'], bottom=previous, label=OS)
    if previous is None:
        previous = monthly_data['downloads']
    else:
        previous += monthly_data['downloads']
plt.title(f'Monthly downloads of FAST GitHub releases per operating system {year}')
plt.legend()
plt.tight_layout()
fig.savefig(f'plots/{year}-OS.svg')
#plt.show()