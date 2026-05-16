from dexvstuff import Logger, Wabt, JsdomRuntime
from dexvstuff.jsdomruntime import require
import requests, time, jsbeautifier

log = Logger()

class KeyFetcher:
    def __init__(self, version: str) -> None:
        self.start_time = time.time()
        self.wabt = Wabt()
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
        ]

        for name, code, idx in ops:
            start = time.time()
            self.runtime.eval(code, suppress=True)
            key = bytes(self.runtime.eval("dumped_keys", byte_array=True)[idx]).hex()
            log.info(f"{name.replace('_', ' ').title()} -> {key}", start=start, end=time.time())
            keys[name] = key

        log.info("Fetched all keys", start=time.time(), end=self.start_time)
        return keys

print(KeyFetcher("ebe7e23e88d295f1ab31b3848838e4e46a1f27169e00cbc8a839a1e1c3425e12").fetch_keys())