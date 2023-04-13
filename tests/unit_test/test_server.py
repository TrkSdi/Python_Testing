from datetime import datetime
    
    
# Load str date
def now_date_str():
    now_date = datetime.now()
    now_str = now_date.strftime("%Y/%m/%d, %H:%M:%S")
    return now_str

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>GUDLFT Registration</title>' in response.data
    
def test_good_login(client):
    response = client.post('/showSummary', data=dict(
        email="test@test.com"
    ), follow_redirects=True)
    assert response.status_code == 200

def test_wrong_login(client):
    response = client.post('/showSummary', data=dict(
        email="email1@mail.com"
    ))
    assert response.status_code == 302

def test_get_access_display_points(client):
    response = client.get('/pointDisplay')
    assert response.status_code == 200
    

def test_get_data_display_points(client, clubs):
    response = client.get('/pointDisplay')
    data = response.data.decode()
    
    assert clubs[0]['name'] in data
    assert clubs[0]['points'] in data

def test_no_more_places_available(client, competitions):
    response = client.post('/showSummary', data=dict(
        email="test@test.com"
    ))
    assert int(competitions[2]['numberOfPlaces']) == 0
    assert 'No more places available' in response.data.decode()
    
def test_book_future_competition_success(client, competitions):
    response = client.post('/showSummary', data=dict(
        email="test@test.com"
    ))
    now = now_date_str()
    
    assert competitions[1]['date'] > now
    assert 'Book Places' in response.data.decode()
        
def test_impossible_to_access_past_competition(client, competitions):
    response = client.post('/showSummary', data=dict(
        email="test@test.com"
    ))
    now = now_date_str()
    assert competitions[0]['date'] < now
    assert 'competition completed' in response.data.decode()

def test_no_competition_scheduled(client, no_competition_scheduled):
    response = client.post('/showSummary', data=dict(
        email="test@test.com"
    ))
    if len(no_competition_scheduled) < 1:
        assert 'no competition scheduled' in response.data.decode()
    

def test_logout_success(client):
    response = client.get('/logout')
    
    assert response.status_code == 302

