
# Project imports
from app.datasources.csv_source import CSVDataSource
from app.datasources.sqlite_source import SQLiteDataSource

# Lib imports
import yaml


async def get_data_source():

    # open config
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    # load correct source object which defines interactions
    src = config["data_source"]
    if src == "csv": # .csv format
        return CSVDataSource(config["csv_path"])

    elif src == "sqlite": # .db format
        return await SQLiteDataSource.create(config["sqlite_path"])

    else: # unknown format!
        raise ValueError("Invalid data_source in config")


if __name__ == '__main__':
    pass