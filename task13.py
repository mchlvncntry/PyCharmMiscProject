import numpy as np
from datascience import *
import matplotlib
# %matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import datetime
from datetime import datetime, date

import datetime
from datetime import datetime, date



unemployment = Table().read_table('/Users/mvrayo-mini/Downloads/materials-fa24/hw/hw03/unemployment.csv')



def update_date_format(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%d').date()
    return date_object

if not isinstance(unemployment.column('DATE').item(0),  date):
    unemployment = unemployment.with_column(
        'DATE', unemployment.apply(update_date_format, 'DATE'))
    print("The date type for the values in the 'DATE' column have been updated.\n")
else:
    print("The date type is correct for the values in the 'DATE' column.\n")

print(unemployment)
print("...LINE BREAKER...")
by_nei = unemployment.sort('NEI',descending=True)
# by_nei_pter = by_nei.sort(by_nei.column('NEI+PTER'),descending=True)
by_nei_pter = unemployment.sort('NEI+PTER',descending=True)
print("by_nei_pter")
print(by_nei_pter)
print("...LINE BREAKER...\n\n")

greatest_nei = by_nei.take(np.arange(10))
print("greatest_nei")
print(greatest_nei)
print("...LINE BREAKER...\n\n")

pter = np.array(abs(unemployment.column("NEI")-unemployment.column("NEI+PTER")))
print("pter")
print(pter)
print("...LINE BREAKER...\n\n")

unemployment = unemployment.with_column("PTER", pter)
unemployment = unemployment.sort("DATE")
print("unemployment")
print(unemployment)
print("...LINE BREAKER...\n\n")

#unemployment.show(2)

last_row_index = unemployment.num_rows - 1
nei_pter_data = unemployment.column("NEI+PTER")
nei_pter_diffs = np.diff(nei_pter_data)
# NEI_PTER_change = np.round((nei_pter_diffs / unemployment.exclude(last_row_index).column("NEI+PTER")),4)
NEI_PTER_change = nei_pter_diffs / unemployment.exclude(last_row_index).column("NEI+PTER")
np.set_printoptions(suppress=True, precision=4)
print("NEI_PTER_change")
print(NEI_PTER_change)

