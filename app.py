from datetime import date, datetime
import json
import os
import secrets
import sqlite3
from functools import wraps

from flask import Flask, flash, g, redirect, render_template, request, session, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
VILLAGE_AREA_MAP = {
    "Jalipudi": ["Main Street", "Riverside Colony", "North Hamlet", "School Road", "Market Road"],
}
VILLAGE_LOCATIONS = {
    "Bhimavaram": (16.5449, 81.5212),
    "Eluru": (16.7107, 81.0952),
    "Jalipudi": (16.6823116, 81.1409858),
    "Nuzvid": (16.7880, 80.8458),
    "Tadepalligudem": (16.8147, 81.5275),
    "Vijayawada": (16.5062, 80.6480),
}
AREA_LABELS = {
    "en": {"Main Street": "Main Street", "Market Road": "Market Road", "North Hamlet": "North Hamlet", "Riverside Colony": "Riverside Colony", "School Road": "School Road"},
    "te": {"Main Street": "మెయిన్ స్ట్రీట్", "Market Road": "మార్కెట్ రోడ్", "North Hamlet": "ఉత్తర పల్లె", "Riverside Colony": "రివర్‌సైడ్ కాలనీ", "School Road": "స్కూల్ రోడ్"},
}
FACILITY_LABELS = {
    "en": {},
    "te": {
        "Main Street Tap": "మెయిన్ స్ట్రీట్ ట్యాప్", "Community Tank": "కమ్యూనిటీ ట్యాంక్",
        "North Borewell": "ఉత్తర బోర్‌వెల్", "School Facility": "పాఠశాల సదుపాయం", "Market Tap": "మార్కెట్ ట్యాప్",
        "Public Water Tap": "పబ్లిక్ వాటర్ ట్యాప్", "Water Tank": "వాటర్ ట్యాంక్",
        "Borewell": "బోర్‌వెల్", "Community Water Facility": "కమ్యూనిటీ వాటర్ సదుపాయం",
    },
}
AVAILABILITY_LABELS = {
    "en": {"Regular": "Regular", "Irregular": "Irregular", "Shortage": "Shortage"},
    "te": {"Regular": "క్రమమైన లభ్యత", "Irregular": "అక్రమిత లభ్యత", "Shortage": "నీటి కొరత"},
}
VILLAGE_LABELS = {
    "en": {name: name for name in VILLAGE_LOCATIONS},
    "te": {"Bhimavaram": "భీమవరం", "Eluru": "ఏలూరు", "Jalipudi": "జాలిపూడి", "Nuzvid": "నూజివీడు", "Tadepalligudem": "తాడేపల్లిగూడెం", "Vijayawada": "విజయవాడ"},
}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "water-demo-secret-key")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
os.makedirs(UPLOAD_DIR, exist_ok=True)

with open(os.path.join(BASE_DIR, "translations", "en.json"), encoding="utf-8") as file:
    TRANSLATIONS = {"en": json.load(file)}
with open(os.path.join(BASE_DIR, "translations", "te.json"), encoding="utf-8") as file:
    TRANSLATIONS["te"] = json.load(file)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query(sql, params=(), one=False):
    cursor = get_db().execute(sql, params)
    rows = cursor.fetchone() if one else cursor.fetchall()
    cursor.close()
    return rows


def tr(key):
    return TRANSLATIONS[session.get("language", "en")].get(key, key)


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS water_facilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facility_name TEXT NOT NULL, location TEXT NOT NULL,
            facility_type TEXT NOT NULL, status TEXT NOT NULL,
            availability TEXT NOT NULL, users_served INTEGER DEFAULT 0,
            last_updated TEXT NOT NULL, remarks TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT, reference_id TEXT UNIQUE NOT NULL,
            user_name TEXT DEFAULT '', location TEXT NOT NULL, category TEXT NOT NULL,
            description TEXT NOT NULL, image TEXT DEFAULT '', report_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending', admin_remarks TEXT DEFAULT '', created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS survey_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT, area TEXT NOT NULL, households INTEGER NOT NULL,
            water_availability TEXT NOT NULL, functional_facilities INTEGER DEFAULT 0,
            non_functional_facilities INTEGER DEFAULT 0, remarks TEXT DEFAULT ''
        );
    """)
    facility_columns = {row[1] for row in db.execute("PRAGMA table_info(water_facilities)").fetchall()}
    for column in ("latitude", "longitude", "village", "area"):
        if column not in facility_columns:
            column_type = "REAL" if column in ("latitude", "longitude") else "TEXT"
            db.execute(f"ALTER TABLE water_facilities ADD COLUMN {column} {column_type}")
    if db.execute("SELECT COUNT(*) FROM water_facilities").fetchone()[0] == 0:
        db.executemany("""INSERT INTO water_facilities
            (facility_name, location, facility_type, status, availability, users_served, last_updated, remarks, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", [
            ("Main Street Tap", "Area 1", "Public Water Tap", "Functional", "Available", 86, "2026-08-18", "Morning and evening supply", 16.6828, 81.1404),
            ("Community Tank", "Area 2", "Water Tank", "Functional", "Partially Available", 124, "2026-08-17", "Refilled every alternate day", 16.6835, 81.1420),
            ("North Borewell", "Area 3", "Borewell", "Under Maintenance", "Not Available", 52, "2026-08-12", "Pump replacement planned", 16.6842, 81.1400),
            ("School Facility", "Area 4", "Community Water Facility", "Functional", "Available", 148, "2026-08-19", "Shared by school and nearby homes", 16.6816, 81.1424),
            ("Market Tap", "Area 2", "Public Water Tap", "Non-functional", "Not Available", 40, "2026-08-10", "Tap handle is broken", 16.6819, 81.1395),
        ])
    coordinates = {
        "Main Street Tap": (16.6828, 81.1404), "Community Tank": (16.6835, 81.1420),
        "North Borewell": (16.6842, 81.1400), "School Facility": (16.6816, 81.1424),
        "Market Tap": (16.6819, 81.1395),
    }
    for facility_name, (latitude, longitude) in coordinates.items():
        db.execute("UPDATE water_facilities SET latitude = ?, longitude = ? WHERE facility_name = ?", (latitude, longitude, facility_name))
    facility_groups = {
        "Main Street Tap": ("Jalipudi", "Main Street"),
        "Community Tank": ("Jalipudi", "Riverside Colony"),
        "North Borewell": ("Jalipudi", "North Hamlet"),
        "School Facility": ("Jalipudi", "School Road"),
        "Market Tap": ("Jalipudi", "Market Road"),
    }
    for facility_name, (village, area) in facility_groups.items():
        db.execute("UPDATE water_facilities SET village = ?, area = ? WHERE facility_name = ?", (village, area, facility_name))
    if db.execute("SELECT COUNT(*) FROM survey_data").fetchone()[0] == 0:
        db.executemany("""INSERT INTO survey_data
            (area, households, water_availability, functional_facilities, non_functional_facilities, remarks)
            VALUES (?, ?, ?, ?, ?, ?)""", [
            ("Main Street", 118, "Regular", 2, 0, "Reliable public tap access"),
            ("Riverside Colony", 156, "Irregular", 1, 1, "Tank supply is alternate days"),
            ("North Hamlet", 96, "Shortage", 0, 1, "Borewell pump under maintenance"),
            ("School Road", 142, "Regular", 2, 0, "Community facility serves the area"),
        ])
    survey_area_migration = {"Area 1": "Main Street", "Area 2": "Riverside Colony", "Area 3": "North Hamlet", "Area 4": "School Road"}
    for old_area, new_area in survey_area_migration.items():
        db.execute("UPDATE survey_data SET area = ? WHERE area = ?", (new_area, old_area))
    db.commit()
    db.close()


@app.context_processor
def inject_globals():
    language = session.get("language", "en")
    localized = dict(TRANSLATIONS[language])
    localized["area_labels"] = AREA_LABELS[language]
    localized["village_labels"] = VILLAGE_LABELS[language]
    localized["facility_labels"] = FACILITY_LABELS[language]
    localized["availability_labels"] = AVAILABILITY_LABELS[language]
    return {"t": localized, "language": language, "area_labels": AREA_LABELS[language], "village_labels": VILLAGE_LABELS[language], "availability_labels": AVAILABILITY_LABELS[language], "logged_in": session.get("admin")}


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin"):
            flash(tr("admin_required"), "error")
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.route("/set-language/<language>")
def set_language(language):
    if language in TRANSLATIONS:
        session["language"] = language
    return redirect(request.referrer or url_for("home"))


@app.route("/")
def home():
    facilities = query("SELECT * FROM water_facilities")
    stats = {
        "total": len(facilities),
        "functional": sum(item["status"] == "Functional" for item in facilities),
        "areas": len(set(item["location"] for item in facilities)),
        "households": query("SELECT SUM(households) AS total FROM survey_data", one=True)["total"] or 0,
    }
    return render_template("index.html", stats=stats)


@app.route("/water-status")
def water_status():
    facilities = query("SELECT * FROM water_facilities")
    counts = {key: sum(item["availability"] == key for item in facilities) for key in ("Available", "Partially Available", "Not Available")}
    villages = sorted(VILLAGE_LOCATIONS)
    areas = {village: sorted({item["area"] for item in facilities if item["village"] == village and item["area"]}) for village in villages}
    village_locations = {village: {"latitude": latitude, "longitude": longitude} for village, (latitude, longitude) in VILLAGE_LOCATIONS.items()}
    map_facilities = [dict(item) for item in facilities]
    focus_id = request.args.get("facility_id", type=int)
    return render_template("water_status.html", facilities=map_facilities, villages=villages, areas=areas, village_locations=village_locations, focus_id=focus_id, counts=counts)


@app.route("/facilities")
def facilities():
    search = request.args.get("search", "").strip()
    filter_value = request.args.get("filter", "All")
    sql = "SELECT * FROM water_facilities WHERE (facility_name LIKE ? OR location LIKE ? OR facility_type LIKE ?)"
    params = [f"%{search}%"] * 3
    if filter_value == "Available":
        sql += " AND availability = 'Available'"
    elif filter_value == "Not Available":
        sql += " AND availability = 'Not Available'"
    elif filter_value in ("Functional", "Non-functional"):
        sql += " AND status = ?"
        params.append(filter_value)
    rows = query(sql + " ORDER BY id", params)
    return render_template("facilities.html", facilities=rows, search=search, filter_value=filter_value)


@app.route("/report", methods=["GET", "POST"])
def report_problem():
    report_areas = sorted({row["area"] for row in query("SELECT area FROM water_facilities WHERE area IS NOT NULL AND area != ''")})
    if request.method == "POST":
        location = request.form.get("location", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        if not location or not category or not description:
            flash(tr("required_error"), "error")
            return render_template("report.html", form=request.form, report_areas=report_areas)
        reference_id = "WC-" + secrets.token_hex(3).upper()
        image = request.files.get("image")
        image_name = ""
        if image and image.filename:
            extension = os.path.splitext(image.filename)[1].lower()
            if extension in {".jpg", ".jpeg", ".png", ".webp"}:
                image_name = reference_id + extension
                image.save(os.path.join(UPLOAD_DIR, image_name))
        db = get_db()
        db.execute("""INSERT INTO reports
            (reference_id, user_name, location, category, description, image, report_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (reference_id, request.form.get("name", "").strip(), location, category,
            description, image_name, request.form.get("date") or date.today().isoformat(), datetime.now().isoformat(timespec="seconds")))
        db.commit()
        return redirect(url_for("track_report", reference_id=reference_id, submitted="1"))
    return render_template("report.html", form={}, report_areas=report_areas)


@app.route("/track", methods=["GET", "POST"])
def track_report():
    reference_id = request.values.get("reference_id", "").strip().upper()
    report = query("SELECT * FROM reports WHERE reference_id = ?", (reference_id,), one=True) if reference_id else None
    if reference_id and not report:
        flash(tr("report_not_found"), "error")
    return render_template("track.html", report=report, reference_id=reference_id, submitted=request.args.get("submitted"))


@app.route("/survey")
def survey():
    rows = query("SELECT * FROM survey_data")
    summary = {
        "households": sum(row["households"] for row in rows),
        "regular": sum(row["households"] for row in rows if row["water_availability"] == "Regular"),
        "irregular": sum(row["households"] for row in rows if row["water_availability"] == "Irregular"),
        "shortage": sum(row["households"] for row in rows if row["water_availability"] == "Shortage"),
        "functional": sum(row["functional_facilities"] for row in rows),
        "non_functional": sum(row["non_functional_facilities"] for row in rows),
    }
    return render_template("survey.html", rows=rows, summary=summary)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("email") == "admin@watercare.demo" and request.form.get("password") == "admin123":
            session["admin"] = True
            return redirect(request.args.get("next") or url_for("admin_dashboard"))
        flash(tr("login_error"), "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


@app.route("/admin")
@admin_required
def admin_dashboard():
    reports = query("SELECT * FROM reports ORDER BY created_at DESC")
    facilities = query("SELECT * FROM water_facilities ORDER BY id")
    counts = {status: sum(report["status"] == status for report in reports) for status in ("Pending", "In Progress", "Resolved")}
    category_counts = {}
    for report in reports:
        category_counts[report["category"]] = category_counts.get(report["category"], 0) + 1
    return render_template("admin.html", reports=reports, facilities=facilities, counts=counts, category_counts=category_counts)


@app.route("/admin/report/<int:report_id>", methods=["POST"])
@admin_required
def update_report(report_id):
    get_db().execute("UPDATE reports SET status = ?, admin_remarks = ? WHERE id = ?", (request.form["status"], request.form.get("remarks", ""), report_id))
    get_db().commit()
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/facility/<int:facility_id>", methods=["POST"])
@admin_required
def update_facility(facility_id):
    get_db().execute("UPDATE water_facilities SET status = ?, availability = ?, last_updated = ? WHERE id = ?", (request.form["status"], request.form["availability"], date.today().isoformat(), facility_id))
    get_db().commit()
    return redirect(url_for("admin_dashboard"))


init_db()

if __name__ == "__main__":
    app.run(debug=True)
