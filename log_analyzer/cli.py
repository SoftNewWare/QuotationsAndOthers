
import argparse, time
from datetime import datetime, timezone
from .parsers import parse_line
from .rules import load_rules
from .utils import parse_timestamp_guess, to_iso, parse_window
from .anomaly import ErrorRateAnomaly
from .sink import FindingSink

def iter_lines(fp, tail=False):
    if not tail:
        for i, line in enumerate(fp, 1):
            yield i, line.rstrip("\n")
        return
    fp.seek(0, 2)
    line_no = 0
    while True:
        pos = fp.tell()
        line = fp.readline()
        if not line:
            time.sleep(0.5)
            fp.seek(pos)
            continue
        line_no += 1
        yield line_no, line.rstrip("\n")

def main(argv=None):
    p = argparse.ArgumentParser(description="Log Analyzer (starter)")
    p.add_argument("--file", required=True, help="Path to log file")
    p.add_argument("--format", default="generic", choices=["generic","combined"], help="Log format")
    p.add_argument("--rules", required=True, help="Path to YAML rules file")
    p.add_argument("--out", default="out/findings.jsonl", help="Path to JSONL output")
    p.add_argument("--tail", action="store_true", help="Follow file for new lines")
    p.add_argument("--window-flush", default="1m", help="How often to flush anomaly buckets")
    args = p.parse_args(argv)

    rules = load_rules(args.rules)
    sink = FindingSink(args.out)
    anomaly = ErrorRateAnomaly(history=60)
    flush_secs = parse_window(args.window_flush) or 60
    next_flush = time.time() + flush_secs

    with open(args.file, "r", errors="ignore", encoding="utf-8") as fp:
        for line_no, line in iter_lines(fp, tail=args.tail):
            parsed = parse_line(line, args.format)
            ts = parsed.get("ts_guess") or parse_timestamp_guess(line)
            for r in rules:
                if r.match(line):
                    sink.write({
                        "ts": to_iso(ts),
                        "rule_id": r.id,
                        "severity": r.severity,
                        "line_no": line_no,
                        "line": line[:1000],
                        "description": r.description,
                        "format": args.format,
                    })
            anomaly.add_line(ts, line)

            if time.time() >= next_flush:
                current_bucket = datetime.now(timezone.utc).replace(second=0, microsecond=0)
                for (b, val, m, sd, z) in anomaly.flush_bucket(current_bucket):
                    sink.write({
                        "ts": b.isoformat().replace("+00:00","Z"),
                        "type": "anomaly",
                        "metric": "error_rate_per_min",
                        "value": val,
                        "zscore": round(z, 2),
                        "baseline_mean": round(m, 2),
                        "baseline_sd": round(sd, 2),
                    })
                next_flush = time.time() + flush_secs

    sink.close()

if __name__ == "__main__":
    main()
