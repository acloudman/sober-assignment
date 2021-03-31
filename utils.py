import csv

FILE_PATH = "bank_unified_data.csv"


class CSVUtill:

    def __init__(self, path=None):
        self.path = path

    def read_csv(self):
        """
        read csv file
        input: csv file
        output: file
        """
        final_data = []
        with open(self.path) as csv_file:
            line_count = 0
            csv_reader = csv.reader(csv_file, delimiter=',')
            header = None
            for row in csv_reader:
                if line_count == 0:
                    header = row
                else:
                    final_data.append(dict(zip(header, row)))
                line_count += 1

        return final_data

    def write_csv(self, save_file_path=None, data_to_write=None, header=None):
        if not save_file_path:
            save_file_path = FILE_PATH

        with open(save_file_path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(header)

            for data in data_to_write:
                writer.writerow(data)
