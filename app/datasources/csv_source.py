
# Project imports
from app.datasources.base import DataSource
from app.utils import make_histogram, steralize_df

# Responses
from app.models import HistogramResponse, PassengerResponse, AllPassengerResponse

# Lib imports
from fastapi import HTTPException
import pandas as pd
from typing import List, Optional


class CSVDataSource(DataSource):
    """
    Define Data Source Operations on CSV Source
    """

    def __init__(self, csvfile_path: str):

        # load csv contents
        self.csvfile_path = csvfile_path
        self.csvfile_df = pd.read_csv(self.csvfile_path)

    async def get_all(self) -> AllPassengerResponse:

        # Split once to avoid take advantage of vectorized operations
        passenger_ids = self.csvfile_df["PassengerId"].values
        metadata_df = self.csvfile_df.drop(columns=["PassengerId"])

        # Convert metadata columns to list of dicts
        metas = metadata_df.to_dict(orient="records")

        # JSONify
        return AllPassengerResponse(
            Passengers={
                str(pid): PassengerResponse(PassengerId=pid, metadata=meta) for pid, meta in zip(passenger_ids, metas)
            }
        )

    async def get_by_id(self, passenger_id: int) -> PassengerResponse:
        return self._get_passenger(self.csvfile_df, passenger_id)

    async def get_by_id_attrs(self, passenger_id: int, attrs: List[str]) -> PassengerResponse:
        return self._get_passenger(self.csvfile_df, passenger_id, cols=attrs)

    async def get_fare_histogram(self) -> HistogramResponse:

        # get relevant data, histogramify and return
        fare_data = self.csvfile_df.Fare.to_numpy()
        histo = make_histogram(data=fare_data)
        return histo

    @ staticmethod
    def _get_passenger(df: pd.DataFrame, passenger_id: int, cols: Optional[List[str]] = None) -> PassengerResponse:
        """
        Helper for getting a passenger from df, allows for efficient col filtering
        :param df: dataframe to query
        :param passenger_id: integer representing the id of the passenger
        :param cols: a list of columns to filter by. will be validated for existence.
        :return: dict if exists, representing the passenger
        """

        # get passenger row and check if exists, if yes, JSONify
        passenger_row = df[df["PassengerId"] == passenger_id]
        if passenger_row.empty:  # if passenger exists..
            raise HTTPException(status_code=404, detail=f"Passenger "
                                                        f"not found")

        # if desired subset cols only required
        if cols:

            # iterate cols to validate existance
            invalid_cols = [col for col in cols if col not in set(df.columns)]
            if invalid_cols:
                raise HTTPException(status_code=400, detail=f"Invalid attributes (columns): {invalid_cols}")

            # if you read this, all cols exist, now filter df to satisfy col subset
            passenger_row = passenger_row[cols]

        # JSONify
        data = passenger_row.iloc[0].to_dict()
        return PassengerResponse(
            PassengerId=passenger_id,
            metadata={k: v for k, v in data.items() if k != "PassengerId"}
        )


if __name__ == '__main__':

    # csvfile_path = r'C:\Users\zivg\Documents\Repos\titanic-web-service\data\titanic.csv'
    # csvfile_df = pd.read_csv(csvfile_path)


    pass