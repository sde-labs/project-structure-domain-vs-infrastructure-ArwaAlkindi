import logging

from pydantic import ValidationError

from src.config.settings import Settings
from src.domain.models import Alert
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

    TODO (Week 4): Return Settings.from_env().
    """
    return Settings.from_env()
    raise NotImplementedError


def build_logger(log_level: str, stream=None) -> logging.Logger:
    """
    Build and return the application logger.

    TODO (Week 4):
    - create/get a logger named "oil_well_monitoring"
    - set the logger level from `log_level`
    - attach one StreamHandler (default stream if stream is None)
    - set formatter to: %(asctime)s,%(levelname)s,%(message)s
    - avoid duplicate handlers across repeated calls in tests
    """
def build_logger(log_level: str, stream=None) -> logging.Logger:
    logger = logging.getLogger("oil_well_monitoring")
    logger.setLevel(getattr(logging, log_level))
    logger.propagate = False

    logger.handlers.clear()

    handler = logging.StreamHandler(stream)
    formatter = logging.Formatter("%(asctime)s,%(levelname)s,%(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def process_alert_event(conn, logger: logging.Logger, timestamp: str, site_id: str,
                        alert_type: str, latitude: float, longitude: float,
                        max_retries: int = 2) -> Alert:
    """
    Validate, classify, persist, and log one alert.

    TODO (Week 4):
    - log debug context before processing
    - build Alert to validate input
    - classify and persist alert
    - retry persistence failures up to `max_retries`
    - log each retry with WARNING
    - log success at INFO
    - on ValidationError use logger.exception(...) then re-raise
    - after final failed retry use logger.exception(...) then re-raise
    """
    logger.debug("processing_alert")

    try:
        _ = Alert.model_validate(
            {
                "timestamp": timestamp,
                "site_id": site_id,
                "alert_type": alert_type,
                "latitude": latitude,
                "longitude": longitude,
                "severity": "TEMP",
            }
        )
    except ValidationError:
        logger.exception("validation_failed")
        raise

    severity = classify_alert(alert_type)

    alert = Alert(
        timestamp=timestamp,
        site_id=site_id,
        alert_type=alert_type,
        severity=severity,
        latitude=latitude,
        longitude=longitude,
    )

    attempt = 0

    while attempt <= max_retries:
        try:
            insert_alert(
                conn=conn,
                timestamp=timestamp,
                site_id=site_id,
                alert_type=alert_type,
                severity=severity,
                latitude=latitude,
                longitude=longitude,
            )

            logger.info("alert_recorded")
            return alert

        except Exception:
            if attempt == max_retries:
                logger.exception("alert_processing_failed")
                raise

            attempt += 1
            logger.warning("retrying_persist")

    try:
        return Settings.from_env()
    except Exception as e:
        raise RuntimeError(f"Failed to load variables: {e}") from e