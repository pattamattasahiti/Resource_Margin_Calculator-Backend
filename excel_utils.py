import xlsxwriter
import tempfile

def make_excel(employee_data_list):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    workbook = xlsxwriter.Workbook(tmp.name)
    worksheet = workbook.add_worksheet()
    
    if not employee_data_list:
        workbook.close()
        return tmp.name
    
    # Write headers
    headers = list(employee_data_list[0].keys())
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    
    # Write data
    for row_num, employee in enumerate(employee_data_list, start=1):
        for col, header in enumerate(headers):
            worksheet.write(row_num, col, employee.get(header, ""))
    
    workbook.close()
    return tmp.name
