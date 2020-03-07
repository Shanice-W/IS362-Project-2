#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import numpy as np

path_to_file = r"C:\Users\shani\Downloads\Salary Survey.csv"

df = pd.read_csv(path_to_file)

print(df.head())


# In[6]:



df['What industry do you work in?'] = df['What industry do you work in?'].str.strip()

df['Job title'] = df['Job title'].str.strip()

df['What is your annual salary?'] = df['What is your annual salary?'].str.replace(' ', '')

df['What is your annual salary?'] = df['What is your annual salary?'].str.replace(',', '')

df['What is your annual salary?'] = df['What is your annual salary?'].str.extract('(\d+)', expand=False)

df['NumericalSalary'] = df['What is your annual salary?'].str.isdigit()


# In[7]:


new = df["Where are you located? (City/state/country)"].str.split(",", n = 2, expand = True) 

new[0] = new[0].str.strip()

new[1] = new[1].str.strip()

for x in range(len(new)):
    if new[1][x] is not None and len(str(new[1][x])) > 2:
        new[1][x] = None

new[1] = new[1].str.upper() 

print(new.head())


# In[9]:


df['City'] = new[0]
file = r"C:\Users\shani\Downloads\\Normalized Industry.csv"

df2 = pd.read_csv(file)

print(df2.head())


# In[10]:


merge = df.merge(df2, on = 'What industry do you work in?', how = 'left')


# In[11]:


USD = merge[merge['Please indicate the currency'] == 'USD'] 

USD['What is your annual salary?'] = USD['What is your annual salary?'].astype(float)

USDnum = USD[(USD['NumericalSalary'] == True) & (USD['What is your annual salary?'] > 5000)] 

print(USDnum.head())


# In[14]:


industry_salary_avg = pd.pivot_table(USDnum, values='What is your annual salary?', index ='Normalized',
                    aggfunc=np.average, fill_value=0)

industry_salary_avg.reset_index(inplace = True)

industry_salary_avg.sort_values(by = ['What is your annual salary?'], ascending = False, inplace = True)

industry_salary_avg.columns = ['Industry', 'Average Salary (USD)']

print(industry_salary_avg)


# In[13]:


top5 = industry_salary_avg.head(5)

bottom5 = industry_salary_avg.tail(5)


# In[15]:


import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

ax = top5.plot.bar(x = 'Industry', y = 'Average Salary (USD)', rot=0, figsize=(20,10), grid = True, legend=False, title ="Top Five Average Salary by Industry")

fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax.yaxis.set_major_formatter(tick) 
plt.xticks(rotation=25)


# In[16]:


ax2 = bottom5.plot.bar(x = 'Industry', y = 'Average Salary (USD)', rot=0, figsize=(20,10), grid = True, legend=False, title ="Bottom Five Average Salary by Industry")

fmt = '${x:,.0f}'
tick = mtick.StrMethodFormatter(fmt)
ax2.yaxis.set_major_formatter(tick) 
plt.xticks(rotation=25)

