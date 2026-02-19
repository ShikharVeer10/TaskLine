
import requests
import uuid
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"

def print_response(response):
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print("-" * 50)

def test_api():
    # 1. Register a new user
    print("\n1. Testing Signup...")
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    payload = {
        "email": email,
        "password": password,
        "full_name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/users/signup", json=payload)
    if response.status_code != 200:
        print(f"Signup failed: {response.text}")
        return
    print("Signup successful")
    print_response(response)

    # 2. Login
    print("\n2. Testing Login...")
    login_data = {
        "username": email,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/login/access-token", data=login_data)
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return
    token_data = response.json()
    access_token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    print("Login successful. Token received.")
    print_response(response)

    # 3. Get Current User
    print("\n3. Testing Get Current User...")
    response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print_response(response)

    # 4. Create Task
    print("\n4. Testing Create Task...")
    task_payload = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "high",
        "status": "todo"
    }
    response = requests.post(f"{BASE_URL}/tasks/", json=task_payload, headers=headers)
    if response.status_code != 200:
        print(f"Create task failed: {response.text}")
        return
    task_data = response.json()
    task_id = task_data["id"]
    print("Task created successfully.")
    print_response(response)

    # 5. List Tasks
    print("\n5. Testing List Tasks...")
    response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    print_response(response)

    # 6. Update Task
    print("\n6. Testing Update Task...")
    update_payload = {
        "status": "in_progress",
        "description": "Updated description"
    }
    response = requests.patch(f"{BASE_URL}/tasks/{task_id}", json=update_payload, headers=headers)
    print_response(response)

    # 7. Delete Task
    print("\n7. Testing Delete Task...")
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    print_response(response)
    
    # 8. Verify Deletion
    print("\n8. Verifying Deletion...")
    response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    if response.status_code == 404:
        print("Task successfully deleted (404 Not Found as expected).")
    else:
        print("Task still exists or error:")
        print_response(response)

if __name__ == "__main__":
    test_api()
