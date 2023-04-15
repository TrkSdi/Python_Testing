from datetime import datetime


# Load str date
def now_date_str():
    now_date = datetime.now()
    now_str = now_date.strftime("%Y/%m/%d, %H:%M:%S")
    return now_str


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


def test_purchase_more_than_available_error(client, clubs, competitions, data_form_purchase_30):
    club_points_before = int(clubs[0]["points"])
    competition_number_place_before = int(competitions[1]["numberOfPlaces"])
    
    response = client.post('/purchasePlaces', data=data_form_purchase_30)
    
    # Check status code
    assert response.status_code == 200
    # no booking has been made : 
    assert club_points_before == int(clubs[0]["points"])
    assert competition_number_place_before == int(competitions[1]["numberOfPlaces"])
    # flash message :
    assert 'Not enough places' in response.data.decode()
    

def test_purchase_more_12_error(client, clubs, competitions, data_form_purchase_13):
    club_points_before = int(clubs[0]["points"])
    competition_number_place_before = int(competitions[1]["numberOfPlaces"])
    
    response = client.post('/purchasePlaces', data=data_form_purchase_13)

    # Check status code
    assert response.status_code == 200
    # no booking has been made : 
    assert club_points_before == int(clubs[0]["points"])
    assert competition_number_place_before == int(competitions[1]["numberOfPlaces"])
    # flash message : 
    assert 'No more than 12 places can be booked' in response.data.decode()
    

def test_purchase_less_or_equal_12_success(client, clubs, competitions, data_form_purchase_12):
    club_points_before = int(clubs[0]["points"])
    competition_number_place_before = int(competitions[1]["numberOfPlaces"])
    
    response = client.post('/purchasePlaces', data=data_form_purchase_12)
    
    # Check status code
    assert response.status_code == 200
    # check booking has been made correctly : 
    assert club_points_before - 12 == int(clubs[0]["points"])
    assert competition_number_place_before - 12 == int(competitions[1]["numberOfPlaces"])
    # flash message : 
    assert 'Great-booking complete!' in response.data.decode()
    
def test_invalid_places_value_error(client, clubs, competitions, data_form_purchase_invalid):
    club_points_before = int(clubs[0]["points"])
    competition_number_place_before = int(competitions[1]["numberOfPlaces"])
    
    response = client.post('/purchasePlaces', data=data_form_purchase_invalid)
    
    # Check status code
    assert response.status_code == 200
    # no booking has been made :  
    assert club_points_before == int(clubs[0]["points"])
    assert competition_number_place_before == int(competitions[1]["numberOfPlaces"])
    # flash message :
    assert 'Invalid value' in response.data.decode()

def test_purchase_for_past_competition_return_error(client, competitions, data_form_purchase_2):
    
    response = client.get(f'/book/{competitions[0]["name"]}/{data_form_purchase_2["club"]}')
    
    # Check status code
    assert response.status_code == 200
    # flash message :
    assert 'impossible to book a past competition' in response.data.decode()
    

def test_access_booking_for_future_competition(client, competitions, data_form_purchase_2):
    response = client.get(f'/book/{competitions[1]["name"]}/{data_form_purchase_2["club"]}')
    assert response.status_code == 200
  

def test_access_booking_return_error(client, no_competition_scheduled, data_form_purchase_2):
    response = client.get(f'/book/{no_competition_scheduled[0]}/{data_form_purchase_2["club"]}')
    
    assert 'Something went wrong-please try again' in response.data.decode()

def test_cannot_book_more_than_club_point_available(client, club_1, competitions, data_form_purchase_2):
    club_points_before = int(club_1[0]["points"])
    competition_number_place_before = int(competitions[1]["numberOfPlaces"])
    
    response = client.post('/purchasePlaces', data=data_form_purchase_2)
    
    # Check status code
    assert response.status_code == 200
    # check booking has been made correctly : 
    assert club_points_before == int(club_1[0]["points"])
    assert competition_number_place_before == int(competitions[1]["numberOfPlaces"])
    # flash message : 
    assert 'Not enough points' in response.data.decode()