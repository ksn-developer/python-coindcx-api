import requests
import pdb

class Request:

    def __init__(self):
        self.response = {}

    def post_json(self,url,json,headers = None):
        response = None
        try:
            if headers:
                response = requests.post(url,json = json,headers = headers)
                
            else:
                response = requests.post(url,json = json)

            if response.status_code == 200:
                self.response["data"] = response.json()
            else:
                self.response["error"] = response.reason

        except Exception as e:
            self.response["exception"] = str(e)
            
            pdb.set_trace()
        return self.response

    def post(self,url,data,headers = None):
       
        response = None
        try:
            if headers:
                response = requests.post(url,data = data,headers = headers)
            else:
                response = requests.post(url,data = data)
            if response.status_code == 200:
                self.response["data"] = self.response.json()
            else:         
                self.response["error"] = str(self.response.content)# this gives better insight to happened
        
        except Exception as e:
            pdb.set_trace()
            self.response["exception"] = str(e)

        return self.response

    def get(self,url,headers = None):
        response = None
        try:
            if headers:
                response = requests.get(url,headers = headers)
            else:
                response = requests.get(url)

            if response.status_code == 200:
                self.response["data"] = response.json()
            else:
                self.response["error"] = response.reason

        except Exception as e:
            
            pdb.set_trace()
            self.response["exception"] = str(e)
            
        return self.response