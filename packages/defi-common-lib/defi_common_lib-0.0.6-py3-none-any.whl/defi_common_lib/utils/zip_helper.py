from zipfile import ZipFile
import os
from os.path import basename


class ZipHelper:
    
    @staticmethod
    def zip_files_in_dir(self, path: str, file_name: str) -> None:

        with ZipFile(os.path.join(self.path, self.file_name), 'w') as zip_file:
            print(f'Packing files at {self.path}')
            for folder_name, _, file_names in os.walk(self.path):
                print(f'Adding {file_names} to zip')
                for file_name in file_names:
                    if 'zip' not in file_name:
                        print(f'Adding {file_name} to zip')
                        file_path = os.path.join(folder_name, file_name)
                        zip_file.write(file_path, basename(file_path))

            zip_file.close()
