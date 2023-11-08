import requests


def test_get_all_company():
    res = requests.get('http://localhost:5000/companies')

    assert res.status_code == 200
    assert isinstance(res.json, list)


def test_create_item_post():
    res = requests.post('http://localhost:5000/companies')

    assert res.status_code == 200