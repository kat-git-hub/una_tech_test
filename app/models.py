from app import db  # Import db from your initialized Flask app
from sqlalchemy import Column, Integer, String, Float

class UsersData(db.Model):  # Ensure it inherits from db.Model
    __tablename__ = "users_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    Gerät = Column(String)
    Seriennummer = Column(String)
    Gerätezeitstempel = Column(String)
    Aufzeichnungstyp = Column(String)
    Glukosewert_Verlauf_mg_dL = Column(Float)
    Glukose_Scan_mg_dL = Column(Float)
    Nicht_numerisches_schnellwirkendes_Insulin = Column(String)
    Schnellwirkendes_Insulin_Einheiten = Column(Float)
    Nicht_numerische_Nahrungsdaten = Column(String)
    Kohlenhydrate_Gramm = Column(Float)
    Kohlenhydrate_Portionen = Column(Float)
    Nicht_numerisches_Depotinsulin = Column(String)
    Depotinsulin_Einheiten = Column(Float)
    Notizen = Column(String)
    Glukose_Teststreifen_mg_dL = Column(Float)
    Keton_mmol_L = Column(Float)
    Mahlzeiteninsulin_Einheiten = Column(Float)
    Korrekturinsulin_Einheiten = Column(Float)
    Insulin_Aenderung_durch_Anwender_Einheiten = Column(Float)
