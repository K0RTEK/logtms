from find_files import FindFiles
from read_files import ReadExcel
from modify_files import DataFrameProcessor, SvodTable


def start(root_directory, intermediate_file_path, svod_excel_file_path) -> None:

    files = FindFiles(root_directory)
    files.find_paths()

    excel_dataframes = ReadExcel(files.paths, intermediate_file_path=intermediate_file_path, svod_file_path=svod_excel_file_path)
    excel_dataframes.read_files()
    print(excel_dataframes.files_paths)

    excel_dataframes.dataframes["297 TE Germany"] = excel_dataframes.dataframes.pop(excel_dataframes.files_paths[0])
    excel_dataframes.dataframes["Цзиньхуа Малашевиче Jinhua WB1224"] = excel_dataframes.dataframes.pop(excel_dataframes.files_paths[1])

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
