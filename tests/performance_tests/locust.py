from locust import HttpUser, task
import shutil


def init_data():
    shutil.copyfile("data/clubs.json", "clubs.json")
    shutil.copyfile("data/competitions.json", "competitions.json")
    


class ProjectPerfTest(HttpUser):
    
    @task
    def index(self):
        self.client.get("/")
    
    @task
    def login(self):
        self.client.post("/showSummary", data=dict({'email':'john@simplylift.co'}))
       
    @task
    def book(self):
        self.client.get('/book/<competition>/<club>', data={'club': 'Simply Lift',
                 'competition': 'Spring Festival'})
        init_data() 
     
    @task
    def purchase(self):
        self.client.post("/purchasePlaces", data={'club': 'Simply Lift',
                 'competition': 'Spring Festival',
                 'places': '2',
                 })
        init_data()
    
    @task
    def get_display(self):
        self.client.get('/pointDisplay')

    @task
    def logout(self):
        self.client.get('/logout')