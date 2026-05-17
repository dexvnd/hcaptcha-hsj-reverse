from dexvstuff import Logger, JsdomRuntime
from dexvstuff.jsdomruntime import require
import requests, time, jsbeautifier

log = Logger()

class KeyFetcher:
    def __init__(self, version: str) -> None:
        self.start_time = time.time()
        self.runtime = JsdomRuntime()
        self.runtime.runtime.HTMLCanvasElement.prototype.getContext = require('canvas').createCanvas().getContext
        self.hsj = requests.get(f"https://newassets.hcaptcha.com/c/{version}/hsj.js").text
        self.hook_hsj()

    def hook_hsj(self) -> None:
        start = time.time()
        hsj = "let dumped_keys = [];\n" + self.hsj
        hsj_lines = jsbeautifier.beautify(hsj).split("\n")

        for i in range(len(hsj_lines) - 10):
            if "- 480 |" in hsj_lines[i]:
                key_var = hsj_lines[i].split("480), ")[1].split(", ")[0]
                log.debug(f"Found key variable -> {key_var}", start=start, end=time.time())
                if "] = ~" in hsj_lines[i + 2]:
                    memory = hsj_lines[i + 2].split("] = ~")[1].split("[")[0]
                    log.debug(f"Found memory buffer -> {memory}", start=start, end=time.time())
                    key_line = hsj_lines[i].split(",")[0]
                    hsj_lines[i] = hsj_lines[i].replace(key_line, f"{key_line}, dumped_keys.push(Array.from(new Uint8Array({memory}.buffer.slice({key_var}, {key_var} + 32))))")
                    log.debug("Injected key dump into hsj.js", start=start, end=time.time())

        self.runtime.eval("\n".join(hsj_lines))

    def fetch_keys(self) -> dict:
        keys = {}

        ops = [
            ("n_key", "hsj('IiI=.eyJzIjowLCJmIjowLCJjIjowfQ==.')", 0),
            ("response_decrypt_key", "hsj(0, new Uint8Array(1024))", 1),
            #("payload_encrypt_key", "hsj(1, new Uint8Array(1024))", 2), not used in hsj, but can be fetched if needed
        ]

        for name, code, idx in ops:
            start = time.time()
            self.runtime.eval(code, suppress=True)
            key = bytes(self.runtime.eval("dumped_keys", byte_array=True)[idx]).hex()
            log.info(f"{name.replace('_', ' ').title()} -> {key}", start=start, end=time.time())
            keys[name] = key

        log.info("Fetched all keys", start=time.time(), end=self.start_time)
        return keys

print(KeyFetcher("7c83af8d9941ab9b80998e63063db44756f8bec51163fd3e28ebfddff965c582").fetch_keys())