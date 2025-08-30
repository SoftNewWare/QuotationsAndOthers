# Log Analyzer (Starter)

A minimal, batteries-included log analyzer you can run locally and extend.

## Features
- Parse generic line-based logs and Apache/Nginx combined access logs.
- Rule engine (YAML) with regex patterns, severity, and optional threshold counts per time window.
- Simple anomaly detection for spikes in ERROR-level lines using rolling windows and z-scores (no deps).
- Streams results to STDOUT and writes structured findings to `out/findings.jsonl`.
- Works on large files with constant memory usage (streaming).
- `--tail` mode to follow live logs.

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python -m log_analyzer.cli --file samples/sample_generic.log --rules samples/rules.yaml --out out/findings.jsonl

python -m log_analyzer.cli --file samples/sample_access.log --format combined --rules samples/rules.yaml --out out/findings.jsonl

python -m log_analyzer.cli --file /var/log/app.log --tail --rules samples/rules.yaml
```

## Rule Spec (YAML)
```yaml
rules:
  - id: failed_login
    description: "Failed login attempt"
    pattern: "failed login|authentication failure"
    severity: "medium"
    window: "5m"      # optional, counts occurrences in window
    threshold: 10     # optional, triggers if >= threshold in window

  - id: http_500
    description: "HTTP 500 in access log"
    pattern: "\s500\s"
    severity: "high"
```
- Regex is case-insensitive by default (set `case_sensitive: true` to override).

## Formats
- `generic` (default): no parsing beyond timestamp guess.
- `combined`: Apache/Nginx combined access log. Extracts: ip, identity, user, time, method, path, protocol, status, size, referrer, agent.

## Anomaly Detection
- Computes rate of `ERROR`/`WARN` lines per 1-minute buckets, keeps a rolling baseline (last 60 buckets), and flags z-score >= 3 as anomaly.

## Output
Findings are appended to JSON Lines:
```json
{"ts":"2025-01-01T12:00:00Z","rule_id":"failed_login","severity":"medium","line_no":42,"line":"..."}
```
Anomaly records use `type: "anomaly"`.

## Extend
- Add more formats in `parsers.py`.
- Add structured routing (e.g., to Kafka/Elasticsearch) in `sink.py`.
- Replace the simple anomaly detector with your model of choice.

---

© 2025-08-13
