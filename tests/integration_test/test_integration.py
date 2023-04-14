import pytest


# LOGIN ACCESS
@pytest.mark.integtest
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>GUDLFT Registration</title>' in response.data

# LOGIN SUCCESS
@pytest.mark.integtest
def test_good_login(client):
    response = client.post('/showSummary', data=dict(
        email="john@simplylift.co"
    ), follow_redirects=True)
    assert response.status_code == 200

# BOOK SUCCESS
@pytest.mark.integtest  
def test_book_competition_success(client, clubs, competitions, data_form_purchase_2):
    club_points_before = int(clubs[0]["points"]) 
    competition_number_place_before = int(competitions[1]["numberOfPlaces"])
    
    response = client.post("/purchasePlaces", data=data_form_purchase_2)

    # Check status code
    assert response.status_code == 200
    
    # check booking has been made correctly :
    assert club_points_before - 2 == int(clubs[0]["points"])
    assert competition_number_place_before - 2 == int(competitions[1]["numberOfPlaces"])
    # flash message :
    assert 'Great-booking complete!' in response.data.decode()  

# DIPLAY POINT BOARD ACCESS
@pytest.mark.integtest  
def test_get_access_display_points(client):
    response = client.get('/pointDisplay')
    assert response.status_code == 200

# DISPLAY POINT DATA SUCCESS
@pytest.mark.integtest  
def test_get_data_display_points(client, clubs):
    response = client.get('/pointDisplay')
    data = response.data.decode()
    
    assert clubs[0]['name'] in data
    assert clubs[0]['points'] in data  

# LOGOUT SUCCESS
@pytest.mark.integtest
def test_logout_success(client):
    response = client.get('/logout')
    assert response.status_code == 302