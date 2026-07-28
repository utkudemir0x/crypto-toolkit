<div align="center">

# 🔐 Crypto Toolkit

**A modern command-line cryptography toolkit written in Python**

<p>
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Cryptography-AES--256-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
</p>

Simple, fast and secure toolkit for hashing, AES encryption/decryption, Base64 operations and file hashing.

</div>

---

# ✨ Features

<table>
<tr>
<td width="50%">

### 🔑 Hashing
- SHA256
- SHA512
- MD5

</td>

<td width="50%">

### 📁 File Hash
- MD5
- SHA256
- SHA512

</td>
</tr>

<tr>
<td>

### 🔒 AES Encryption
- Encrypt Text
- Encrypt Files

</td>

<td>

### 🔓 AES Decryption
- Decrypt Text
- Decrypt Files

</td>
</tr>

<tr>
<td colspan="2">

### 📦 Utilities
- Base64 Encode
- Base64 Decode
- Colored CLI Interface

</td>
</tr>
</table>

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/utkudemir0x/crypto-toolkit.git
cd crypto-toolkit
```

Install dependencies

```bash
pip install cryptography colorama
```

---

# 🚀 Usage

Run the application

```bash
python crypto_toolkit.py
```

---

# 🖥️ Menu

```text
┌────────────────────────────────────────────┐
│                Crypto Toolkit              │
├────────────────────────────────────────────┤
│ [1] SHA256 Hash                            │
│ [2] SHA512 Hash                            │
│ [3] MD5 Hash                               │
│ [4] File Hash                              │
│ [5] AES Encryption                         │
│ [6] AES Decryption                         │
│ [7] Base64 Encode / Decode                 │
│ [0] Exit                                   │
└────────────────────────────────────────────┘
```

---

# 🔐 AES Implementation

<table>
<tr>
<th>Algorithm</th>
<td>AES-256</td>
</tr>

<tr>
<th>Mode</th>
<td>CBC</td>
</tr>

<tr>
<th>Padding</th>
<td>PKCS7</td>
</tr>

<tr>
<th>Key Derivation</th>
<td>PBKDF2-HMAC-SHA256</td>
</tr>

<tr>
<th>Salt</th>
<td>Random 16 Bytes</td>
</tr>

<tr>
<th>IV</th>
<td>Random 16 Bytes</td>
</tr>

<tr>
<th>Output</th>
<td>.enc file</td>
</tr>
</table>

---

# 📋 Requirements

| Dependency | Version |
|------------|---------|
| Python | 3.9+ |
| cryptography | Latest |
| colorama | Latest |

---

# 📂 Project Structure

```text
crypto-toolkit/
│
├── crypto_toolkit.py
└── README.md
```

---

<div align="center">

# 📜 License

Licensed under the **MIT License**

---



<p>

</p>

</div>
