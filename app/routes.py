from flask import Blueprint, request, jsonify
from app import db
from app.models import UsersData

api_bp = Blueprint("api", __name__)

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

# GET A SINGLE GLUCOSE LEVEL ENTRY BY ID
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

# Register Routes Function
def register_routes(app):
    app.register_blueprint(api_bp, url_prefix="/api/v1")
