import hashlib, xxhash, json, zlib, time, random, base64, string, msgpack
from Crypto.Random import get_random_bytes
from urllib.parse import unquote, quote
from Crypto.Cipher import AES
from math import ceil

class HSJEncryption:
    def __init__(self, key: str) -> None:
        self.key: bytes = bytes.fromhex(key)

    def encrypt(self, data: str) -> str:
        iv = get_random_bytes(12)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=iv)
        text, tag = cipher.encrypt_and_digest(data.encode())
        encrypted = text + tag + iv + b"\x00"
        return base64.b64encode(encrypted).decode()

    def decrypt(self, data: str) -> str:
        decoded = base64.b64decode(data)
        data, tag, iv = decoded[:-29], decoded[-29:-13], decoded[-13:][:-1]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=iv)
        return cipher.decrypt_and_verify(data, tag).decode()

class ResponseEncryption:
    def __init__(self, key: str) -> None:
        self.key: bytes = bytes.fromhex(key)

    def encrypt(self, data: dict) -> bytes:
        iv = get_random_bytes(12)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=iv)
        packed_data = msgpack.packb(data)
        encrypted, tag = cipher.encrypt_and_digest(packed_data)
        return iv + encrypted + tag

    def decrypt(self, data: bytes) -> dict:
        iv, data, tag = data[:12], data[12:-16], data[-16:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=iv)
        data = cipher.decrypt_and_verify(data, tag)
        return msgpack.unpackb(data, strict_map_key=False)

class Encoding:
    def __init__(self):
        self.alphabet = string.ascii_lowercase

    def encode(self, data: str) -> list:
        key = ''.join(chr(random.randint(65, 90)) for _ in range(13))
        shift = random.randint(1, 26)
        rev_str = ' '.join(data.split()[::-1])[::-1]
        trans_str = ''.join(
            char if not char.isalpha() else
            self.alphabet[(self.alphabet.index(char.lower()) + shift) % 26].upper() if char.isupper() else
            self.alphabet[(self.alphabet.index(char.lower()) + shift) % 26]
            for char in rev_str
        )
        enc_str = ''.join(reversed(base64.b64encode(quote(trans_str).encode('utf-8')).decode('utf-8')))
        split_idx = random.randint(1, len(enc_str) - 1)
        keys = list(key)
        table = str.maketrans(
            ''.join(keys + [c.lower() for c in keys]),
            ''.join(c.lower() if c.isupper() else c.upper() for c in keys + [c.lower() for c in keys])
        )
        result = (enc_str[split_idx:] + enc_str[:split_idx]).translate(table)
        return [result, hex(shift)[2:], hex(split_idx)[2:], key]

    def decode(self, data: list) -> str:
        data, shift, split_idx, key = data
    
        shift = int(shift, 16)
        split_idx = int(split_idx, 16)
        keys = list(key)
    
        rearranged = data[-split_idx:] + data[:-split_idx]
        trans_table = str.maketrans(
            ''.join(keys + [c.lower() for c in keys]),
            ''.join([c.lower() if c.isupper() else c.upper() for c in keys + [c.lower() for c in keys]])
        )
        translated = rearranged.translate(trans_table)
        reversed_str = ''.join(reversed(translated))
        decoded = unquote(base64.b64decode(reversed_str).decode('utf-8'))
    
        return ''.join([
            char if not char.isalpha() else
            self.alphabet[(self.alphabet.index(char.lower()) - shift) % 26].upper() if char.isupper() else
            self.alphabet[(self.alphabet.index(char.lower()) - shift) % 26]
            for char in ' '.join(decoded.split()[::-1])[::-1]
        ])
    
class Hash:
    def __init__(self, data: any) -> None:
        self.data = data
        if not isinstance(self.data, str): self.data = json.dumps(self.data, separators=(",", ":"))

    def crc32(self) -> int:
        crc = zlib.crc32(self.data.encode())
        return crc

    def xx64(self) -> str:
        seed = 5575352424011909552
        return str(xxhash.xxh64_intdigest(self.data, seed=seed))

class OtherAlgorithms:
    def __init__(self) -> None:
        pass

    def hashcash(self, data: str, diff: int = 2) -> str:
        timestamp = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        salt = ''.join([random.choice(string.ascii_letters + "+/=") for _ in range(8)])
        challenge = f"1:{diff}:{timestamp}:{data}::{salt}:"
        counter, zeros = 0, '0' * int(ceil(diff / 4.0))
        while 1:
            digest = hashlib.sha1((challenge + hex(counter)[2:]).encode()).hexdigest()
            if digest[:int(ceil(diff / 4.0))] == zeros:
                return f"{challenge}{hex(counter)[2:]}"
            counter += 1
    
    def get_average(self, request_history: list) -> tuple:
        history_x = []
        history_y = []

        def get_median(data: list) -> float:
            values = sorted(data)
            mid_idx = len(values) // 2
            if len(values) % 2 != 0:
                return values[mid_idx]
            else:
                return (values[mid_idx - 1] + values[mid_idx]) / 2

        for i in request_history:
            x = i[1]
            y = i[2]

            if x > 0:
                history_x.append(x)
            if y > 0:
                history_y.append(y)

        return get_median(history_x), get_median(history_y)