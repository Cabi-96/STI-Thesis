

class TableRve:
    def __init__(self, name, file_name, header, num_cols, num_rows):
        self.name = name
        self.file_name = file_name
        self.header = header
        self.num_cols = num_cols
        self.num_rows = num_rows


        def __str__(self):
            return self.name


class TableDataRve:
    def __init__(self, table, header,data_original , data):
        self.table = table
        self.header = header
        self.data_original = data_original
        self.data = data
        self.infoTableRve = None

    def set_infoTable (self,table, table_name, lit_cols, ne_cols, no_ann_cols):
        # idealement il faut construire la table ici plutot que de la passer
        self.infoTableRve = InfoTableRVE(table, table_name, lit_cols, ne_cols, no_ann_cols)



class InfoTableRVE:
    def __init__(self, table, table_name, lit_cols, ne_cols, no_ann_cols):
        self.table = table
        self.table_name = table_name
        self.lit_cols = lit_cols
        self.ne_cols = ne_cols
        self.no_ann_cols = no_ann_cols
        self.subject_col = 0
        self.subject_cols_paper = []



