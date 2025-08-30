
from collections import deque, defaultdict
from statistics import mean, pstdev
from .utils import bucket_minute

class ErrorRateAnomaly:
    """Tracks ERROR/WARN counts per minute and flags spikes using z-score >= 3."""
    def __init__(self, history=60):
        self.history = history
        self.buffer = deque(maxlen=history)
        self.series = defaultdict(int)  # bucket -> count

    def add_line(self, dt, line: str):
        b = bucket_minute(dt)
        if "ERROR" in line or "WARN" in line:
            self.series[b] += 1

    def flush_bucket(self, current_bucket):
        keys = sorted(self.series.keys())
        anomalies = []
        for k in keys:
            if k <= current_bucket:
                val = self.series[k]
                baseline = list(self.buffer) if self.buffer else [0]
                m = mean(baseline)
                sd = pstdev(baseline) if len(baseline) > 1 else 0
                z = (val - m) / sd if sd > 0 else 0
                if z >= 3 and val >= max(5, int(m) + 5):
                    anomalies.append((k, val, m, sd, z))
                self.buffer.append(val)
                del self.series[k]
        return anomalies
