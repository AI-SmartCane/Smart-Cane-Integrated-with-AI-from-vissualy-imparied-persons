import difflib
import json
import re

GENERIC = {"block", "blocks", "department", "departments", "dept",
           "building", "buildings", "bldg"}
FILLER = {"the", "at", "to", "in", "of"}
FUZZY_CUTOFF = 0.80


def _words(text):
    t = text.lower().replace("&", " and ")
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    words = [w for w in t.split() if w not in FILLER]
    joined, run = [], []
    for w in words:
        if len(w) == 1 and w.isalpha():
            run.append(w)
        else:
            if run:
                joined.append("".join(run))
                run = []
            joined.append(w)
    if run:
        joined.append("".join(run))
    return joined


def _core(text):
    return [w for w in _words(text) if w not in GENERIC]


class DestinationMatcher:

    def __init__(self, json_path):
        with open(json_path) as f:
            table = json.load(f)
        self.index = {}
        for standard, aliases in table.items():
            for alias in list(aliases) + [standard]:
                key = " ".join(_core(alias))
                if key:
                    self.index[key] = standard

    def match(self, text):
        words = _core(text or "")
        if not words:
            return None
        key = " ".join(words)

        if key in self.index:
            return self.index[key]

        best = None
        for alias, standard in self.index.items():
            a = alias.split()
            for i in range(len(words) - len(a) + 1):
                if words[i:i + len(a)] == a:
                    if best is None or len(alias) > len(best[0]):
                        best = (alias, standard)
        if best:
            return best[1]

        close = difflib.get_close_matches(
            key, list(self.index), n=1, cutoff=FUZZY_CUTOFF)
        if close:
            return self.index[close[0]]
        return None
