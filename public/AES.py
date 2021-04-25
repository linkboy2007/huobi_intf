# -*- coding=utf-8-*-
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome
from Crypto.Cipher import AES
from binascii import b2a_hex,a2b_hex
from Crypto import Random

"""
aes加密算法
padding : PKCS7
"""

class AESUtil:

    __BLOCK_SIZE_16 = BLOCK_SIZE_16 = AES.block_size

    @staticmethod
    def encryt(str, key):
        cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        x = AESUtil.__BLOCK_SIZE_16 - (len(str) % AESUtil.__BLOCK_SIZE_16)
        if x != 0:
            str = str + chr(x)*x
        msg = cipher.encrypt(str.encode("utf-8"))
        return b2a_hex(msg).decode()

    @staticmethod
    def decrypt(enStr, key):
        cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        decryptByts = a2b_hex(enStr)
        msg = cipher.decrypt(decryptByts)
        ret = str(msg, encoding='utf-8')
        ret = ret.strip()
        return ret.replace('\0','').replace('\x01', '').replace('\x05', '').replace('\x06', '').replace('\x07', '').replace('\x0e', '')