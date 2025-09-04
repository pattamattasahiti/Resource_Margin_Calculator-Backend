import pandas as pd
import tempfile

def make_excel(employee_data_list):
    df = pd.DataFrame(employee_data_list)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    with pd.ExcelWriter(tmp.name, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return tmp.name
