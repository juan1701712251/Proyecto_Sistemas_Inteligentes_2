import requests

class ClientHTTP:
    def postData(self,url,data):
        resp = requests.post(url=url, data=data)
        return resp