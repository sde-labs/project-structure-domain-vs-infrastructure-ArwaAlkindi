"""
Domain models - pure data structures with validation
"""
from pydantic import BaseModel, field_validator
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Heartbeat:
    site_id: str
    timestamp: str


@dataclass
class Alert:
    timestamp: str
    site_id: str
    alert_type: str
    severity: str
    latitude: float
    longitude: float

class Alert(BaseModel):
    """
    Alert domain model with built-in validation.
    
    TODO (Week 2): Add validators for:
    - latitude: must be between -90 and 90
    - longitude: must be between -180 and 180
    - alert_type: must be one of the valid types
    """
    timestamp: str
    site_id: str
    alert_type: str
    severity: str
    latitude: float
    longitude: float
    
    # TODO: Add @field_validator for latitude
    @field_validator('latitude')
    def check_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('latitude must be between -90 and 90')
        return v
    
    # TODO: Add @field_validator for longitude
    @field_validator('longitude')
    def check_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('longitude must be between -180 and 180')
        return v
    
    # TODO: Add @field_validator for alert_type
    # Valid types: LEAK, BLOCKAGE, PRESSURE, TEMPERATURE, ACOUSTIC
    @field_validator('alert_type')
    def check_alert_type(cls, v):
        if v not in {"LEAK", "BLOCKAGE", "PRESSURE", "TEMPERATURE", "ACOUSTIC"}:
            raise ValueError('alert_type must be LEAK, BLOCKAGE, PRESSURE, TEMPERATURE, or ACOUSTIC')
        return v


    @field_validator("timestamp")
    def validate_timestamp(cls, v: str) -> str:
        valid_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%SZ"
        ]

        for format in valid_formats:
            try:
                datetime.strptime(v, format)
                return v
            except ValueError:
                continue

        raise ValueError(
            "Invalid timestamp format. Expected formats: "
            "YYYY-MM-DD, YYYY-MM-DD HH:MM:SS, or ISO format."
        )
