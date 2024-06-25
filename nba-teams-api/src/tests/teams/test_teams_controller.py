import os
import sys
import pytest
from unittest.mock import patch
from src.controllers.teams import CustomException

# current_dir = os.path.dirname(os.path.abspath(__file__))
# src_dir = os.path.abspath(os.path.join(current_dir, '..', ".."))
# sys.path.append(src_dir)
def test_get_teams(test_client):
    response = test_client.get('/teams/')
    assert response.status_code == 200
    assert response.json == {"teams": [ 
    {
        "id": 1,
        "name": "Los Angeles Lakers",
        "city": "Los Angeles"
    },
    {
        "id": 2,
        "name": "Golden State Warriors",
        "city": "San Fransisco"
    }
]}

def test_get_empty_teams(test_client):
    with patch('controllers.teams.teams', []):
        response = test_client.get('/teams/')
        assert response.status_code == 400
        assert response.json == {"message": "There are no registered teams yet"}

@pytest.mark.parametrize("team_id, expected_status", [
    (1, 200),
    (2, 200),
    (99, 400)
])
def test_with_parameterized(test_client, team_id, expected_status):
    response = test_client.get(f'/teams/{team_id}')
    if team_id == 99:
        assert response.status_code == expected_status
        assert response.json == {"message": f"There are no registered teams with ID: {team_id}"}
    else:
        assert response.status_code == expected_status

def test_create_with_invalid_data(test_client):
    response = test_client.post('/teams/', json={'city': 'Bogor'})
    assert response.status_code == 422
    assert response.json == {"message": "Ensure Team's name and city is provided!"}

@patch('controllers.teams.validate_team_data')
def test_mock(mocked_validate_team_data, test_client):
    mocked_validate_team_data.return_value = None
    side_effect = CustomException("Jiakh", 403)
    mocked_validate_team_data.side_effect = side_effect
    response = test_client.post('/teams/', json={'city': 'Bogor'})
    assert response.status_code == 403
    assert response.json == {"message": "Jiakh"}

