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
    # Load credentials from environment variable (for Render.com)
    # or fall back to credentials.json file (for local use)
    creds_json = os.environ.get("GOOGLE_CREDENTIALS")
    if creds_json:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        creds = Credentials.from_service_account_file(
            os.path.join(BASE_DIR, "credentials.json"), scopes=SCOPES
        )

    client = gspread.authorize(creds)

    try:
        spreadsheet = client.open(SPREADSHEET_NAME)
    except gspread.SpreadsheetNotFound:
        spreadsheet = client.create(SPREADSHEET_NAME)

    try:
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows="1000", cols="20")

    if not worksheet.get_all_values():
        headers = ["Customer ID", "Name", "Address", "Product", "Price (₹)", "Date & Time"]
        worksheet.append_row(headers)
        worksheet.format("A1:F1", {
            "textFormat": {"bold": True},
            "backgroundColor": {"red": 0.13, "green": 0.13, "blue": 0.18}
        })

    return worksheet


def generate_customer_id(worksheet):
    existing_data = worksheet.get_all_values()
    existing_ids = set()
    if len(existing_data) > 1:
        for row in existing_data[1:]:
            if row and row[0].startswith("CUST-"):
                existing_ids.add(row[0])
    while True:
        random_part = ''.join(random.choices(string.digits, k=4))
        customer_id = f"CUST-{random_part}"
        if customer_id not in existing_ids:
            return customer_id


@app.route("/")
def index():
    return send_from_directory(os.path.join(BASE_DIR, "static"), "index.html")


@app.route("/submit", methods=["POST"])
def submit_customer():
    try:
        data    = request.get_json()
        name    = data.get("name", "").strip()
        address = data.get("address", "").strip()
        product = data.get("product", "").strip()
        price   = data.get("price", "").strip()

        if not all([name, address, product, price]):
            return jsonify({"success": False, "message": "All fields are required."}), 400

        try:
            price = float(price)
        except ValueError:
            return jsonify({"success": False, "message": "Price must be a valid number."}), 400

        worksheet   = get_worksheet()
        customer_id = generate_customer_id(worksheet)
        timestamp   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        worksheet.append_row([customer_id, name, address, product, price, timestamp])

        return jsonify({
            "success":     True,
            "message":     "Details submitted successfully!",
            "customer_id": customer_id,
            "timestamp":   timestamp
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    print("=" * 50)
    print("  Customer Form Server Running...")
    print(f"  Open: http://localhost:{PORT}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=PORT, debug=False)
