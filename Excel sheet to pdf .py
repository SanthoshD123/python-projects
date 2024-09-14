import win32com.client as win32

excel = win32.Dispatch('Excel.Application')

workbook = excel.Workbooks.Open('path_to_your_excel_file.xlsx')

sheet = workbook.Worksheets[1]

sheet.ExportAsFixedFormat(0, 'path_to_save_pdf_file.pdf')

workbook.Close(False)

excel.Quit()
