from src.config.settings import Settings
from src.domain.processor import classify_alert
from src.infrastructure.database import get_connection, initialize_database
from src.infrastructure.repositories import insert_alert



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

	print(f"Alert recorded with severity: {severity}")

def load_settings():
    """
    Load application settings from environment.

    TODO (Week 3): Replace NotImplementedError with Settings.from_env().
    This should fail fast when required config is missing in local `.env` or CI env vars.
    """
    try:
        return Settings.from_env()
    except Exception as e:
        raise RuntimeError(f"Failed to load variables: {e}") from e