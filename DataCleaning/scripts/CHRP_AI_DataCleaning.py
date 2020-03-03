#!/usr/bin/env python
# coding: utf-8

import pandas as pd


filepath = '../data/Load_Data_Full_ChillerValuesOnly.csv'
rel_data = pd.read_csv(filepath)


# In[ ]:


rel_data.head()


# ### Find Outliers
# Use 1 hour interval (15 points before and 15 points after current point)
# 
# For points with only N points before (w/ N < 15), use N points before and 30-N points after.<br>
# For points with only N points after (w/ N < 15), use N points after and 30-N points before.

# In[ ]:


outlier_cols = []
for x in rel_data.columns[1:]:
    outlier_col = [0 for i in range(len(rel_data))]
    for i in range(len(rel_data)):
        if i < 15:
            window = rel_data.loc[0:29,x]
            q1 = window.quantile(0.25)
            q3 = window.quantile(0.75)
            iqr = abs(q3 - q1)
            if ((rel_data.loc[i,x] < q1 - 1.5 * iqr) or (rel_data.loc[i,x] > q3 + 1.5 * iqr)):
                outlier_col[i] = 1
        elif i > len(rel_data) - 15:
            window = rel_data.loc[len(rel_data) - 30:len(rel_data) - 1,x]
            q1 = window.quantile(0.25)
            q3 = window.quantile(0.75)
            iqr = abs(q3 - q1)
            if ((rel_data.loc[i,x] < q1 - 1.5 * iqr) or (rel_data.loc[i,x] > q3 + 1.5 * iqr)):
                outlier_col[i] = 1
        else:
            window = rel_data.loc[i-15:i+14,x]
            q1 = window.quantile(0.25)
            q3 = window.quantile(0.75)
            iqr = abs(q3 - q1)
            if ((rel_data.loc[i,x] < q1 - 1.5 * iqr) or (rel_data.loc[i,x] > q3 + 1.5 * iqr)):
                outlier_col[i] = 1
    outlier_cols.append(outlier_col)


# In[ ]:


rel_data.columns


filepath = '../data/cleanLoadData.csv'
rel_data.to_csv(filepath)





