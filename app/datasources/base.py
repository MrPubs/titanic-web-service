
# Responses
from app.models import HistogramResponse, PassengerResponse, AllPassengerResponse

# Lib imports
from abc import ABC, abstractmethod
from typing import List


class DataSource(ABC):

    @abstractmethod
    async def get_all(self) -> dict:
        """
        Get all the data passenger data
        :return: a dict representing every passenger in the datasource
        """
        ...

    @abstractmethod
    async def get_by_id(self, passenger_id: int) -> dict:
        """
        Get the data of a passenger based on id only
        :param passenger_id: integer representing the passenger id
        :return: a dict representing a passenger, if exists
        """
        ...

    @abstractmethod
    async def get_by_id_attrs(self, passenger_id: int, attrs: List[str]) -> dict:
        """
        Get the data of a passenger based on id, and specific attributes
        :param passenger_id: integer representing the passenger id
        :param attrs: attributes list which specifies the columns (fields) in the dataframe to filter by
        :return: a filtered row as a dict representing the passenger in the desired fields if exists
        """
        ...

    @abstractmethod
    async def get_fare_histogram(self) -> HistogramResponse:
        """
        get fare histogram for the datasource.
        :return: dict if exists, representing the histogram of passenger fares
        """
        ...


if __name__ == '__main__':
    pass
