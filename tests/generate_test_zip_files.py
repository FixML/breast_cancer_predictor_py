import pytest
import os
import openpyxl
import zipfile
import shutil

# Create a directory named 'subdir'
os.makedirs('subdir', exist_ok=True)

# Create 'test1.txt' and write "test data" to it
with open('test1.txt', 'w') as file:
    file.write('test data')

# Create 'test2.txt' inside 'subdir' and write "test data" to it
with open('subdir/test2.txt', 'w') as file:
    file.write('test data')

# Create 'test1.xlsx' and write "test data" to it
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet.cell(row=1, column=1, value='test data')
workbook.save('test1.xlsx')

# Case 1 - Create a zip file containing 'test1.txt' and 'test1.xlsx'
with zipfile.ZipFile('files_txt_xlsx.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('test1.txt')
    zipf.write('test1.xlsx')

# Case 2 - Create a zip file containing 'test1.txt' and 'subdir/test2.txt'
with zipfile.ZipFile('files_txt_subdir.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('test1.txt')
    zipf.write('subdir/test2.txt')

# Case 3 - Create an empty zip file
with zipfile.ZipFile('empty.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    pass

# Clean up the files and directories created
test_files = ['test1.txt', 'test1.xlsx']

for file in test_files:
    if os.path.exists(file):
        os.remove(file)

if os.path.exists("subdir"):
    shutil.rmtree("subdir")
