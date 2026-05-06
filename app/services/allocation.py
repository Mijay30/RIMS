class AllocationService:
    def allocate_resource(self, incident_id: str, vehicle_id: str, staff_id: str):
        # Decide care vehicul pleacă la intervenție
        return {"success": True, "incident": incident_id, "vehicle": vehicle_id}