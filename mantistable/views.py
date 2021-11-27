import datetime
import os
import pandas as pd

from mantistable.utils.assets import importer
from mantistable.normalization.normalize import normalizeRve
from mantistable.columns_classification import info_tables
from mantistable.subject_column_detection.sub_detection import SubDetection
from mantistable.utils.export.format_exporters.csv_exporter import CSVExporter


def get_subject_index_mantistable(file_csv):
    # convert to json
    file_json = convert_to_json(file_csv)
    # open file
    f = open(file_json, "r")
    column_subject_index = 0

    # get subject column index
    try:
        column_subject_index = get_index_and_create_tables(f)
    except:
        print("Error in get_subject_index_mantistable(file_csv)")
    finally:
        # remove file
        if os.path.exists(file_json):
            f.close()
            os.remove(file_json)

    return column_subject_index




def convert_to_json(file_csv):
    head, tail = os.path.split(file_csv)
    file_name, file_extension = os.path.splitext(tail)

    file_json = os.path.join(head,file_name+".json")
    #print(file_json)

    # convert to json
    df = pd.read_csv(file_csv)
    df.to_json(file_json, orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)


    return file_json


def get_index_and_create_tables(file):

    invalid_file = False
    valid_file = False
    subject_index= 0

    data = file.read()
    #TODO get file name
    file_name = "FileName"
    table_name = "Table Name"

    try:
        listImport = importer.load_table(table_name, file_name, data)
        subject_index = get_subject_index_column(listImport[1], listImport[2])
        # id  tableRve, tableDataRve
    except ValueError as e:
        print(e)
        invalid_file = True

    return subject_index




def get_subject_index_column(tableRve, tableDataRve):


    subject_index = 0

    # normalize
    normalizeRve(tableRve,tableDataRve)

    #subdetection
    info_tables.set_info_tableRve(tableRve,tableDataRve)
    SubDetection().get_sub_colRve(tableRve,tableDataRve)
    subject_index = tableDataRve.infoTableRve.subject_col

    return subject_index

    #######


# download doesnt work, TODO
def download_csv(tableRve, tableDataRve):
    def build_file_response_download(name_prefix, data, ext):

        date = datetime.datetime.now().strftime("%d_%m_%Y")

        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{name_prefix}_{date}.csv"'

        return response

    table = tableRve


    print("TODO")

    # Le header n'est pas filtré, on place juste la colonne sujet en premier
    header = table.header
    header.insert(0,header.pop(tableDataRve.infoTableRve.subject_col))
    header = [header]
    #print(header)

    # Error to export TODO
    # On recupère les données de la table
    data = [
        [
            col[row_idx]["value"]
            for col_idx, col in enumerate(table)
        ] for row_idx in range(0, table.num_rows)
    ]

    #On place la colonne sujet en premier pour chaque ligne de la table
    for row in data:
        row.insert(0,row.pop(tableRve.infoTableRve.data.subject_col))


    table = header + data


    result = CSVExporter(table).export()

    #export_format = request.GET.get('export_format', 'csv')

    return build_file_response_download(f"annotations_CSV", result, 'csv')