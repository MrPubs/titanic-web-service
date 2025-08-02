# Project imports
from app.datasources.base import DataSource
from app.utils import make_histogram

# Responses
from app.models import HistogramResponse, PassengerResponse, AllPassengerResponse

# Lib imports
from fastapi import HTTPException
import aiosqlite
from typing import List, Optional
import numpy as np


class SQLiteDataSource(DataSource):
    """
    Define Data Source Operations on SQLite .db Source
    """

    def __init__(self, db_path: str, conn: aiosqlite.Connection):
        self.db_path = db_path
        self.conn = conn

    @classmethod
    async def create(cls, db_path: str):
        conn = await aiosqlite.connect(db_path)
        conn.row_factory = aiosqlite.Row  # enables dict-like access to rows
        return cls(db_path, conn)

    async def get_all(self) -> AllPassengerResponse:

        # Construct query
        query = "SELECT * FROM passengers"
        async with self.conn.execute(query) as cursor:
            rows = await cursor.fetchall()

        return AllPassengerResponse(
            Passengers={
                str(row['PassengerId']): PassengerResponse(
                    PassengerId=row['PassengerId'],
                    metadata={k: v for k, v in dict(row).items() if k != 'PassengerId'}
                ) for row in rows
            }
        )

    async def get_by_id(self, passenger_id: int) -> PassengerResponse:
        return await self._get_passenger(passenger_id=passenger_id)

    async def get_by_id_attrs(self, passenger_id: int, attrs: List[str]) -> PassengerResponse:
        return await self._get_passenger(passenger_id=passenger_id, fields=attrs)

    async def get_fare_histogram(self) -> HistogramResponse:

        # Construct query
        query = "SELECT Fare FROM passengers"
        async with self.conn.execute(query) as cursor:
            rows = await cursor.fetchall()

        # Make fare data array
        fare_data = np.array([row["Fare"] for row in rows], dtype=np.float32)
        return make_histogram(data=fare_data)

    async def _get_passenger(self, passenger_id: int, fields: Optional[List[str]] = None) -> PassengerResponse:
        '''
        Shared helper for fetching passenger by id with optional attribute filtering.
        '''

        # Validate column names if filtering
        if fields:

            # Get Schema
            async with self.conn.execute("PRAGMA table_info(passengers)") as cursor:
                columns_info = await cursor.fetchall()  # all cols info

            # extract names for validity check
            all_column_names = {col_info['name'] for col_info in columns_info}
            invalid = [col for col in fields if col not in all_column_names]
            if invalid:
                raise HTTPException(status_code=400, detail=f"Invalid attributes: {invalid}")

        # Construct query
        selected_fields = ", ".join(fields) if fields else "*"
        query = f"SELECT {selected_fields} FROM passengers WHERE PassengerId = ?"
        async with self.conn.execute(query, (passenger_id,)) as cursor:
            row = await cursor.fetchone()

        # Raise if Passenger not found
        if row is None:
            raise HTTPException(status_code=404, detail=f"Passenger {passenger_id} not found")

        # JSONify
        row_dict = dict(row)
        return PassengerResponse(
            PassengerId=passenger_id,
            metadata={k: v for k, v in row_dict.items() if k != "PassengerId"}
        )


if __name__ == '__main__':
    import asyncio


    async def test():
        dbfile_path = r'C:\Users\zivg\Documents\Repos\titanic-web-service\data\titanic.db'
        ds = await SQLiteDataSource.create(db_path=dbfile_path)
        result = await ds.get_fare_histogram()
        print(result)


    asyncio.run(test())
    pass
