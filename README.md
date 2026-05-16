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

## notes

only use this for research purposes, reverse engineering hcaptcha probably breaks their tos!!!!