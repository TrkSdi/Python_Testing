from locust import HttpUser, task

class ProjectPerfTest(HttpUser):
    
    @task
    def index(self):
        self.client.get("/")
    
    @task
    def login(self):
        self.client.post("/showSummary", data=dict({'email':'john@simplylift.co'}))
        
    @task
    def purchase(self):
        self.client.post("/purchasePlaces", data={'club': 'Test',
                 'competition': 'Test Festival_2030',
                 'places': '2',
                 })
    
    @task
    def book(self):
        self.client.get('/book/<competition>/<club>')
    
    @task
    def get_display(self):
        self.client.get('/pointDisplay')
    
    @task
    def logout(self):
        self.client.get('/logout')