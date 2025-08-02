from typing import List, Dict, Any
from pydantic import BaseModel
import numpy as np


# Passenger
class PassengerResponse(BaseModel):
    PassengerId: int
    metadata: Dict[str, Any]  # could enforce Any further using Union[]

class AllPassengerResponse(BaseModel):
    Passengers: Dict[str, PassengerResponse]


# Histogram

class Bin(BaseModel):
    percentile_start: float
    percentile_end: float
    bin_start: float
    bin_end: float
    count: int


class Histogram(BaseModel):
    bins: List[Bin]


class HistogramMetadata(BaseModel):
    field: str
    bucket_count: int
    total_count: int


class HistogramResponse(BaseModel):
    metadata: HistogramMetadata
    histogram: Histogram


if __name__ == '__main__':
    pass
