import os
import sys
import base64
import hashlib
import getpass

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.exceptions import InvalidKey

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR_OK = True
except ImportError:
    COLOR_OK = False

    class _Dummy:
        def __getattr__(self, name):
            return ""

    Fore = Style = _Dummy()



SALT_SIZE = 16
IV_SIZE = 16
KDF_ITERATIONS = 200_000
KEY_SIZE = 32  # AES-256
MAGIC_HEADER = b"CTK1"  # 


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    banner = rf"""{Fore.CYAN}{Style.BRIGHT}
   ______                  __        ______            ____   _ __
  / ____/______  ______  / /_____   /_  __/___  ____  / / /__(_) /_
 / /   / ___/ / / / __ \/ __/ __ \   / / / __ \/ __ \/ / //_/ / __/
/ /___/ /  / /_/ / /_/ / /_/ /_/ /  / / / /_/ / /_/ / / ,< / / /_
\____/_/   \__, / .___/\__/\____/  /_/  \____/\____/_/_/|_/_/\__/
          /____/_/
{Style.RESET_ALL}{Fore.YELLOW}        SHA256 * SHA512 * MD5 * File Hash * AES * Base64{Style.RESET_ALL}
{Fore.WHITE}        ------------------------------------------------------------{Style.RESET_ALL}
"""
    print(banner)


def print_menu():
    options = [
    ("1", "Calculate SHA256 Hash"),
    ("2", "Calculate SHA512 Hash"),
    ("3", "Calculate MD5 Hash"),
    ("4", "Calculate File Hash"),
    ("5", "AES Encryption"),
    ("6", "AES Decryption"),
    ("7", "Base64 Encode / Decode"),
    ("0", "Exit"),
]

    print(f"{Fore.GREEN}{Style.BRIGHT}  MENU{Style.RESET_ALL}")
    print(f"{Fore.WHITE}  " + "-" * 40)
    for key, label in options:
        print(f"  {Fore.CYAN}[{key}]{Style.RESET_ALL} {label}")
    print(f"{Fore.WHITE}  " + "-" * 40)


def pause():
    input(f"\n{Fore.MAGENTA}Press ENTER to continue...{Style.RESET_ALL}")



def info(msg):
    print(f"{Fore.GREEN}[+] {msg}{Style.RESET_ALL}")


def error(msg):
    print(f"{Fore.RED}[!] {msg}{Style.RESET_ALL}")


def prompt(msg):
    return input(f"{Fore.YELLOW}{msg}{Style.RESET_ALL}")


# --------------------------------------------------------------------------
# Hash Functions
# --------------------------------------------------------------------------
def hash_text(algo_name: str, hasher) -> None:
    text = prompt(f"Enter text to hash ({algo_name}): ")
    info(f"{algo_name} Result:")
    hasher.update(text.encode("utf-8"))
    digest = hasher.hexdigest()
    print(f"    {Fore.CYAN}{digest}{Style.RESET_ALL}")


def menu_sha256():
    hash_text("SHA256", hashlib.sha256())


def menu_sha512():
    hash_text("SHA512", hashlib.sha512())


def menu_md5():
    hash_text("MD5", hashlib.md5())


def menu_file_hash():
    path = prompt("File Path: ").strip().strip('"')
    if not os.path.isfile(path):
        error("File not found.")
        return

    print(f"{Fore.WHITE}  [1] MD5   [2] SHA256   [3] SHA512{Style.RESET_ALL}")
    choice = prompt("Choose an algorithm (1-3): ").strip()
    algo_map = {"1": hashlib.md5, "2": hashlib.sha256, "3": hashlib.sha512}
    algo_name_map = {"1": "MD5", "2": "SHA256", "3": "SHA512"}

    if choice not in algo_map:
        error("Invalid choice.")
        return

    hasher = algo_map[choice]()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
    except OSError as exc:
        error(f"The file could not be read: {exc}")
        return

    info(f"{algo_name_map[choice]} File Hash Result ({os.path.basename(path)}):")
    print(f"    {Fore.CYAN}{hasher.hexdigest()}{Style.RESET_ALL}")



def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    return kdf.derive(password.encode("utf-8"))


def aes_encrypt(plaintext: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)
    key = derive_key(password, salt)

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return MAGIC_HEADER + salt + iv + ciphertext


def aes_decrypt(blob: bytes, password: str) -> bytes:
    if not blob.startswith(MAGIC_HEADER):
        raise ValueError("Invalid or corrupted encrypted data (signature mismatch).")

    offset = len(MAGIC_HEADER)
    salt = blob[offset: offset + SALT_SIZE]
    iv = blob[offset + SALT_SIZE: offset + SALT_SIZE + IV_SIZE]
    ciphertext = blob[offset + SALT_SIZE + IV_SIZE:]

    key = derive_key(password, salt)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    try:
        return unpadder.update(padded_data) + unpadder.finalize()
    except ValueError:
        raise ValueError("Incorrect password or corrupted data.")


def menu_aes_encrypt():
    print(f"{Fore.WHITE}  [1] Encrypt text   [2] Encrypt file{Style.RESET_ALL}")
    choice = prompt("Choose an option (1-2): ").strip()

    password = getpass.getpass("Encryption password: ")
    password2 = getpass.getpass("Re-enter password: ")
    if password != password2:
        error("Passwords do not match.")
        return
    if not password:
        error("Password cannot be empty.")
        return

    if choice == "1":
        text = prompt("Enter the text to encrypt: ")
        result = aes_encrypt(text.encode("utf-8"), password)
        encoded = base64.b64encode(result).decode("utf-8")
        info("Encrypted text (Base64):")
        print(f"    {Fore.CYAN}{encoded}{Style.RESET_ALL}")

    elif choice == "2":
        path = prompt("Path of the file to encrypt: ").strip().strip('"')
        if not os.path.isfile(path):
            error("File not found.")
            return
        with open(path, "rb") as f:
            data = f.read()
        result = aes_encrypt(data, password)
        out_path = path + ".enc"
        with open(out_path, "wb") as f:
            f.write(result)
        info(f"File encrypted -> {out_path}")

    else:
        error("Invalid choice.")


def menu_aes_decrypt():
    print(f"{Fore.WHITE}  [1] Decrypt text   [2] Decrypt file{Style.RESET_ALL}")
    choice = prompt("Choose an option (1-2): ").strip()
    password = getpass.getpass("Decryption password: ")

    try:
        if choice == "1":
            encoded = prompt("Enter the encrypted text (Base64): ").strip()
            blob = base64.b64decode(encoded)
            plaintext = aes_decrypt(blob, password)
            info("Decrypted text:")
            print(f"    {Fore.CYAN}{plaintext.decode('utf-8')}{Style.RESET_ALL}")

        elif choice == "2":
            path = prompt("Path of the encrypted (.enc) file: ").strip().strip('"')
            if not os.path.isfile(path):
                error("File not found.")
                return
            with open(path, "rb") as f:
                blob = f.read()
            plaintext = aes_decrypt(blob, password)
            out_path = path[:-4] if path.endswith(".enc") else path + ".dec"
            with open(out_path, "wb") as f:
                f.write(plaintext)
            info(f"File decrypted -> {out_path}")

        else:
            error("Invalid choice.")

    except (ValueError, InvalidKey) as exc:
        error(str(exc))
    except Exception as exc:  # unexpected errors
        error(f"Decryption failed: {exc}")


# --------------------------------------------------------------------------
# Base64
# --------------------------------------------------------------------------
def menu_base64():
    print(f"{Fore.WHITE}  [1] Encode   [2] Decode{Style.RESET_ALL}")
    choice = prompt("Choose an option (1-2): ").strip()

    if choice == "1":
        text = prompt("Enter the text to encode: ")
        result = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        info("Base64 Result:")
        print(f"    {Fore.CYAN}{result}{Style.RESET_ALL}")

    elif choice == "2":
        text = prompt("Enter the Base64 text to decode: ").strip()
        try:
            result = base64.b64decode(text).decode("utf-8")
            info("Decoded Result:")
            print(f"    {Fore.CYAN}{result}{Style.RESET_ALL}")
        except Exception as exc:
            error(f"Decoding failed: {exc}")
    else:
        error("Invalid choice.")


# --------------------------------------------------------------------------
# Main Loop
# --------------------------------------------------------------------------
MENU_ACTIONS = {
    "1": menu_sha256,
    "2": menu_sha512,
    "3": menu_md5,
    "4": menu_file_hash,
    "5": menu_aes_encrypt,
    "6": menu_aes_decrypt,
    "7": menu_base64,
}


def main():
    while True:
        clear_screen()
        print_banner()
        print_menu()
        choice = prompt("\n  Your choice: ").strip()

        clear_screen()
        print_banner()

        if choice == "0":
            print(f"{Fore.CYAN}Shutting down Crypto Toolkit. Goodbye!{Style.RESET_ALL}")
            sys.exit(0)

        action = MENU_ACTIONS.get(choice)
        if action:
            try:
                action()
            except KeyboardInterrupt:
                print()
                error("Operation cancelled.")
            except Exception as exc:
                error(f"Unexpected error: {exc}")
        else:
            error("Invalid choice, please try again.")

        pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}Exiting.{Style.RESET_ALL}")
        sys.exit(0)
