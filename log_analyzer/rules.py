
import re
from typing import Optional, List
from .utils import parse_window

class Rule:
    def __init__(self, rid: str, description: str, pattern: str, severity: str = "low",
                 window: Optional[str] = None, threshold: Optional[int] = None,
                 case_sensitive: bool = False):
        flags = 0 if case_sensitive else re.IGNORECASE
        self.id = rid
        self.description = description
        self.pattern = re.compile(pattern, flags)
        self.severity = severity
        self.window_seconds = parse_window(window) if window else None
        self.threshold = threshold

    def match(self, line: str) -> bool:
        return bool(self.pattern.search(line))

def load_rules(path: str) -> List['Rule']:
    import yaml
    with open(path, "r") as f:
        cfg = yaml.safe_load(f) or {}
    rules = []
    for r in (cfg.get("rules") or []):
        rules.append(
            Rule(
                rid=r.get("id"),
                description=r.get("description",""),
                pattern=r.get("pattern",""),
                severity=r.get("severity","low"),
                window=r.get("window"),
                threshold=r.get("threshold"),
                case_sensitive=r.get("case_sensitive", False),
            )
        )
    return rules
