#!/usr/bin/env python
# coding: utf-8

# In[2]:


un_dataframe = pd.read_excel(
    'UN_MigrantStockByOriginAndDestination_2015.xlsx',
    sheet_name='Table 15',
    skiprows=15
)


# In[3]:


un_dataframe.rename(
    columns={
        'Unnamed: 3': 'Destination Country Code',
        'Unnamed: 1': 'Destination Country'
    },
    inplace=True
)


# In[4]:


un_dataframe = un_dataframe[un_dataframe['Unnamed: 4'].notna()]


un_dataframe.drop(['Unnamed: 0', 'Unnamed: 2', 'Unnamed: 4', 'Total'],
                  axis=1,
                  inplace=True)


# In[ ]:


un_dataframe = un_dataframe.melt(
    id_vars=['Destination Country', 'Destination Country Code'],
    value_name='People',
    var_name='Origin Country'
)


# In[ ]:


singapore_migrants = un_dataframe[
    un_dataframe['Destination Country'] == 'Singapore'
]


singapore_migrants_top_origin = singapore_migrants.sort_values(
    'People', ascending=False
).head(10)


singapore_migrants_top_origin['Origin Country'].replace(
    to_replace='China, Hong Kong Special Administrative Region',
    value='Hong Kong',
    inplace=True
)

singapore_migrants_top_origin.plot.bar(
    x='Origin Country',
    y='People',
    title='Origin Countries of Migrants to Singapore in 2010')

plt.tight_layout()
plt.savefig('top_origin_countries_migrants_singapore_2010.png',
            dpi=150)

