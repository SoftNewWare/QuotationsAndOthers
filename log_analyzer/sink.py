
import json, os

class FindingSink:
    def __init__(self, path=None):
        self.path = path
        if path:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self.fh = open(path, "a", encoding="utf-8")
        else:
            self.fh = None

    def write(self, obj):
        line = json.dumps(obj, ensure_ascii=False)
        if self.fh:
            self.fh.write(line + "\n")
            self.fh.flush()
        print(line)

    def close(self):
        if self.fh:
            self.fh.close()
