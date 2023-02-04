

import pandas as pd

# ijournals = ['source:"European Journal of Information Systems"',
#              'source:"Information Systems Journal"',
#              'source:"Information Systems Research"',
#              'source:"Journal of the Association for Information Systems"',
#              'source:"Journal of Information Technology" - source:"International Journal of Information Technology" - source: "Journal of Information Technology &" - source:"Journal of Information Technology and"',
#              'source:"Journal of Management information systems"',
#              'source:"Journal of Strategic Information Systems"',
#              'source:"MIS quarterly"']


df1 = pd.read_excel('data_1.xlsx')
new_column = pd.Series(["European Journal of Information Systems"] * len(df1), name="journal_searched")
df1 = df1.assign(journal_searched=new_column)

df2 = pd.read_excel('data_2.xlsx')
new_column = pd.Series(["Information Systems Journal"] * len(df2), name="journal_searched")
df2 = df2.assign(journal_searched=new_column)

df3 = pd.read_excel('data_3.xlsx')
new_column = pd.Series(["Information Systems Research"] * len(df3), name="journal_searched")
df3 = df3.assign(journal_searched=new_column)

df4 = pd.read_excel('data_4.xlsx')
new_column = pd.Series(["Journal of the Association for Information Systems"] * len(df4), name="journal_searched")
df4 = df4.assign(journal_searched=new_column)

df5 = pd.read_excel('data_5_filtered.xlsx')
new_column = pd.Series(["Journal of Information Technology"] * len(df5), name="journal_searched")
df5 = df5.assign(journal_searched=new_column)

df6 = pd.read_excel('data_6.xlsx')
new_column = pd.Series(["Journal of Management information systems"] * len(df6), name="journal_searched")
df6 = df6.assign(journal_searched=new_column)

df7 = pd.read_excel('data_7.xlsx')
new_column = pd.Series(["Journal of Strategic Information Systems"] * len(df7), name="journal_searched")
df7 = df7.assign(journal_searched=new_column)

df8 = pd.read_excel('data_8.xlsx')
new_column = pd.Series(["MIS quarterly"] * len(df8), name="journal_searched")
df8 = df8.assign(journal_searched=new_column)

df_list = [df1, df2, df3, df4, df5, df6, df7, df8]

df = pd.DataFrame()
for data in df_list:
    df = df.append(data)

print(df)


df = df.dropna()

df.to_excel('data_02032023.xlsx')

