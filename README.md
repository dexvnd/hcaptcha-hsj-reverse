# HSW KEY FETCHER FOR SALE
If you are looking to buy a HSW key fetcher contact me on [telegram](https://t.me/dexv0) 
<img width="959" height="273" alt="Code_fStSz0t28qvxc" src="https://github.com/user-attachments/assets/f876520c-1895-42d4-9303-bc7eb37ceb34" />


# HSJ ( inspekt_client js ;) ) reverse engineered

this is a project that reverse engineers hcaptcha's hsj.js to get the encryption keys it uses

## what it does

- hooks into hsj.js's aes key schedule and injects code to dump keys from the memory buffer
- has all the crypto stuff hsj uses (aes-gcm encryption, encoding, hashing etc)

## how to use

```python
keys = KeyFetcher("ebe7e23e88d295f1ab31b3848838e4e46a1f27169e00cbc8a839a1e1c3425e12").fetch_keys()
```

it will print out the n_key and response_decrypt_key

## files

- keyfetcher.py - the main thing, downloads hsj.js and extracts the keys
- algorithm.py - has all the helper classes (encryption, hashing, encoding etc)

## requirements

```
pycryptodome
xxhash
msgpack
jsbeautifier
requests
dexvstuff
```

`pip install pycryptodome xxhash msgpack jsbeautifier requests dexvstuff`

# Legal Disclaimer
This repository is intended for educational and research purposes only. The code and content provided here are not affiliated with, endorsed by, or associated with [hCaptcha](https://www.hcaptcha.com) or any related entities.

If you are a representative of hCaptcha and believe this repository violates your rights or terms of service, please contact me at [**dexv@dexv.lol**](mailto://dexv@dexv.lol) to request its removal. I will respond promptly to resolve the issue.
