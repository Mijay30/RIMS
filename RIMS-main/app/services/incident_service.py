from ..models.incident import IncidentStatus

class IncidentService:
    @staticmethod
    def get_next_status(current_status: IncidentStatus):
        transitions = {
            IncidentStatus.REPORTED: IncidentStatus.ASSIGNED,
            IncidentStatus.ASSIGNED: IncidentStatus.IN_PROGRESS,
            IncidentStatus.IN_PROGRESS: IncidentStatus.COMPLETED
        }
        return transitions.get(current_status)

    @staticmethod
    def validate_transition(current_status: IncidentStatus, next_status: IncidentStatus):
        allowed_next = IncidentService.get_next_status(current_status)
        return next_status == allowed_next
