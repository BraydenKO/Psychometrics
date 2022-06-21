from reader import df, pd

# The data is actually all in just one column
# Split into multiple columns
columns = df.columns[0].split('\t"')

# Clean up that trailing "
for i in range(len(columns[1:])):
    columns[i+1] = columns[i+1][:-1]

quit()
new_df = pd.DataFrame(columns = columns)

for i in range(len(df)):
    row = df.iloc[i][0].split("\t")
    new_df.loc[i] = row
    
    if i%1000 == 0:
        print(i)

print(new_df)
new_df.to_csv(r"Docs\16PF/data_fix.csv", index = False)