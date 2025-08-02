# Responses
from app.models import PassengerResponse, HistogramResponse, AllPassengerResponse

# Lib imports
from fastapi import APIRouter, Request, Query
from typing import List

router = APIRouter()


@router.get("/passengers", response_model=AllPassengerResponse)
async def get_all(req: Request):
    return await req.app.state.datasource.get_all()


@router.get("/passenger/{pid}", response_model=PassengerResponse)
async def get_one(pid: int, req: Request):
    return await req.app.state.datasource.get_by_id(pid)


@router.get("/passenger/{pid}/attributes", response_model=PassengerResponse)
async def get_attrs(pid: int, attrs: List[str] = Query(...), req: Request = None):
    return await req.app.state.datasource.get_by_id_attrs(pid, attrs)


@router.get("/histogram/fare", response_model=HistogramResponse)
async def get_histogram(req: Request):
    return await req.app.state.datasource.get_fare_histogram()


if __name__ == '__main__':
    pass
