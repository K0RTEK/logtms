from glob import glob
from typing import List

class FindFiles:
    def __init__(self, root_directory: str) -> None:
        self._paths: List[str] = []
        self.root_directory = root_directory
    
    def find_paths(self) -> List[str]:
        self._paths = glob(f"{self.root_directory}\\*[0-9][0-9][0-9]*.xlsx")
        return self._paths

    @property
    def paths(self) -> List[str]:
        return self._paths

    @paths.setter
    def paths(self, new_paths: List[str]) -> None:
        if all(isinstance(path, str) for path in new_paths):
            self._paths = new_paths
        else:
            raise ValueError("All paths must be strings")

    def __str__(self) -> str:
        return str(self._paths)
    

if __name__ == '__main__':
    pass