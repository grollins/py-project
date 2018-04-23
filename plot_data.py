import matplotlib
matplotlib.use('agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
plt.style.use('seaborn-deep')

import pandas as pd
import seaborn as sns


ax = (df.set_index('ticker')
        .loc[['MSFT', 'AAPL', 'AXP', 'V']]
        .query("date >= '2018-01-01'")
        .drop_duplicates()
        .pivot(index='date', columns='name', values='price')
        .plot())

ax.xaxis.set_major_locator(mdates.WeekdayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

plt.savefig('test.png')
