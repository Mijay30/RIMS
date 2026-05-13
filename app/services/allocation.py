class AllocationService:
    def allocate_resource(self, incident_id: str, vehicle_id: str, staff_id: str):

        return {"success": True, "incident": incident_id, "vehicle": vehicle_id}
        from .notification_service import NotificationService