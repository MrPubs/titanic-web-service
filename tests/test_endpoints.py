import pytest
import httpx
from app.models import PassengerResponse, AllPassengerResponse, HistogramResponse

from http import HTTPStatus

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_get_all_passengers():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/passengers")

        # Response validation
        assert response.status_code == HTTPStatus.OK  # Check for HTTP Response -> OK

        # Schema validation
        data = response.json()
        try:
            parsed = AllPassengerResponse(**data)  # Check for Response Data Structure
        except Exception as e:
            pytest.fail(f"Response doesn't match AllPassengerResponse schema: {e}")

@pytest.mark.asyncio
async def test_get_single_passenger():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/passenger/1")

        # Response validation
        assert response.status_code == HTTPStatus.OK  # Check for HTTP Response -> OK

        # Schema validation
        data = response.json()
        try:
            parsed = PassengerResponse(**data)  # Check for Response Data Structure
        except Exception as e:
            pytest.fail(f"Response doesn't match PassengerResponse schema: {e}")

@pytest.mark.asyncio
async def test_get_passenger_attributes():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/passenger/1/attributes?attrs=Name&attrs=Sex&attrs=Age"
        )

        # Response validation
        assert response.status_code == HTTPStatus.OK  # Check for HTTP Response -> OK

        # Schema validation
        data = response.json()
        try:
            parsed = PassengerResponse(**data)  # Check for Response Data Structure
        except Exception as e:
            pytest.fail(f"Response doesn't match PassengerResponse schema: {e}")

@pytest.mark.asyncio
async def test_get_fare_histogram():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/histogram/fare")

        # Response validation
        assert response.status_code == HTTPStatus.OK  # Check for HTTP Response -> OK

        # Schema validation
        data = response.json()
        try:
            parsed = HistogramResponse(**data)  # Check for Response Data Structure
        except Exception as e:
            pytest.fail(f"Response doesn't match HistogramResponse schema: {e}")
