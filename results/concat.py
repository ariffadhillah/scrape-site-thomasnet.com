import pandas as pd

# List nama file Excel yang akan digabungkan
file_names = ['1.csv', '2.csv', '7.csv']

# Membaca file Excel dan menggabungkannya menjadi satu dataframe
dataframes = []
for name in file_names:
    df = pd.read_csv(name)
    dataframes.append(df)

merged_dataframe = pd.concat(dataframes)

# Menyimpan dataframe menjadi file Excel baru
merged_dataframe.to_excel('merged_file.xlsx', index=False)
