import pytest

import requests
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Включаем режим тестирования
    with app.test_client() as client:  # Используем тестового клиента Flask
        yield client

def test_get_all_company(client):
    res = requests.get('http://localhost:5000/companies')

    assert res.status_code == 200
    assert isinstance(res.json, list)