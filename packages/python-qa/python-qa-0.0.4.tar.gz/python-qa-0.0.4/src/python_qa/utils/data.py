import binascii
import os
import time


class DataGenerate:
    @staticmethod
    def mongo_id() -> str:
        timestamp = int(time.time())
        other_part = binascii.b2a_hex(os.urandom(8)).decode("ascii")
        return f"{timestamp:x}{other_part}"
