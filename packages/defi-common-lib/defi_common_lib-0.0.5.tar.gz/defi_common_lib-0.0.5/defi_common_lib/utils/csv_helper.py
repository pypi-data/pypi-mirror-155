import os
import csv
import codecs
from io import StringIO
import sys


class CsvHelper:

    @staticmethod
    def create_csv(data):

        file = StringIO()
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        file.seek(0)

        return file

    @staticmethod
    def write_csv_from_s3_content(data, path, file_name):

        rows = []
        for row in csv.DictReader(codecs.getreader("utf-8")(data["Body"])):
            rows.append(row)

        keys = rows[0].keys()

        with open(os.path.join(path, file_name), 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(rows)


    @staticmethod
    def get_file_size_content(file: any):
        file_size = sys.getsizeof(file)
        file_content = file.getvalue()

        return file_size, file_content