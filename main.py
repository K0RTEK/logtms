from find_files import FindFiles
from read_files import ReadExcel
from modify_files import DataFrameProcessor, SvodTable


def start(root_directory, intermediate_file_path, svod_excel_file_path) -> None:

    files = FindFiles(root_directory)
    files.find_paths()

    excel_dataframes = ReadExcel(files.paths, intermediate_file_path=intermediate_file_path, svod_file_path=svod_excel_file_path)
    excel_dataframes.read_files()

    excel_dataframes.dataframes["297 TE Germany"] = excel_dataframes.dataframes.pop("D:\\logtms\\№_297_TE_Germany_24_12_Цзиньхуа_Малашевиче_Jinhua_WB1224\\7084-087-1306 Мала ОТЛК- 297.xlsx")
    excel_dataframes.dataframes["Цзиньхуа Малашевиче Jinhua WB1224"] = excel_dataframes.dataframes.pop("D:\\logtms\\№_297_TE_Germany_24_12_Цзиньхуа_Малашевиче_Jinhua_WB1224\\Лист перегруза 674 Сиань-Будапешт.xlsx")

    intermediate_file = excel_dataframes.get_intermediate_file()
    svod_workbook = excel_dataframes.get_svod_file()

    modify = DataFrameProcessor(excel_dataframes.dataframes, intermediate_dataframe=intermediate_file)
    res = modify.update_intermediate_file()
    modify.save_intermediate_file(intermediate_file_path)

    modify_svod_table = SvodTable(svod_workbook, worksheet_name="WB", intermediate_file=res)
    modify_svod_table.create_data_string()
    modify_svod_table.insert_data([['Алтынколь', 'СП', 297, 'TE Germany GmbH', 'Сиань', 'БЕЛЫЙ РАСТ', 'ТК № 297', 54, 31, 'BEAU5694302', 'БЕЛЫЙ РАСТ', '', '7084-087-1306', 1268, '27.12.2023 23:35:00', '28.12.2023 07:12:00', '03.01.2024 17:25', '1в1', '1в1']])
    modify_svod_table.save_workbook(svod_excel_file_path)

if __name__ == "__main__":
    start()
