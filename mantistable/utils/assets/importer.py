import datetime
import json


from models.models import TableRve, TableDataRve





def load_table(table_name, file_name, content):
    assert (len(table_name) > 0)
    assert (len(file_name) > 0)
    assert (len(content) > 0)

    json_data = json.loads(content)
    header = list(json_data[0].keys())

    tableRve = TableRve(
        name=table_name,
        file_name=file_name,
        header=header,
        num_cols=len(list(json_data[0].keys())),
        num_rows=len(json_data),
    )



    datas = []
    for col_index in range(0, len(header)):
        data = []
        for i in range(0, len(json_data)):
            col_name = header[col_index]
            if col_name in json_data[i]:
                data.append({
                    "value": json_data[i][col_name]
                })
            else:
                data.append({
                    "value": ""
                })

        datas.append(data)


    tableDataRve = TableDataRve(
        table=tableRve,
        header=header,
        data_original=datas,
        data=datas,

    )

    return [0, tableRve, tableDataRve]

