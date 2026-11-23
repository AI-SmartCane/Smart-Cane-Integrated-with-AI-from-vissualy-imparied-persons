import json
import os
import subprocess

try:
    from object_detection.intent_classifier import IntentClassifier
    from object_detection.destinations import DestinationMatcher
except ImportError:  # running the file directly
    from intent_classifier import IntentClassifier
    from destinations import DestinationMatcher

NLP_DIR = "/home/jc-bose-lab/ros2_ws/models/nlp"
NER_PYTHON = "/home/jc-bose-lab/ner_env/bin/python"


class NlpPipeline:

    def __init__(self, nlp_dir=NLP_DIR):
        self.intent = IntentClassifier(
            os.path.join(nlp_dir, "intent_bilstm_weights.npz"),
            os.path.join(nlp_dir, "word_to_index.json"),
        )

        dest_file = os.path.join(nlp_dir, "destinations.json")
        self.matcher = (DestinationMatcher(dest_file)
                        if os.path.exists(dest_file) else None)
        if self.matcher is None:
            print("WARNING: destinations.json not found - destination names "
                  "will not be standardised.", flush=True)

        ner_path = os.path.join(nlp_dir, "sit_destination_ner_model")
        helper = os.path.join(nlp_dir, "ner_helper.py")
        for needed in (NER_PYTHON, helper, ner_path):
            if not os.path.exists(needed):
                raise RuntimeError("Not found: " + needed)

        self.ner_proc = subprocess.Popen(
            [NER_PYTHON, helper, ner_path],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            universal_newlines=True, bufsize=1)
        first = self.ner_proc.stdout.readline().strip()
        if first != "READY":
            raise RuntimeError("NER helper failed to start (see messages above)")

    def extract_destination(self, sentence):
        self.ner_proc.stdin.write(sentence.replace("\n", " ") + "\n")
        self.ner_proc.stdin.flush()
        reply = self.ner_proc.stdout.readline()
        return json.loads(reply)["destination"]

    def close(self):
        if self.ner_proc and self.ner_proc.poll() is None:
            self.ner_proc.terminate()

    def process(self, text):
        text = (text or "").strip()
        result = {
            "text": text,
            "is_navigation": False,
            "non_nav_probability": None,
            "destination": None,
            "raw_destination": None,
            "known_place": False,
        }
        if not text:
            return result

        p_non_nav = self.intent.non_navigation_probability(text)
        result["non_nav_probability"] = p_non_nav
        result["is_navigation"] = p_non_nav < 0.5

        if result["is_navigation"]:
            raw = self.extract_destination(text)
            result["raw_destination"] = raw
            standard = self.matcher.match(raw) if (self.matcher and raw) else None
            result["known_place"] = standard is not None
            result["destination"] = standard if standard else raw
        return result


if __name__ == "__main__":
    pipeline = NlpPipeline()
    print("NLP test mode. Type a sentence (or 'q' to quit).")
    while True:
        sentence = input("> ").strip()
        if sentence.lower() == "q":
            break
        r = pipeline.process(sentence)
        print("  Intent     :", "NAVIGATION" if r["is_navigation"]
              else "NON-NAVIGATION")
        if r["is_navigation"]:
            print("  Heard      :", r["raw_destination"])
            print("  Destination:", r["destination"],
                  "" if r["known_place"] else "  (not in destinations.json)")
    pipeline.close()
