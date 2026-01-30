import requests
from requests.auth import HTTPBasicAuth

BASE_URL = 'http://127.0.0.1:8000/api/network-nodes/2/'
USERNAME = 'Mvideo'
PASSWORD = 'Rz67911223'

print("=== PUT запрос с изменением debt ===")
data = {
    "name": "Сеть М.Видео",
    "node_type": 1,
    "email": "romansolik@vivaldi.net",
    "country": "Россия", 
    "city": "Соликамск",
    "street": "Белинского",
    "house_number": "13",
    "products": [1],
    "supplier": 1,
    "debt": "50000.00"
}

# response = requests.put(
#     BASE_URL,
#     json=data,
#     auth=(USERNAME, PASSWORD)
# )
# print('PUT status:', response.status_code)
# print('PUT response:', response.json())

response = requests.get(BASE_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
print('GET status для неактивного:', response.status_code)