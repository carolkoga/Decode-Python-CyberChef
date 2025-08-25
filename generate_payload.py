import os
import base64
import hashlib
from pathlib import Path

KEY = 0x42  # 0x42 = 66 decimal

PLAIN = br"""BEGIN_PAYLOAD
id: 2025-01
url: http://example[.]com/update
path: C:\Users\Public\Documents\update.bin
user_agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
note: Sample benign payload for CyberChef demo
END_PAYLOAD
"""

def xor_single_byte(data: bytes, key: int) -> bytes:
    return bytes([b ^ key for b in data])

def ensure_dirs(base: Path):
    for sub in ("payload", "hashes", "iocs", "screenshots"):
        (base / sub).mkdir(parents=True, exist_ok=True)

def write_bytes(path: Path, data: bytes):
    with open(path, "wb") as f:
        f.write(data)

def write_text(path: Path, text: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def hash_bytes(data: bytes):
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "sha512": hashlib.sha512(data).hexdigest(),
    }

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    ensure_dirs(base_dir)

    plain_path = base_dir / "payload" / "payload_plain.txt"
    obf_path = base_dir / "payload" / "payload_obfuscated.txt"
    hashes_path = base_dir / "hashes" / "hashes.txt"

    # 1) Salvar o payload original
    write_bytes(plain_path, PLAIN)

    # 2) XOR e Base64
    xored = xor_single_byte(PLAIN, KEY)
    b64 = base64.b64encode(xored)

    # 3) Salvar o payload ofuscado (texto Base64)
    write_bytes(obf_path, b64)

    # 4) Hashes
    h_plain = hash_bytes(PLAIN)
    h_obf = hash_bytes(b64)

    hashes_text = (
        f"Arquivo: {plain_path.name}\n"
        f"MD5: {h_plain['md5']}\n"
        f"SHA1: {h_plain['sha1']}\n"
        f"SHA256: {h_plain['sha256']}\n"
        f"SHA512: {h_plain['sha512']}\n\n"
        f"Arquivo: {obf_path.name}\n"
        f"MD5: {h_obf['md5']}\n"
        f"SHA1: {h_obf['sha1']}\n"
        f"SHA256: {h_obf['sha256']}\n"
        f"SHA512: {h_obf['sha512']}\n"
    )
    write_text(hashes_path, hashes_text)

    print(f"Chave XOR (hex): 0x{KEY:02X}")
    print(f"Gerados: {plain_path} ({len(PLAIN)} bytes), {obf_path} ({len(b64)} bytes)")
    print(f"Hashes salvos em: {hashes_path}")
    print("Decodifique no CyberChef com: From Base64 -> XOR (Single byte key 0x42).")