import datetime
import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render


from utils.assets import importer
from normalization.normalize import normalizeRve
from columns_classification import info_tables
from subject_column_detection.sub_detection import SubDetection
from utils.export.format_exporters.csv_exporter import CSVExporter


def index(request):
    context = {}
    return render(request, 'mantistable/index.html', context)



def create_tables(file):

    invalid_file = False
    valid_file = False

    data = file.read()
    file_name = "FileName"
    table_name = "Table Name"

    try:
        listImport = importer.load_table(table_name, file_name, data)
        print("-----------------------------------------------------------------------------------------------------------------")

        print("-----------------------------------------------------------------------------------------------------------------")
        process_directTable(listImport[1], listImport[2])
        # id  tableRve, tableDataRve
    except ValueError as e:
        print(e)
        invalid_file = True



def process_directTable(tableRve, tableDataRve):

    # Faire le complete_table_task revient à faire la normalization + colonne analysis

    # normalize
    normalizeRve(tableRve,tableDataRve)

    #subdetection
    info_tables.set_info_tableRve(tableRve,tableDataRve)
    SubDetection().get_sub_colRve(tableRve,tableDataRve)

    print("La colonne sujet est TADADADADADADA (roulement de tambours) : " )
    print( tableDataRve.infoTableRve.subject_col)

    download_csv(tableRve, tableDataRve)

    #######



def download_csv(tableRve, tableDataRve):
    def build_file_response_download(name_prefix, data, ext):

        date = datetime.datetime.now().strftime("%d_%m_%Y")

        response = HttpResponse(data, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{name_prefix}_{date}.csv"'

        return response

    table = tableRve

    #if table.process['phases'][PhasesEnum.COLUMN_ANALYSIS.value["key"]]['status'] == GlobalStatusEnum.DONE.value:
    #    table = get_object_or_404(Table, id=table_id)
    #    table_data = TableData.objects.get(table=table)
    #    info_table = InfoTable.objects.get(table=table)


    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")

    # Le header n'est pas filtré, on place juste la colonne sujet en premier
    header = table.header
    header.insert(0,header.pop(tableDataRve.infoTableRve.subject_col))
    header = [header]
    print(header)

    # Filter data ? TODO
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


    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")

    result = CSVExporter(table).export()

    #export_format = request.GET.get('export_format', 'csv')

    return build_file_response_download(f"annotations_CSV", result, 'csv')