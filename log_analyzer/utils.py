
import re
from datetime import datetime, timezone

WINDOW_PATTERN = re.compile(r"^(\d+)([smhd])$")

def parse_window(s: str):
    """Convert window like '5m', '1h', '30s', '2d' to seconds (int)."""
    if not s:
        return None
    m = WINDOW_PATTERN.match(s.strip())
    if not m:
        raise ValueError(f"Invalid window: {s}")
    value, unit = int(m.group(1)), m.group(2)
    return value * {'s':1, 'm':60, 'h':3600, 'd':86400}[unit]

def parse_timestamp_guess(line: str):
    """Tries to extract an ISO-like timestamp. Fallback to current time."""
    m = re.search(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}", line)
    if m:
        try:
            return datetime.fromisoformat(m.group(0).replace(" ", "T")).replace(tzinfo=timezone.utc)
        except Exception:
            pass
    return datetime.now(timezone.utc)

def to_iso(dt):
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

def bucket_minute(dt):
    return dt.replace(second=0, microsecond=0)
