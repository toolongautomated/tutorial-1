import os
import pytest
import requests

ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
if not ENDPOINT_URL:
    raise ValueError("ENDPOINT_URL environment variable must be set")


@pytest.mark.parametrize(
    "position, expected_status, expected_response",
    [
        (3, 200, {"planet": "Earth"}),
        (9, 404, {"error": "No planet exists at position 9"}),
        (-1, 400, {"error": "Position must be greater than 0"}),
        ("not_a_number", 400, {"error": "Position must be a valid integer"}),
    ],
)
def test_planet_endpoint(position, expected_status, expected_response):
    response = requests.get(f"{ENDPOINT_URL}/planet", params={"position": position})
    assert response.status_code == expected_status
    data = response.json()

    for key, value in expected_response.items():
        assert key in data
        assert value in data[key] if "error" in key else data[key] == value
