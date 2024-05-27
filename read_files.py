from typing import List, Dict, Optional
import pandas as pd
import openpyxl as px
from find_files import FindFiles


class ReadExcel:
    def __init__(self, excel_files_paths: Optional[List[str]] = None, intermediate_file_path: Optional[str] = None, svod_file_path: Optional[str] = None) -> None:
        self.files_paths = excel_files_paths
        self._dataframes: Dict[str, pd.DataFrame] = {}
        self.intermediate_file_path = intermediate_file_path
        self.svod_file_path = svod_file_path

    def read_files(self) -> Dict[str, pd.DataFrame]:
        if not self.files_paths:
            return {}
        
        for file_path in self.files_paths:
            self._dataframes[file_path] = pd.read_excel(file_path, header=0)
        return self._dataframes

    def get_intermediate_file(self) -> Optional[pd.DataFrame]:
        if not self.intermediate_file_path:
            return None
        
        return pd.read_excel(self.intermediate_file_path, header=0)
    
    def get_svod_file(self) -> Optional[px.Workbook]:
        if not self.svod_file_path:
            return None
        
        return px.load_workbook(self.svod_file_path)

    @property
    def dataframes(self) -> Dict[str, pd.DataFrame]:
        return self._dataframes
    
    @dataframes.setter
    def dataframes(self, new_dataframes: Dict[str, pd.DataFrame]) -> None:
        if all(isinstance(key, str) and isinstance(value, pd.DataFrame) for key, value in new_dataframes.items()):
            self._dataframes = new_dataframes
        else:
            raise ValueError("All keys must be strings and values must be DataFrames")
        
    def __str__(self) -> str:
        return f"DataFrames: {list(self._dataframes.keys())}"
