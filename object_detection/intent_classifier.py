"""NumPy-only version of the BiLSTM navigation / non-navigation classifier.
No TensorFlow needed, so it runs easily on the Jetson TX2."""

import json
import re

import numpy as np

MAX_LEN = 21


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class IntentClassifier:

    def __init__(self, weights_path, vocab_path):
        w = np.load(weights_path)
        self.emb = w["embedding"]
        self.fw = (w["fw_kernel"], w["fw_recurrent"], w["fw_bias"])
        self.bw = (w["bw_kernel"], w["bw_recurrent"], w["bw_bias"])
        self.dense_w = w["dense_w"]
        self.dense_b = w["dense_b"]
        self.units = self.fw[1].shape[0]  # 64

        with open(vocab_path, "r") as f:
            self.word_to_index = json.load(f)

    def _tokens_to_ids(self, sentence):
        sentence = sentence.lower()
        sentence = re.sub(r"[^\w\s]", "", sentence)
        ids = [self.word_to_index[w] for w in sentence.split()
               if w in self.word_to_index]
        return ids[:MAX_LEN]

    def _run_lstm(self, ids, params):
        kernel, recurrent, bias = params
        h = np.zeros(self.units, dtype=np.float32)
        c = np.zeros(self.units, dtype=np.float32)
        for idx in ids:
            x = self.emb[idx]
            z = x @ kernel + h @ recurrent + bias
            i, f, g, o = np.split(z, 4)
            i, f, o = _sigmoid(i), _sigmoid(f), _sigmoid(o)
            g = np.tanh(g)
            c = f * c + i * g
            h = o * np.tanh(c)
        return h

    def non_navigation_probability(self, sentence):
        """Probability that the sentence is NON-navigation
        (same label order as in your notebook: 0 = NAVIGATION, 1 = NON_NAVIGATION)."""
        ids = self._tokens_to_ids(sentence)
        h_fw = self._run_lstm(ids, self.fw)
        h_bw = self._run_lstm(ids[::-1], self.bw)
        features = np.concatenate([h_fw, h_bw])
        logit = features @ self.dense_w + self.dense_b
        return float(_sigmoid(logit)[0])

    def is_navigation(self, sentence):
        return self.non_navigation_probability(sentence) < 0.5
