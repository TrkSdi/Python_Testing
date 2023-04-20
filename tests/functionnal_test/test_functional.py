from datetime import datetime


# Load str date
def now_date_str():
    now_date = datetime.now()
    now_str = now_date.strftime("%Y/%m/%d, %H:%M:%S")
    return now_str

#Integration Test
def test_complete_user_interaction(client, clubs, competitions, data_form_purchase_2):
    # --- Access sign in --- #
    response = client.get('/')
    assert response.status_code == 200
    assert 'Welcome to the GUDLFT' in response.data.decode()
    
    # --- Login --- #
    response = client.post('/showSummary', data=dict(
        email="test@test.com"
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert 'Competitions' in response.data.decode()
    
    # --- Access club's list --- #
    response = client.get('/pointDisplay')
    assert response.status_code == 200
    
    # --- Book competition --- #
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

    # --- Logout --- #
    response = client.get('/logout')
    # flash message :
    assert response.status_code == 302
