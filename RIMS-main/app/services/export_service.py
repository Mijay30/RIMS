import csv
import io
from typing import List, Dict
from ..database import Database

class ExportService:
    def __init__(self):
        self.db = Database.connect()

    def export_incidents_to_csv(self) -> str:
        incidents = list(self.db.incidents.find({}, {"_id": 0}))
        if not incidents:
            return ""

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=incidents[0].keys())
        writer.writeheader()
        writer.writerows(incidents)
        
        return output.getvalue()