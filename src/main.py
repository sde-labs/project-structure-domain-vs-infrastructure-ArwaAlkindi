from domain.processor import classify_alert
from infrastructure.repositories import insert_alert


def process_alert_reading(conn, timestamp: str, site_id: str, alert_type: str, latitude: float, longitude: float,
):

	severity = classify_alert(alert_type)

	# Infrastructure I/O
	insert_alert(
		conn=conn,
		timestamp=timestamp,
		site_id=site_id,
		alert_type=alert_type,
		severity=severity,
		latitude=latitude,
		longitude=longitude,
	)


