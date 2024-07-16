from flask import Flask, request, jsonify
from firebase_admin import credentials, initialize_app, db
import smtplib
from email.mime.text import MIMEText
import random
import string
from datetime import datetime, timedelta
from flask_cors import CORS
from dateutil import parser
import hashlib

app = Flask(__name__)
CORS(app)

cred = credentials.Certificate('/path/to/your/firebase/credentials.json')
initialize_app(cred, {'databaseURL': 'https://your-database-url.firebaseio.com'})

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_email(subject, body, to_email):
    sender_email = "your_email@gmail.com"
    app_password = "your_email_app_password"
    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, to_email, message.as_string())
    except Exception as e:
        print("Failed to send email:", e)

def generate_access_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    password_hash = hash_password(password)
    ref = db.reference('users').order_by_child('email').equal_to(email).limit_to_last(1).get()
    user_data = next(iter(ref.values()), None)

    if user_data and user_data.get('password') == password_hash:
        if email == 'laksh4740@gmail.com':
            return jsonify({"message": "Superadmin login successful.", "superadmin": True}), 200
        else:
            return jsonify({"message": "Login successful.", "superadmin": False}), 200
    return jsonify({"message": "Invalid email or password."}), 400

@app.route('/request_approval', methods=['POST'])
def request_approval():
    data = request.json
    email = data.get('email')

    approval_link = f"http://127.0.0.1:5000/approve?email={email}"
    denial_link = f"http://127.0.0.1:5000/deny?email={email}"
    approve_forever_link = f"http://127.0.0.1:5000/approve_forever?email={email}"
    body = f"User {email} is requesting access.\nApprove: {approval_link}\nDeny: {denial_link}\nApprove Forever: {approve_forever_link}"
    send_email("Access Approval Request", body, "laksh4740@gmail.com")
    
    return jsonify({'message': 'Approval request sent to superadmin.'}), 200

@app.route('/approve', methods=['GET'])
def approve():
    email = request.args.get('email')
    access_code = generate_access_code()
    expiry_time = datetime.utcnow() + timedelta(hours=1)
    db.reference('access_codes').push({
        'email': email,
        'access_code': access_code,
        'expiry_time': expiry_time.isoformat()
    })

    body = f"Your access code is: {access_code}\nThis code is valid for 1 hour."
    send_email("Access Approved", body, email)
    
    return "Access approved and code sent to user.", 200

@app.route('/approve_forever', methods=['GET'])
def approve_forever():
    email = request.args.get('email')
    access_code = generate_access_code()
    db.reference('access_codes').push({
        'email': email,
        'access_code': access_code,
        'expiry_time': 'forever'
    })
    db.reference('whitelisted_users').push({
        'email': email,
        'access_code': access_code
    })

    body = f"Your access code is: {access_code}\nThis code is valid indefinitely."
    send_email("Access Approved Forever", body, email)
    
    return "Access approved forever and code sent to user.", 200

@app.route('/deny', methods=['GET'])
def deny():
    email = request.args.get('email')

    body = "Your access request has been denied."
    send_email("Access Denied", body, email)
    
    return "Access denied and user notified.", 200

@app.route('/verify_access_code', methods=['POST'])
def verify_access_code():
    try:
        data = request.get_json()
        access_code = data.get('access_code')

        if access_code:
            ref = db.reference('access_codes')
            codes = ref.order_by_child('access_code').equal_to(access_code).get()
            for code_key, code_value in codes.items():
                expiry_time = code_value['expiry_time']
                if expiry_time == 'forever' or datetime.utcnow() <= parser.isoparse(expiry_time):
                    return jsonify({"message": "Access code is valid."}), 200
                else:
                    return jsonify({"message": "Access code expired."}), 400
            return jsonify({"message": "Invalid access code."}), 400
        return jsonify({"message": "Access code is required."}), 400
    except Exception as e:
        app.logger.error(f"Error verifying access code: {e}")
        return jsonify({"message": "An error occurred while verifying access code."}), 500

@app.route('/whitelisted_users', methods=['GET', 'DELETE'])
def whitelisted_users():
    if request.method == 'GET':
        users = db.reference('whitelisted_users').get()
        return jsonify(users), 200

    if request.method == 'DELETE':
        email = request.json.get('email')
        if email:
            ref = db.reference('whitelisted_users').order_by_child('email').equal_to(email).get()
            for key in ref.keys():
                db.reference('whitelisted_users').child(key).delete()
            ref = db.reference('access_codes').order_by_child('email').equal_to(email).get()
            for key in ref.keys():
                db.reference('access_codes').child(key).delete()
            return jsonify({"message": f"Whitelisted user {email} removed."}), 200
        return jsonify({"message": "Email is required."}), 400

if __name__ == '__main__':
    app.run(port=5000)
