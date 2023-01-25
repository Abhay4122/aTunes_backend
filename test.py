import requests, time
from locust import HttpUser, task

count = 0

HOST = 'https://atunes.cimsedu.com'
ENDPOINT = ''
URL = HOST + ENDPOINT

# while True:
#     st = time.time()
requests.get(URL)
    # count +=1 
    # print(count, '--', '%.2f' % (st - time.time()))

class WebsiteUser(HttpUser):
    @task 
    def hello_world(self): 
        self.client.get(url='/')