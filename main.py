from service import Bank1, Bank2, Bank3, IngestService

# input : multiple file (csv)
# out: csv/json/xml

# If we want to add new bank , we need to create new 
# class and need to add bank type class mapping in BANK_CONFIGS Variable

BANK_CONFIGS = {
    "bank1": {
        "class": Bank1,
        "path": "bank1.csv"
    },
    "bank2": {
        "class": Bank2,
        "path": "bank2.csv"
    },
    "bank3": {
        "class": Bank3,
        "path": "bank3.csv"
    }
}

if __name__ == '__main__':
    all_bank_data = None
    for bank_type in BANK_CONFIGS:
        BankClass = BANK_CONFIGS[bank_type]['class']
        file_path = BANK_CONFIGS[bank_type]['path']
        bank_obj = BankClass(file_path)
        bank_table_obj = bank_obj.process_file()
        all_bank_data = bank_table_obj + all_bank_data

    IngestService.save_to_csv(path="bank.csv", bank_table=all_bank_data)
    IngestService.save_to_json(path="bank.json", bank_table=all_bank_data)
