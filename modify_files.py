from typing import List, Dict, Any
import pandas as pd
import openpyxl as px
import re

class DataFrameProcessor:
    def __init__(self, 
                 dataframes: Dict[str, pd.DataFrame], 
                 intermediate_dataframe: pd.DataFrame) -> None:
        self.dataframes = dataframes
        self.intermediate_dataframe = intermediate_dataframe

    def find_columns(self, dataframe: pd.DataFrame) -> List[int]:
        columns: List[int] = []
        pattern_container: str = r'[A-Z]{4}[0-9]{7}'
        pattern_train_index: str = r'[0-9]{4}-[0-9]{3}-[0-9]{4}'

        for idx, col in enumerate(dataframe.iloc[1].values):
            if re.search(pattern_container, str(col)) or re.search(pattern_train_index, str(col)):
                columns.append(idx)

        if len(columns) <= 1:
            raise ValueError("Найдены не все колонки в датафрейме")
        
        return columns

    def update_intermediate_file(self) -> pd.DataFrame:
        mapped_columns: Dict[str, List[int]] = {}
        main_df_columns = self.find_columns(self.intermediate_dataframe)
        main_df_copy = self.intermediate_dataframe.iloc[:, main_df_columns].copy()

        for df_name, df in self.dataframes.items():
            mapped_columns[df_name] = self.find_columns(df)

        for df_name, df in self.dataframes.items():
            self.dataframes[df_name] = df.iloc[:, mapped_columns[df_name]]
            self.dataframes[df_name].columns = main_df_copy.columns

        for df_name, df in self.dataframes.items():
            df["Название"] = df_name

        for df_name, df in self.dataframes.items():
            self.intermediate_dataframe = self.intermediate_dataframe.merge(
                df, 
                on=list(df.columns[:-1]), 
                how='left'
            )

        cols_to_concat = self.intermediate_dataframe.columns[-len(self.dataframes):]

        self.intermediate_dataframe['E'] = self.intermediate_dataframe[cols_to_concat].fillna('').astype(str).apply(
            lambda x: ' '.join(x), axis=1
        )
        self.intermediate_dataframe.drop(cols_to_concat, axis=1, inplace=True)
        
        return self.intermediate_dataframe

    def __str__(self) -> str:
        return str(self.intermediate_dataframe)
    

class SvodTable:
    def __init__(self, workbook: px.Workbook, worksheet_name: str, intermediate_file: pd.DataFrame) -> None:
        self.workbook = workbook
        self.worksheet_name = worksheet_name
        self.intermediate_file = intermediate_file


    def create_data_string(self):
        station = []
        terminal = []
        order = []
        client = []
        departure_point = []
        destination_point = []
        numeration = []
        container = []
        wagons = []
        containers_not_shipped = []
        destination_station = []
        pkp_carrier = []
        train_index = []
        train_number = []

        unique_df = self.intermediate_file.drop_duplicates(subset='E')

        for val in unique_df["Индекс поезда"].values:
            if str(val)[2:4] == "84":
                station.append("Достык")
            else:
                station.append("Алтынколь")

        for val in unique_df["E"].values:
            curr = val.split(" ")
            order.append(curr[0])

        # station.append()

        

    def find_last_row(self):
        row_index = 1
        for row in self.workbook[self.worksheet_name].iter_rows(min_col=1, max_col=1, min_row=1):
            if row[0].value is None:
                break
            else:
                row_index += 1
        
        return row_index
    
    def insert_data(self, data: List[List[Any]]):
        last_row_idx = self.find_last_row()

        for df_row in data:
            for col_index, value in enumerate(df_row, start=1):
                self.workbook[self.worksheet_name].cell(row=last_row_idx, column=col_index, value=value)
            last_row_idx += 1

    def save_workbook(self):
        self.workbook.save("new_svod.xlsx")