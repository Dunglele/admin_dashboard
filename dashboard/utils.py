import requests
from django.conf import settings

def call_api(method, endpoint, token=None, data=None):
    """
    Hàm tiện ích để gọi FastAPI Backend.
    """
    url = f"{settings.API_BASE_URL}{endpoint}"
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return {"detail": "Không thể kết nối tới Backend API"}, 500
