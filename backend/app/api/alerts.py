from fastapi import APIRouter, Query, HTTPException, Header
from typing import List, Optional
from ..schemas.schemas import AlertResponse
from ..services.alert_service import alert_service

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=List[AlertResponse])
def get_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity: CRITICAL, HIGH, WARNING, INFO"),
    district: Optional[str] = Query(None, description="Filter by district")
):
    """Retrieves live simulated hazard alerts."""
    return alert_service.get_all_alerts(severity=severity, district=district)

@router.post("/{alert_id}/ack")
def acknowledge_alert(
    alert_id: int,
    x_user_role: Optional[str] = Header("Disaster_Authority")
):
    """Marks an emergency alert as acknowledged by the incident command team."""
    if x_user_role in ("Public Citizen", "Public_Citizen"):
        raise HTTPException(status_code=403, detail="Operational authorization required to acknowledge disaster alerts")
    success = alert_service.acknowledge_alert(alert_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alert ID not found")
    return {"status": "acknowledged", "alert_id": alert_id}
