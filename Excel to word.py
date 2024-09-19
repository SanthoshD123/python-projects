import openpyxl
from docxtpl import DocxTemplate

# Load the Excel workbook and select the active sheet
wb = openpyxl.load_workbook('data.xlsx')
sheet = wb.active

# Load the Word template
doc = DocxTemplate('template.docx')

# Create a context dictionary from the Excel data
context = {}
for row in sheet.iter_rows(min_row=2, values_only=True):
    context[row[0]] = row[1]

# Render the Word document with the context data
doc.render(context)

# Save the generated Word document
doc.save('output.docx')
