import json
from abc import ABC, abstractmethod

from utils import CSVUtill


class BankTable:
    def __init__(self, bank_row_list):
        self.header = ['date', 'tr_type', 'amount', 'to', 'from']
        self.bank_row_list = bank_row_list

    def get_all_trasactions(self, tr_type):
        transactions = []
        for brl in self.bank_row_list:
            if brl.type == tr_type:
                transactions.append(brl)

        return transactions

    def __add__(self, obj2):
        if not obj2:
            return self

        obj = BankTable(self.bank_row_list)
        obj.bank_row_list.extend(obj2.bank_row_list)
        return obj


class IngestService:

    @classmethod
    def save_to_csv(cls, path=None, bank_table=None):
        bank_row_list = bank_table.bank_row_list
        header = bank_table.header
        csv_utill = CSVUtill()
        bank_table = [data.to_row() for data in bank_row_list]
        csv_utill.write_csv(data_to_write=bank_table, header=header)

    @classmethod
    def save_to_json(self, path=None, bank_table=None):
        bank_row_list = bank_table.bank_row_list
        header = bank_table.header
        bank_table = [dict(zip(header, data.to_row())) for data in bank_row_list]
        with open(path, "w") as out_file:
            json.dump({'data': bank_table}, out_file)

    # TODO
    @classmethod
    def save_to_xml(self, path=None):
        pass


class BankRow:
    '''
        Final Unified Row Structure
    '''

    def __init__(self, timestamp, tr_type, amount, amount_from, amount_to):
        self.__timestamp = timestamp
        self.__tr_type = tr_type
        self.__amount = amount
        self.__amount_from = amount_from
        self.__amount_to = amount_to

    def to_row(self):
        return [self.__timestamp, self.__tr_type,
                self.__amount, self.__amount_from, self.__amount_to]


class Bank(ABC):

    def process_file(self, path=None):
        """
            this function process input bank transaction file as csv and
            convert it to banktable object and return it
        """
        csv = CSVUtill(self.file_path)
        bank_data = csv.read_csv()
        final_list = self.convert_list_to_bank_table(bank_data)
        return final_list

    @abstractmethod
    def convert_list_to_bank_table(self):
        """
            function will list of bank row and convert it into BankTable Obj
            Input: list of bank row
            output: BankTable Object
        """
        pass


class Bank1(Bank):
    # Input:
    # timestamp,type,amount,from,to
    # Oct 1 2019,remove,99.20,198,182
    # Oct 2 2019,add,2000.10,188,198

    # Output:
    # timestamp,type,amount,from,to
    # Oct 1 2019,remove,99.20,198,182
    # Oct 2 2019,add,2000.10,188,198

    def __init__(self, file_path=None):
        if not file_path:
            self.file_path = 'bank1.csv'
        else:
            self.file_path = file_path

    def convert_list_to_bank_table(self, data_list):
        final_list = []
        for data in data_list:
            bank_row = BankRow(
                timestamp=data['timestamp'],
                tr_type=data['type'],
                amount=data['amount'],
                amount_from=data['from'],
                amount_to=data['to']
            )
            final_list.append(bank_row)

        return BankTable(bank_row_list=final_list)


class Bank2(Bank):
    # date,transaction,amounts,to,from
    # 03-10-2019,remove,99.40,182,198
    # 04-10-2019,add,2123.50,198,188

    def __init__(self, file_path=None):
        if not file_path:
            self.file_path = 'bank2.csv'
        else:
            self.file_path = file_path

    def convert_list_to_bank_table(self, data_list):
        final_list = []
        for data in data_list:
            bank_row = BankRow(
                timestamp=data['date'],
                tr_type=data['transaction'],
                amount=data['amounts'],
                amount_from=data['from'],
                amount_to=data['to']
            )
            final_list.append(bank_row)

        return BankTable(bank_row_list=final_list)


class Bank3(Bank):
    # date_readable,type,euro,cents,to,from
    # 5 Oct 2019,remove,5,7,182,198
    # 6 Oct 2019,add,1060,8,198,188

    def __init__(self, file_path=None):
        if not file_path:
            self.file_path = 'bank3.csv'
        else:
            self.file_path = file_path

    def convert_list_to_bank_table(self, data_list):
        final_list = []
        for data in data_list:
            amount = int(data['euro']) + int(data['cents']) / 100
            bank_row = BankRow(
                timestamp=data['date_readable'],
                tr_type=data['type'],
                amount=f"{amount}",
                amount_from=data['from'],
                amount_to=data['to']
            )
            final_list.append(bank_row)

        return BankTable(bank_row_list=final_list)
