import requests
import time
import random

url = "http://127.0.0.1:5000/login"

# Simulated fake attacker IPs
fake_ips = [
    "192.168.1.10",
    "172.16.0.5",
    "203.0.113.99",
    "10.0.0.22",
    "198.51.100.42"
]

for i in range(30):
    fake_ip = random.choice(fake_ips)
    
    headers = {
        "X-Fake-IP": fake_ip
    }
    
    data = {
        'username': 'admin',
        'password': f'wrong{i}'
    }

    response = requests.post(url, data=data, headers=headers)
    print(f"Attempt {i} from {fake_ip}: {response.status_code}")
    
    time.sleep(0.2)  # simulate attack speed
