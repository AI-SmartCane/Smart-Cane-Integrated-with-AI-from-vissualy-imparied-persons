import json
import os
import subprocess
import threading
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from object_detection.nlp_pipeline import NlpPipeline, NER_PYTHON

AUDIO_DEVICE = "plughw:CARD=WEBCAM,DEV=0"    # Logitech C270 microphone
SAMPLE_RATE = 16000
ON_TEXT = "Switch is now on."
STT_HELPER = "/home/jc-bose-lab/ros2_ws/models/nlp/stt_helper.py"
STT_MODEL_PATH = ("/home/jc-bose-lab/ros2_ws/models/stt/"
                  "faster-whisper-small.en")


class Recorder:

    def __init__(self):
        self.proc = None
        self.thread = None
        self.chunks = []

    def start(self):
        if self.proc is not None and self.proc.poll() is None:
            return                      # already recording
        self.chunks = []
        proc = subprocess.Popen(
            ["arecord", "-q", "-D", AUDIO_DEVICE,
             "-f", "S16_LE", "-c", "1", "-r", str(SAMPLE_RATE),
             "-t", "raw"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.proc = proc
        self.thread = threading.Thread(target=self._read, args=(proc,),
                                       daemon=True)
        self.thread.start()

    def _read(self, proc):
        while True:
            data = proc.stdout.read(4096)
            if not data:
                break
            self.chunks.append(data)

    def stop(self):
        proc = self.proc
        if proc is None:
            return b"", ""
        proc.terminate()
        proc.wait()
        if self.thread is not None:
            self.thread.join(timeout=2)
        err = proc.stderr.read().decode(errors="ignore").strip()
        self.proc = None
        return b"".join(self.chunks), err


class SpeechToText:

    def __init__(self):
        for needed in (NER_PYTHON, STT_HELPER, STT_MODEL_PATH):
            if not os.path.exists(needed):
                raise RuntimeError("Not found: " + needed)
        self.proc = subprocess.Popen(
            [NER_PYTHON, STT_HELPER, STT_MODEL_PATH],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        first = self.proc.stdout.readline().strip()
        if first != b"READY":
            raise RuntimeError(
                "Speech helper failed to start (see messages above)")

    def transcribe(self, pcm):
        self.proc.stdin.write(("AUDIO %d\n" % len(pcm)).encode())
        self.proc.stdin.write(pcm)
        self.proc.stdin.flush()
        reply = self.proc.stdout.readline().decode()
        return json.loads(reply)["text"]

    def close(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()


class Speaker:
    """Asks servo_serial_node (which owns the Arduino) to speak a message."""

    def __init__(self, node):
        self.pub = node.create_publisher(String, '/speak_text', 10)

    def say(self, text):
        print("[SPEAK]", text, flush=True)
        self.pub.publish(String(data=text))


class VoiceNode(Node):

    def __init__(self):
        super().__init__('voice_node')

        self.get_logger().info("Loading speech and NLP models...")
        self.speaker = Speaker(self)
        self.stt = SpeechToText()
        self.nlp = NlpPipeline()

        self.dest_pub = self.create_publisher(String, '/destination', 10)

        self.recorder = Recorder()
        self.recording = False
        self.switch_on = False
        self.pending_start = False
        self.pending_since = 0.0

        self.create_subscription(
            String, '/voice_switch', self.switch_callback, 10)
        self.create_subscription(
            String, '/speak_done', self.speak_done_callback, 10)
        self.create_timer(0.5, self.check_pending)
        self.get_logger().info(
            "Voice node ready. Switch ON = speak, switch OFF = process.")
        # Announce once, a moment later, so the speaker node has connected.
        self.ready_timer = self.create_timer(2.0, self.announce_ready)

    def announce_ready(self):
        self.ready_timer.cancel()
        self.speaker.say("Model ready.")

    def switch_callback(self, msg):
        self.switch_on = (msg.data == 'ON')
        if self.switch_on:
            if not self.recording and not self.pending_start:
                self.pending_start = True
                self.pending_since = time.time()
                self.speaker.say(ON_TEXT)
        else:
            self.pending_start = False
            if self.recording:
                self.stop_and_process()

    def speak_done_callback(self, msg):
        if msg.data == ON_TEXT and self.pending_start:
            self.pending_start = False
            if self.switch_on and not self.recording:
                self.start_recording()

    def check_pending(self):
        if self.pending_start and time.time() - self.pending_since > 8.0:
            self.pending_start = False
            if self.switch_on and not self.recording:
                self.start_recording()

    def start_recording(self):
        if self.recording:
            return
        self.recording = True
        self.recorder.start()
        print("\n[MIC ON] Listening... speak now. Turn the switch OFF "
              "when you finish.", flush=True)

    def stop_and_process(self):
        self.recording = False
        pcm, err = self.recorder.stop()
        print("[MIC OFF] Processing speech...", flush=True)
        self.speaker.say("Switch is now off. Model processing, please wait.")

        if len(pcm) < SAMPLE_RATE * 2 * 0.3:
            print("No audio captured. arecord said:", err or "(nothing)")
            self.speaker.say("I did not hear anything.")
            return

        text = self.stt.transcribe(pcm)
        print("You said     :", repr(text))
        if not text:
            print("Could not understand any speech.")
            self.speaker.say("I could not understand any speech.")
            return

        result = self.nlp.process(text)
        if result["is_navigation"]:
            print("Intent       : NAVIGATION")
            if result["known_place"]:
                print("Destination  :", result["destination"])
                self.dest_pub.publish(String(data=result["destination"]))
                self.speaker.say("Model intent: Navigation. Destination: "
                                 + result["destination"])
            elif result["raw_destination"]:
                print("Destination  : not found in your map (heard: "
                      + repr(result["raw_destination"]) + ")")
                self.speaker.say("Model intent: Navigation. "
                                 "Destination not found in your map.")
            else:
                print("Destination  : none heard")
                self.speaker.say(
                    "Model intent: Navigation. No destination found.")
        else:
            print("Intent       : NON-NAVIGATION")
            self.speaker.say("Model intent: Non navigation.")

    def destroy_node(self):
        if self.recording:
            self.recorder.stop()
        self.stt.close()
        self.nlp.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = VoiceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
