from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime
import random
import string
import os
import json

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
SPREADSHEET_NAME = "Customer Database"
WORKSHEET_NAME   = "Customers"
PORT             = int(os.environ.get("PORT", 5000))
# ─────────────────────────────────────────────

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"))
CORS(app)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def get_worksheet():
    """Connect to Google Sheets and return worksheet"""
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    
    if creds_json:
        # For Render.com deployment
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        # For local PyCharm development
        creds_path = os.path.join(BASE_DIR, "credentials.json")
        if not os.path.exists(creds_path):
            raise FileNotFoundError("credentials.json not found. Please add it to the project folder.")
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)

    client = gspread.authorize(creds)

    # Open or create spreadsheet
    try:
        spreadsheet = client.open(SPREADSHEET_NAME)
    except gspread.SpreadsheetNotFound:
        spreadsheet = client.create(SPREADSHEET_NAME)
        print(f"✅ Created new spreadsheet: {SPREADSHEET_NAME}")

    # Open or create worksheet
    try:
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows="1000", cols="20")
        print(f"✅ Created new worksheet: {WORKSHEET_NAME}")

    # Create header row if empty
    if not worksheet.get_all_values():
        headers = [
            "Order ID",
            "Full Name",
            "Wall Art Type",
            "Size",
            "Budget (₹)",
            "Address",
            "Pin Code",
            "State",
            "Phone No.",
            "Alternate Phone",
            "Submitted At"
        ]
        worksheet.append_row(headers)
        worksheet.format("A1:K1", {
            "textFormat": {"bold": True},
            "backgroundColor": {"red": 0.08, "green": 0.06, "blue": 0.15}
        })
        print("✅ Headers created in Google Sheet")

    return worksheet


def generate_order_id(worksheet):
    """Generate unique Order ID: ORD-XXXX"""
    existing_data = worksheet.get_all_values()
    existing_ids = set()
    
    if len(existing_data) > 1:
        for row in existing_data[1:]:
            if row and row[0].startswith("ORD-"):
                existing_ids.add(row[0])
    
    while True:
        random_part = ''.join(random.choices(string.digits, k=4))
        order_id = f"ORD-{random_part}"
        if order_id not in existing_ids:
            return order_id


@app.route("/")
def index():
    return send_from_directory(os.path.join(BASE_DIR, "static"), "index.html")

# ADD THIS CRITICAL ROUTE BELOW TO SERVE IMAGES
@app.route("/<path:filename>")
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/submit", methods=["POST"])
def submit_order():
    """Handle form submission and save to Google Sheets"""
    try:
        data = request.get_json()

        # Extract and validate fields
        name    = data.get("name",    "").strip()
        product = data.get("product", "").strip()
        size    = data.get("size",    "").strip()
        price   = data.get("price",   "").strip()
        address = data.get("address", "").strip()
        pincode = data.get("pincode", "").strip()
        state   = data.get("state",   "").strip()
        phone   = data.get("phone",   "").strip()
        altphone= data.get("altphone", "N/A").strip() or "N/A"

        # Validate required fields
        if not all([name, product, size, price, address, pincode, state, phone]):
            return jsonify({
                "success": False,
                "message": "All required fields must be completed."
            }), 400

        # Validate price is a number
        try:
            price_val = float(price)
        except ValueError:
            return jsonify({
                "success": False,
                "message": "Price must be a valid number."
            }), 400

        # Connect to Google Sheets
        worksheet = get_worksheet()
        order_id = generate_order_id(worksheet)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append row to worksheet
        worksheet.append_row([
            order_id,
            name,
            product,
            size,
            price_val,
            address,
            pincode,
            state,
            phone,
            altphone,
            timestamp
        ])

        print(f"✅ Order saved: {order_id} | {name}")

        return jsonify({
            "success": True,
            "message": "Order submitted successfully!",
            "customer_id": order_id,
            "timestamp": timestamp
        })

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  🎨 3D Dark Art — Order Form Server")
    print("=" * 60)
    print(f"  🌐 Local:    http://localhost:{PORT}")
    print(f"  📱 Network:  http://YOUR_IP:{PORT}")
    print("=" * 60 + "\n")
    
    app.run(host="0.0.0.0", port=PORT, debug=False)
