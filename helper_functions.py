import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5000" 

def calculate_end_time(dryer_id):
    """
    Calculate the end time of a dryer cycle based on temperature and start time.

    Parameters:
        dryer_id (int): The ID of the dryer.

    Returns:
        dict: The calculated end time or an error message.
    """
    # Define durations for each temperature setting
    temp_durations = {
        "Low": 30,         
        "Medium": 45,     
        "High": 60,        
        "No heat": 20      
    }

    try:
        response = requests.get(f"{BASE_URL}/DryerHistory")
        if response.status_code != 200:
            return {"error": "Failed to fetch dryer history"}

        dryer_history = response.json()

        # Find the record for the given dryer ID
        record = next((item for item in dryer_history if item["dryerID"] == dryer_id), None)
        if not record:
            return {"error": f"No record found for dryerID {dryer_id}"}

        start_time_str = record["time"]
        temp = record["temp"]

        if temp not in temp_durations:
            return {"error": f"Invalid temperature setting: {temp}"}

        # Parse the start time
        start_time = datetime.fromisoformat(start_time_str)

        # Calculate the end time
        duration_minutes = temp_durations[temp]
        end_time = start_time + timedelta(minutes=duration_minutes)

        return {"dryerID": dryer_id, "start_time": start_time_str, "end_time": end_time.isoformat()}
    except Exception as e:
        return {"error": str(e)}

def is_active_user(username):
    """
    Check if a user has been active in the last 30 days.
    """
    import datetime
    import requests

    current_time = datetime.datetime.now()

    # Fetch user's usage, feedback, and payments
    uses = requests.get(f"{BASE_URL}/Uses").json()
    feedbacks = requests.get(f"{BASE_URL}/Feedback").json()
    payments = requests.get(f"{BASE_URL}/Payment").json()

    # Check activity
    for use in uses:
        if use["username"] == username and (current_time - datetime.datetime.fromisoformat(use["startTime"])).days <= 30:
            return True

    for feedback in feedbacks:
        if feedback["feedbackUser"] == username and (current_time - datetime.datetime.fromisoformat(feedback["feedbackID"])).days <= 30:
            return True

    for payment in payments:
        pass  

    return False

def overdue_balance(username, threshold=100):
    """
    Check if a student's balance exceeds a specific threshold.
    """
    import requests

    students = requests.get(f"{BASE_URL}/Student").json()

    for student in students:
        if student["username"] == username and student["balance"] > threshold:
            return True

    return False

def machine_count():
    """
    Count the total number of laundry devices per building.
    """
    import requests

    buildings = requests.get(f"{BASE_URL}/Building").json()
    devices = requests.get(f"{BASE_URL}/LaundryDevice").json()

    machine_counts = {}
    for building in buildings:
        count = sum(1 for device in devices if device["roomLocation"] == building["laundryRoom"])
        machine_counts[building["name"]] = count

    return machine_counts

def active_service_requests():
    """
    Count unresolved service requests per building.
    """
    import requests

    buildings = requests.get(f"{BASE_URL}/Building").json()
    devices = requests.get(f"{BASE_URL}/LaundryDevice").json()
    service_requests = requests.get(f"{BASE_URL}/ServiceRequest").json()

    active_requests = {}
    for building in buildings:
        count = 0
        for device in devices:
            if device["roomLocation"] == building["laundryRoom"]:
                count += sum(1 for sr in service_requests if sr["machineID"] == device["machineID"] and not sr["resolved"])
        active_requests[building["name"]] = count

    return active_requests
