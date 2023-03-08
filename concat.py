import pandas as pd
import os

# Menentukan path folder yang berisi file Excel
folder_path = os.path.abspath('path/to/results/')

# Membuat list nama file Excel dalam folder
file_names = os.listdir(folder_path)

# Membaca setiap file Excel dan menggabungkannya menjadi satu dataframe
dataframes = []
for name in file_names:
    if name.endswith('.xlsx'):  # Membaca hanya file Excel dengan ekstensi .xlsx
        path = os.path.join(folder_path, name)
        df = pd.read_excel(path)
        dataframes.append(df)

merged_dataframe = pd.concat(dataframes)

# Menyimpan dataframe menjadi file Excel baru
merged_dataframe.to_excel('merged_file.xlsx', index=False)
