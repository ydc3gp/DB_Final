from flask import Flask, jsonify, request
import pyodbc
import base64
import datetime

app = Flask(__name__)

server = 'localhost\\SQLEXPRESS'
database = 'LaundryAppDB'
username = 'sa'
password = 'carsoncolyer920'

# Connection string
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


def execute_query(query, params=None, fetch=False):
    """Helper function to execute database queries."""
    conn = None
    cursor = None
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if fetch:
            return cursor.fetchall()
        conn.commit()
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def query_database(query, params=None):
    """Reusable function to query the database."""
    conn = None
    cursor = None
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        rows = cursor.fetchall()

        def serialize_row(row):
            """Convert a row to a JSON-serializable dictionary."""
            row_dict = {}
            for index, column in enumerate(cursor.description):
                col_name = column[0]
                col_value = row[index]
                if isinstance(col_value, bytes):
                    col_value = base64.b64encode(col_value).decode('utf-8')
                elif isinstance(col_value, (datetime.date, datetime.time)):
                    col_value = col_value.isoformat()
                row_dict[col_name] = col_value
            return row_dict

        return [serialize_row(row) for row in rows]
    except Exception as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ------------------------- GET REQUESTS -------------------------

@app.route('/Users', methods=['GET'])
def get_users():
    try:
        query = "SELECT * FROM Users"
        result = query_database(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/Uses', methods=['GET'])
def get_uses():
    try:
        query = "SELECT * FROM Uses"
        result = query_database(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/Payment', methods=['GET'])
def get_payment():
    try:
        query = "SELECT * FROM Payment"
        result = query_database(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/DryerHistory', methods=['GET'])
def get_dryer_history():
    try:
        query = "SELECT * FROM DryerHistory"
        result = query_database(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/LaundryDevice', methods=['GET'])
def get_laundry_device():
    try:
        query = "SELECT * FROM LaundryDevice"
        result = query_database(query)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------------- PUT REQUESTS -------------------------

@app.route('/Payment/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    data = request.json
    try:
        query = "UPDATE Payment SET amount = ?, type = ? WHERE paymentID = ?"
        execute_query(query, (data['amount'], data['type'], payment_id))
        return jsonify({"message": f"Payment {payment_id} updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/Uses', methods=['PUT'])
def update_uses():
    data = request.json
    try:
        query = """
        UPDATE Uses 
        SET startTime = ? 
        WHERE machineID = ? AND username = ? AND paymentID = ?
        """
        execute_query(query, (data['startTime'], data['machineID'], data['username'], data['paymentID']))
        return jsonify({"message": "Uses record updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/LaundryDevice/<int:machine_id>', methods=['PUT'])
def update_laundry_device(machine_id):
    data = request.json
    try:
        query = "UPDATE LaundryDevice SET roomLocation = ?, isOccupied = ? WHERE machineID = ?"
        execute_query(query, (data['roomLocation'], data['isOccupied'], machine_id))
        return jsonify({"message": f"LaundryDevice {machine_id} updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/Users/<string:username>', methods=['PUT'])
def update_user(username):
    data = request.json
    try:        
        query = """
        UPDATE Users 
        SET email = ?, password = ?, phone_number = ? 
        WHERE username = ?
        """
        params = (data['email'], data['password'], data['phone_number'], username)
        
        execute_query(query, params)
        return jsonify({"message": f"User {username} updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/DryerHistory/<int:dryer_id>', methods=['PUT'])
def update_dryer_history(dryer_id):
    data = request.json
    try:
        query = """
        UPDATE DryerHistory 
        SET temp = ?, sensorDry = ?, time = ? 
        WHERE dryerID = ?
        """
        execute_query(query, (data['temp'], data['sensorDry'], data['time'], dryer_id))
        return jsonify({"message": f"DryerHistory {dryer_id} updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------------- DELETE REQUESTS -------------------------

@app.route('/Payment/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    try:
        query = "DELETE FROM Payment WHERE paymentID = ?"
        execute_query(query, (payment_id,))
        return jsonify({"message": f"Payment {payment_id} deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/Uses', methods=['DELETE'])
def delete_uses():
    data = request.json
    try:
        query = """
        DELETE FROM Uses 
        WHERE machineID = ? AND username = ? AND paymentID = ?
        """
        execute_query(query, (data['machineID'], data['username'], data['paymentID']))
        return jsonify({"message": "Uses record deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/LaundryDevice/<int:machine_id>', methods=['DELETE'])
def delete_laundry_device(machine_id):
    try:
        query = "DELETE FROM LaundryDevice WHERE machineID = ?"
        execute_query(query, (machine_id,))
        return jsonify({"message": f"LaundryDevice {machine_id} deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/Users/<string:username>', methods=['DELETE'])
def delete_user(username):
    try:
        query = "DELETE FROM Users WHERE username = ?"
        execute_query(query, (username,))
        return jsonify({"message": f"User {username} deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/DryerHistory/<int:dryer_id>', methods=['DELETE'])
def delete_dryer_history(dryer_id):
    try:
        query = "DELETE FROM DryerHistory WHERE dryerID = ?"
        execute_query(query, (dryer_id,))
        return jsonify({"message": f"DryerHistory {dryer_id} deleted successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ------------------------- POST REQUESTS -------------------------

@app.route('/Payment', methods=['POST'])
def create_payment():
    """Create a new Payment record."""
    data = request.json
    try:
        query = "INSERT INTO Payment (amount, type) VALUES (?, ?)"
        execute_query(query, (data['amount'], data['type']))
        return jsonify({"message": "Payment record created successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/Uses', methods=['POST'])
def create_uses():
    """Create a new Uses record."""
    data = request.json
    try:
        query = """
        INSERT INTO Uses (machineID, username, paymentID, startTime) 
        VALUES (?, ?, ?, ?)
        """
        execute_query(query, (data['machineID'], data['username'], data['paymentID'], data.get('startTime', None)))
        return jsonify({"message": "Uses record created successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/LaundryDevice', methods=['POST'])
def create_laundry_device():
    """Create a new LaundryDevice record."""
    data = request.json
    try:
        query = "INSERT INTO LaundryDevice (roomLocation, isOccupied) VALUES (?, ?)"
        execute_query(query, (data['roomLocation'], data['isOccupied']))
        return jsonify({"message": "LaundryDevice record created successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/Users/<string:username>', methods=['POST'])
def create_user(username):
    """Create a new User record."""
    data = request.json
    try:
        query = """
        INSERT INTO Users (email, password, username, phone_number) 
        VALUES (?, ?, ?, ?)
        """
        execute_query(query, (data['email'], data['password'], username, data['phone_number']))
        return jsonify({"message": f"User {username} created successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/DryerHistory', methods=['POST'])
def create_dryer_history():
    """Create a new DryerHistory record."""
    data = request.json
    try:
        query = "INSERT INTO DryerHistory (dryerID, temp, sensorDry, time) VALUES (?, ?, ?, ?)"
        execute_query(query, (data['dryerID'], data['temp'], data['sensorDry'], data['time']))
        return jsonify({"message": "DryerHistory record created successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
