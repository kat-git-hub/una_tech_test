import os
import csv
import glob
from flask import Blueprint, request, jsonify
from app import db
from app.models import UsersData

api_bp = Blueprint("api", __name__)

# Column mapping to ensure correct database insertion
column_mapping = {
    "Gerät": "Gerät",
    "Seriennummer": "Seriennummer",
    "Gerätezeitstempel": "Gerätezeitstempel",
    "Aufzeichnungstyp": "Aufzeichnungstyp",
    "Glukosewert-Verlauf mg/dL": "Glukosewert_Verlauf_mg_dL",
    "Glukose-Scan mg/dL": "Glukose_Scan_mg_dL",
    "Nicht numerisches schnellwirkendes Insulin": "Nicht_numerisches_schnellwirkendes_Insulin",
    "Schnellwirkendes Insulin (Einheiten)": "Schnellwirkendes_Insulin_Einheiten",
    "Nicht numerische Nahrungsdaten": "Nicht_numerische_Nahrungsdaten",
    "Kohlenhydrate (Gramm)": "Kohlenhydrate_Gramm",
    "Kohlenhydrate (Portionen)": "Kohlenhydrate_Portionen",
    "Nicht numerisches Depotinsulin": "Nicht_numerisches_Depotinsulin",
    "Depotinsulin (Einheiten)": "Depotinsulin_Einheiten",
    "Notizen": "Notizen",
    "Glukose-Teststreifen mg/dL": "Glukose_Teststreifen_mg_dL",
    "Keton mmol/L": "Keton_mmol_L",
    "Mahlzeiteninsulin (Einheiten)": "Mahlzeiteninsulin_Einheiten",
    "Korrekturinsulin (Einheiten)": "Korrekturinsulin_Einheiten",
    "Insulin-Änderung durch Anwender (Einheiten)": "Insulin_Aenderung_durch_Anwender_Einheiten"
}

# Function to Import CSV Files from `/data` (Only New Files)
def upload_csv_files():
    data_folder = os.path.join(os.getcwd(), "data")  # Absolute path to /data folder
    csv_files = glob.glob(os.path.join(data_folder, "*.csv"))  # Get all CSV files

    if not csv_files:
        return {"message": "No CSV files found in /data", "imported": 0, "skipped": 0}

    imported_files = []
    skipped_files = []

    for file in csv_files:
        user_id = os.path.splitext(os.path.basename(file))[0]  # Extract user_id from filename

        # Check if user_id already exists in the database
        existing_entry = UsersData.query.filter_by(user_id=user_id).first()
        if existing_entry:
            skipped_files.append(file)
            continue  # Skip if data already exists

        with open(file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)  # Read first row as headers

            # Convert CSV headers to database column names
            sanitized_headers = [column_mapping.get(col, col).replace(" ", "_").replace("-", "_") for col in headers]

            # Ensure required columns exist
            missing_columns = [col for col in column_mapping.keys() if col not in headers]
            if missing_columns:
                skipped_files.append(file)
                continue  # Skip files with incorrect structure

            # Bulk insert data into the database
            data = [
                UsersData(
                    user_id=user_id,
                    **dict(zip(sanitized_headers, [None if cell == "" else cell for cell in row]))
                )
                for row in reader
            ]
            db.session.bulk_save_objects(data)
            db.session.commit()
            imported_files.append(file)

    return {
        "message": f"Imported {len(imported_files)} files, skipped {len(skipped_files)} files.",
        "imported": len(imported_files),
        "skipped": len(skipped_files)
    }

# POST Endpoint to Trigger CSV Upload
@api_bp.route("/upload", methods=["POST"])
def upload_csv():
    result = upload_csv_files()
    return jsonify(result)

# GET ALL GLUCOSE LEVELS (With Filters, Pagination, Sorting)
@api_bp.route("/levels", methods=["GET"])
def get_glucose_levels():
    user_id = request.args.get("user_id")
    start_time = request.args.get("start")  # Optional start timestamp filter
    end_time = request.args.get("stop")  # Optional end timestamp filter
    page = request.args.get("page", 1, type=int)  # Pagination
    per_page = request.args.get("per_page", 10, type=int)  # Limit results per page

    query = UsersData.query

    if user_id:
        query = query.filter_by(user_id=user_id)
    if start_time:
        query = query.filter(UsersData.Gerätezeitstempel >= start_time)
    if end_time:
        query = query.filter(UsersData.Gerätezeitstempel <= end_time)

    # Sorting (newest first)
    query = query.order_by(UsersData.Gerätezeitstempel.desc())

    # Pagination
    paginated_data = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total": paginated_data.total,
        "page": paginated_data.page,
        "per_page": paginated_data.per_page,
        "data": [
            {
                "id": entry.id,
                "user_id": entry.user_id,
                "timestamp": entry.Gerätezeitstempel,  # String format
                "glucose_value_trend": entry.Glukosewert_Verlauf_mg_dL,
                "glucose_scan": entry.Glukose_Scan_mg_dL,
                "insulin_units": entry.Schnellwirkendes_Insulin_Einheiten,
                "carbs_grams": entry.Kohlenhydrate_Gramm,
                "carbs_portions": entry.Kohlenhydrate_Portionen,
                "notes": entry.Notizen
            } for entry in paginated_data.items
        ]
    })

# ✅ GET A SINGLE GLUCOSE LEVEL ENTRY BY ID
@api_bp.route("/levels/<int:id>", methods=["GET"])
def get_glucose_by_id(id):
    entry = UsersData.query.get(id)
    if not entry:
        return jsonify({"error": "Glucose entry not found"}), 404

    return jsonify({
        "id": entry.id,
        "user_id": entry.user_id,
        "timestamp": entry.Gerätezeitstempel,
        "glucose_value_trend": entry.Glukosewert_Verlauf_mg_dL,
        "glucose_scan": entry.Glukose_Scan_mg_dL,
        "insulin_units": entry.Schnellwirkendes_Insulin_Einheiten,
        "carbs_grams": entry.Kohlenhydrate_Gramm,
        "carbs_portions": entry.Kohlenhydrate_Portionen,
        "notes": entry.Notizen
    })

# ✅ Register Routes Function
def register_routes(app):
    app.register_blueprint(api_bp, url_prefix="/api/v1")
