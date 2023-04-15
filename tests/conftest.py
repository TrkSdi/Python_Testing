import pytest

from server import app
import server


@pytest.fixture
def client():
    client = app.test_client()
    yield client
     
@pytest.fixture
def clubs():
    clubs = server.clubs = [
        {
            "name": "Test",
            "email": "test@test.com",
            "points": "20"
        }
        ]
    yield clubs
    
@pytest.fixture
def club_1():
    clubs = server.clubs = [
        {
            "name": "Test",
            "email": "test@test.com",
            "points": "1"
        }
        ]
    yield clubs

@pytest.fixture
def competitions():
    competitions = server.competitions = [
        {
            "name": "Test Festival 2020",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Test Festival_2030",
            "date": "2030-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Test No Place Festival",
            "date": "2030-03-27 10:00:00",
            "numberOfPlaces": "0"
        }
        ]
    yield competitions

@pytest.fixture
def data_form_purchase_2():
    data_form = {'club': 'Test',
                 'competition': 'Test Festival_2030',
                 'places': '2',
                 }
    return data_form

@pytest.fixture
def data_form_purchase_13():
    data_form = {'club': 'Test',
                 'competition': 'Test Festival_2030',
                 'places': '13',
                 }
    return data_form

@pytest.fixture
def data_form_purchase_30():
    data_form = {'club': 'Test',
                 'competition': 'Test Festival_2030',
                 'places': '30',
                 }
    return data_form

@pytest.fixture
def data_form_purchase_12():
    data_form = {'club': 'Test',
                 'competition': 'Test Festival_2030',
                 'places': '12',
                 }
    return data_form

@pytest.fixture
def data_form_purchase_invalid():
    data_form = {'club': 'Test',
                 'competition': 'Test Festival_2030',
                 'places': '',
                 }
    return data_form

@pytest.fixture
def no_competition_scheduled():
    competition = [{}]
    return competition
