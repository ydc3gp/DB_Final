import requests
import json

BASE_URL = "http://127.0.0.1:5000"  # Update this URL if your Flask app runs on a different host or port


def get_users():
    """Fetch all users."""
    response = requests.get(f"{BASE_URL}/Users")
    return response.json()


def get_uses():
    """Fetch all uses."""
    response = requests.get(f"{BASE_URL}/Uses")
    return response.json()


def get_payment():
    """Fetch all payment records."""
    response = requests.get(f"{BASE_URL}/Payment")
    return response.json()


def get_dryer_history():
    """Fetch all dryer history records."""
    response = requests.get(f"{BASE_URL}/DryerHistory")
    return response.json()


def get_laundry_device():
    """Fetch all laundry devices."""
    response = requests.get(f"{BASE_URL}/LaundryDevice")
    return response.json()


def make_payment(amount, payment_type):
    """Create a payment record."""
    data = {
        "amount": amount,
        "type": payment_type
    }
    response = requests.post(f"{BASE_URL}/Payment", json=data)
    return response.json()


def create_use(machine_id, username, payment_id, start_time=None):
    """Create a new use record."""
    data = {
        "machineID": machine_id,
        "username": username,
        "paymentID": payment_id,
        "startTime": start_time
    }
    response = requests.post(f"{BASE_URL}/Uses", json=data)
    return response.json()

def create_laundry_device(room_location, is_occupied):
    """Create a new laundry device."""
    data = {
        "roomLocation": room_location,
        "isOccupied": is_occupied
    }
    response = requests.post(f"{BASE_URL}/LaundryDevice", json=data)
    return response.json()


def update_laundry_device(machine_id, room_location, is_occupied):
    """Update a laundry device record."""
    data = {
        "roomLocation": room_location,
        "isOccupied": is_occupied
    }
    response = requests.put(f"{BASE_URL}/LaundryDevice/{machine_id}", json=data)
    return response.json()
def update_user(username, profile_picture, email, password, phone_number):
    """Update a user's information."""
    data = {
        "profile_picture": profile_picture,
        "email": email,
        "password": password,
        "phone_number": phone_number
    }
    response = requests.put(f"{BASE_URL}/Users/{username}", json=data)
    return response.json()
def update_dryer_history(dryer_id, temp, sensor_dry, time):
    """Update an existing dryer history record."""
    data = {
        "temp": temp,
        "sensorDry": sensor_dry,
        "time": time
    }
    response = requests.put(f"{BASE_URL}/DryerHistory/{dryer_id}", json=data)
    return response.json()
def update_uses(machine_id, username, payment_id, start_time):
    """Update an existing use record."""
    data = {
        "startTime": start_time,
        "machineID": machine_id,
        "username": username,
        "paymentID": payment_id
    }
    response = requests.put(f"{BASE_URL}/Uses", json=data)
    return response.json()

def update_payment(payment_id, amount, payment_type):
    """Update an existing payment."""
    data = {
        "amount": amount,
        "type": payment_type
    }
    response = requests.put(f"{BASE_URL}/Payment/{payment_id}", json=data)
    return response.json()

def create_user(profile_picture, email, password, username, phone_number):
    """Create a new user."""
    data = {
        "profile_picture": profile_picture,
        "email": email,
        "password": password,
        "username": username,
        "phone_number": phone_number
    }
    response = requests.post(f"{BASE_URL}/Users", json=data)
    return response.json()


def create_dryer_history(dryer_id, temp, sensor_dry, time):
    """Create a new dryer history record."""
    data = {
        "dryerID": dryer_id,
        "temp": temp,
        "sensorDry": sensor_dry,
        "time": time
    }
    response = requests.post(f"{BASE_URL}/DryerHistory", json=data)
    return response.json()

def delete_payment(payment_id):
    """Delete a payment record."""
    response = requests.delete(f"{BASE_URL}/Payment/{payment_id}")
    return response.json()


def delete_uses(machine_id, username, payment_id):
    """Delete a use record."""
    data = {
        "machineID": machine_id,
        "username": username,
        "paymentID": payment_id
    }
    response = requests.delete(f"{BASE_URL}/Uses", json=data)
    return response.json()


def delete_laundry_device(machine_id):
    """Delete a laundry device record."""
    response = requests.delete(f"{BASE_URL}/LaundryDevice/{machine_id}")
    return response.json()


def delete_user(username):
    """Delete a user."""
    response = requests.delete(f"{BASE_URL}/Users/{username}")
    return response.json()


def delete_dryer_history(dryer_id):
    """Delete a dryer history record."""
    response = requests.delete(f"{BASE_URL}/DryerHistory/{dryer_id}")
    return response.json()



# Example usage:
if __name__ == "__main__":
    # Test fetching users
    print("Users:", get_users())
    
    # Create a payment
    payment_response = make_payment(5.50, "credit")
    print("Payment Response:", payment_response)
    
    # Create a use record
    use_response = create_use(machine_id=101, username="john_doe", payment_id=1, start_time="2024-11-29T10:00:00")
    print("Use Response:", use_response)
    
    # Update a laundry device
    laundry_response = update_laundry_device(machine_id=101, room_location="Dorm A", is_occupied=True)
    print("Laundry Device Update Response:", laundry_response)
    
    # Create a user
    user_response = create_user(
        profile_picture="base64encodedstring",
        email="john.doe@example.com",
        password="securepassword",
        username="john_doe",
        phone_number="1234567890"
    )
    print("User Creation Response:", user_response)
    
    # Create a dryer history record
    dryer_response = create_dryer_history(dryer_id=201, temp=70, sensor_dry=True, time="2024-11-29T10:00:00")
    print("Dryer History Creation Response:", dryer_response)
