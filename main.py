import pandas as pd
import json
import requests
from tokens import client_id, client_secret_id, manual_code, wca_mail, wca_password

#auth

access_token_url = 'https://staging.worldcubeassociation.org/oauth/token'
competition_url = 'https://staging.worldcubeassociation.org/api/v0/competitions/MunichOpen2018/wcif'

   
headers = {'grant_type':'password', 'username':wca_mail, 'password':wca_password, 'scope':'public manage_competitions'}
request1 = requests.post(access_token_url, data=headers)
access_token = json.loads(request1.text)['access_token']


comp_id = "OakvilleFallB2022"
query = "https://www.worldcubeassociation.org/api/v0/competitions/{}/wcif/".format(
    comp_id)

authorization = 'Bearer ' + access_token
headers2 = {'Authorization': authorization}    
request2 = requests.get(query, headers=headers2)

r_json = request2.json()


