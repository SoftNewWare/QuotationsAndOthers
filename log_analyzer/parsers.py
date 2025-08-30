
import re
from .utils import parse_timestamp_guess

COMBINED_REGEX = re.compile(
    r'(?P<ip>\S+) (?P<identd>\S+) (?P<user>\S+) \[(?P<time>.*?)\] '
    r'"(?P<method>\S+)\s(?P<path>[^"]*?)\s(?P<protocol>HTTP/\d\.\d)" '
    r'(?P<status>\d{3}) (?P<size>\S+) "(?P<referrer>[^"]*)" "(?P<agent>[^"]*)"'
)

def parse_line(line: str, fmt: str):
    if fmt == "combined":
        m = COMBINED_REGEX.search(line)
        if not m:
            return {"raw": line}
        d = m.groupdict()
        return {
            "ip": d.get("ip"),
            "user": d.get("user"),
            "time_raw": d.get("time",""),
            "method": d.get("method"),
            "path": d.get("path"),
            "protocol": d.get("protocol"),
            "status": int(d.get("status")) if d.get("status") else None,
            "size": None if d.get("size") == "-" else int(d.get("size")),
            "referrer": d.get("referrer"),
            "agent": d.get("agent"),
            "raw": line,
        }
    else:
        return {"raw": line, "ts_guess": parse_timestamp_guess(line)}
