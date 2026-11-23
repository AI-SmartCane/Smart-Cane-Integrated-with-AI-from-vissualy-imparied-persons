import queue
import subprocess
import threading
import time

import numpy as np
import rclpy
import serial

from rclpy.node import Node
from std_msgs.msg import String

OUT_RATE = 7812.5        # samples per second played by the Arduino
CHUNK = 64
SPEECH_SPEED = 125       # words per minute


def make_audio(text):
    """Text -> 8-bit audio at 7812.5 Hz (None if espeak-ng is missing)."""
    try:
        wav = subprocess.run(
            ["espeak-ng", "--stdout", "-s", str(SPEECH_SPEED), text],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout
    except FileNotFoundError:
        return None
    pos = wav.find(b"data")
    if pos < 0:
        return None
    in_rate = int.from_bytes(wav[24:28], "little")
    body = wav[pos + 8:]
    x = np.frombuffer(body[:len(body) // 2 * 2],
                      dtype="<i2").astype(np.float64) / 32768.0
    if len(x) == 0:
        return None
    n = 101
    t = np.arange(n) - (n - 1) / 2
    h = np.sinc(2 * (3400.0 / in_rate) * t) * np.hamming(n)
    y = np.convolve(x, h / h.sum(), mode="same")
    grid = np.arange(int(len(y) * OUT_RATE / in_rate)) * (in_rate / OUT_RATE)
    y = np.interp(grid, np.arange(len(y)), y)
    peak = max(float(np.max(np.abs(y))), 1e-6)
    y = y / peak * 0.85
    fade = int(0.02 * OUT_RATE)
    if len(y) > 2 * fade:
        y[:fade] *= np.linspace(0, 1, fade)
        y[-fade:] *= np.linspace(1, 0, fade)
    return np.clip(y * 127 + 128, 0, 255).astype(np.uint8)


class ServoSerialNode(Node):

    def __init__(self):
        super().__init__('servo_serial_node')

        self.ser = serial.Serial(
            '/dev/ttyACM0',
            115200,
            timeout=1
        )
        self.lock = threading.Lock()

        self.subscription = self.create_subscription(
            String,
            '/servo_command',
            self.command_callback,
            10
        )

        self.switch_pub = self.create_publisher(String, '/voice_switch', 10)
        self.create_timer(0.02, self.read_serial)

        self.done_pub = self.create_publisher(String, '/speak_done', 10)
        self.create_subscription(String, '/speak_text', self.speak_callback, 10)
        self.speak_queue = queue.Queue()
        threading.Thread(target=self._speak_worker, daemon=True).start()

        self.get_logger().info("Arduino servo connection established")

    def handle_line(self, raw):
        line = raw.decode(errors='ignore').strip()
        if line == 'SWITCH_ON':
            self.switch_pub.publish(String(data='ON'))
        elif line == 'SWITCH_OFF':
            self.switch_pub.publish(String(data='OFF'))

    def read_serial(self):
        if not self.lock.acquire(False):
            return
        try:
            while self.ser.in_waiting:
                self.handle_line(self.ser.readline())
        except serial.SerialException as e:
            self.get_logger().error("Serial read error: {}".format(e))
        finally:
            self.lock.release()

    def command_callback(self, msg):

        command = msg.data.strip()

        allowed_commands = [
            'MOVE_LEFT',
            'MOVE_RIGHT',
            'GO_FORWARD',
            'STOP'
        ]

        if command not in allowed_commands:
            return
        if not self.lock.acquire(False):
            return
        try:
            self.ser.write((command + '\n').encode())
        finally:
            self.lock.release()

        self.get_logger().info(
            f"Servo command sent: {command}"
        )

    def speak_callback(self, msg):
        self.speak_queue.put(msg.data)

    def _speak_worker(self):
        while True:
            text = self.speak_queue.get()
            try:
                pcm = make_audio(text)
                if pcm is None:
                    self.get_logger().error(
                        "Cannot speak (is espeak-ng installed?): " + text)
                else:
                    with self.lock:
                        if not self.play(pcm):
                            self.get_logger().error("Speaker playback failed")
            except Exception as e:
                self.get_logger().error("Speech error: {}".format(e))
            finally:
                self.done_pub.publish(String(data=text))

    def play(self, pcm):
        total = len(pcm)
        self.ser.reset_input_buffer()
        self.ser.write(("PLAY %d\n" % total).encode())
        sent = 0
        deadline = time.time() + total / OUT_RATE + 10
        while time.time() < deadline:
            raw = self.ser.readline()
            line = raw.decode(errors='ignore').strip()
            if line == "K":
                chunk = pcm[sent:sent + CHUNK]
                if len(chunk):
                    self.ser.write(chunk.tobytes())
                    sent += len(chunk)
            elif line == "DONE":
                return True
            elif line == "ERR":
                return False
            else:
                self.handle_line(raw)
        return False

    def destroy_node(self):
        if self.ser.is_open:
            self.ser.close()

        super().destroy_node()


def main(args=None):

    rclpy.init(args=args)

    node = ServoSerialNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
