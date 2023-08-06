#!/usr/bin/env python
# -*- coding: utf8 -*-
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
from zenutils.sixutils import *

__all__ = [
    "method_load",
    "get_file_hash",
    "get_file_md5",
    "get_file_sha",
    "get_file_sha1",
    "get_file_sha224",
    "get_file_sha256",
    "get_file_sha384",
    "get_file_sha512",
    "get_hash_hexdigest",
    "get_md5",
    "get_sha",
    "get_sha1",
    "get_sha224",
    "get_sha256",
    "get_sha384",
    "get_sha512",
    "get_md5_hexdigest",
    "get_sha_hexdigest",
    "get_sha1_hexdigest",
    "get_sha224_hexdigest",
    "get_sha256_hexdigest",
    "get_sha384_hexdigest",
    "get_sha512_hexdigest",
    "get_hash_base64",
    "get_md5_base64",
    "get_sha_base64",
    "get_sha1_base64",
    "get_sha224_base64",
    "get_sha256_base64",
    "get_sha384_base64",
    "get_sha512_base64",
    "pbkdf2_hmac",
    "get_pbkdf2_hmac",
    "validate_pbkdf2_hmac",
    "get_pbkdf2_md5",
    "get_pbkdf2_sha",
    "get_pbkdf2_sha1",
    "get_pbkdf2_sha224",
    "get_pbkdf2_sha256",
    "get_pbkdf2_sha384",
    "get_pbkdf2_sha512",
    "validate_pbkdf2_md5",
    "validate_pbkdf2_sha",
    "validate_pbkdf2_sha1",
    "validate_pbkdf2_sha224",
    "validate_pbkdf2_sha256",
    "validate_pbkdf2_sha384",
    "validate_pbkdf2_sha512",
]

import re
import string
import hashlib
import functools

# ##################################################################################
# being: copy from hashlib of python3.9 to fix pbkdf2_hmac missing in python3.3/python3.2
# ##################################################################################
try:
    # OpenSSL's PKCS5_PBKDF2_HMAC requires OpenSSL 1.0+ with HMAC and SHA
    from hashlib import pbkdf2_hmac
except ImportError:
    _trans_5C = bytes((x ^ 0x5C) for x in range(256))
    _trans_36 = bytes((x ^ 0x36) for x in range(256))

    def pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None):
        """Password based key derivation function 2 (PKCS #5 v2.0)

        This Python implementations based on the hmac module about as fast
        as OpenSSL's PKCS5_PBKDF2_HMAC for short passwords and much faster
        for long passwords.
        """
        if not isinstance(hash_name, str):
            raise TypeError(hash_name)

        if not isinstance(password, (bytes, bytearray)):
            password = bytes(memoryview(password))
        if not isinstance(salt, (bytes, bytearray)):
            salt = bytes(memoryview(salt))

        # Fast inline HMAC implementation
        inner = hashlib.new(hash_name)
        outer = hashlib.new(hash_name)
        blocksize = getattr(inner, 'block_size', 64)
        if len(password) > blocksize:
            password = hashlib.new(hash_name, password).digest()
        password = password + b'\x00' * (blocksize - len(password))
        inner.update(password.translate(_trans_36))
        outer.update(password.translate(_trans_5C))

        def prf(msg, inner=inner, outer=outer):
            # PBKDF2_HMAC uses the password as key. We can re-use the same
            # digest objects and just update copies to skip initialization.
            icpy = inner.copy()
            ocpy = outer.copy()
            icpy.update(msg)
            ocpy.update(icpy.digest())
            return ocpy.digest()

        if iterations < 1:
            raise ValueError(iterations)
        if dklen is None:
            dklen = outer.digest_size
        if dklen < 1:
            raise ValueError(dklen)

        dkey = b''
        loop = 1
        from_bytes = int.from_bytes
        while len(dkey) < dklen:
            prev = prf(salt + loop.to_bytes(4, 'big'))
            # endianness doesn't matter here as long to / from use the same
            rkey = int.from_bytes(prev, 'big')
            for i in range(iterations - 1):
                prev = prf(prev)
                # rkey = rkey ^ prev
                rkey ^= from_bytes(prev, 'big')
            loop += 1
            dkey += rkey.to_bytes(inner.digest_size, 'big')

        return dkey[:dklen]

    hashlib.pbkdf2_hmac = pbkdf2_hmac
# ##################################################################################
# end: copy from hashlib of python3.9 to fix pbkdf2_hmac missing in python3.3/python3.2
# ##################################################################################

def method_load(method):
    """Get hash generator class by method name.

    @Returns:
        (hash generator class)
    
    @Parameters:
        method(str, bytes, hash generator class): Hash generator class name.
    """
    if isinstance(method, STR_TYPE):
        return getattr(hashlib, method)
    if isinstance(method, BYTES_TYPE):
        return getattr(hashlib, force_text(method))
    return method

def get_file_hash(filename, method, buffer_size=1024*64):
    method = method_load(method)
    gen = method()
    with open(filename, "rb") as fobj:
        while True:
            buffer = fobj.read(buffer_size)
            if not buffer:
                break
            gen.update(buffer)
    return gen.hexdigest()

get_file_md5 = functools.partial(get_file_hash, method=hashlib.md5)
get_file_sha = functools.partial(get_file_hash, method=hashlib.sha1)
get_file_sha1 = functools.partial(get_file_hash, method=hashlib.sha1)
get_file_sha224 = functools.partial(get_file_hash, method=hashlib.sha224)
get_file_sha256 = functools.partial(get_file_hash, method=hashlib.sha256)
get_file_sha384 = functools.partial(get_file_hash, method=hashlib.sha384)
get_file_sha512 = functools.partial(get_file_hash, method=hashlib.sha512)

def get_hash_hexdigest(*args, **kwargs):
    method = kwargs.get("method", "md5")
    gen_class = method_load(method)
    gen = gen_class()
    for arg in args:
        gen.update(force_bytes(arg))
    result = force_text(gen.hexdigest())
    return result

get_md5 = get_md5_hexdigest = functools.partial(get_hash_hexdigest, method=hashlib.md5)
get_sha = get_sha_hexdigest = functools.partial(get_hash_hexdigest, method=hashlib.sha1)
get_sha1 = get_sha1_hexdigest = functools.partial(get_hash_hexdigest, method=hashlib.sha1)
get_sha224 = get_sha224_hexdigest = functools.partial(get_hash_hexdigest, method=hashlib.sha224)
get_sha256 = get_sha256_hexdigest = functools.partial(get_hash_hexdigest, method=hashlib.sha256)
get_sha384 = get_sha384_hexdigest = functools.partial(get_hash_hexdigest, method=hashlib.sha384)
get_sha512 = get_sha512_hexdigest = functools.partial(get_hash_hexdigest, method=hashlib.sha512)

def get_hash_base64(*args, **kwargs):
    from zenutils import strutils
    from zenutils import base64utils
    method = kwargs.get("method", "md5")
    gen_class = method_load(method)
    gen = gen_class()
    for arg in args:
        gen.update(force_bytes(arg))
    data = gen.digest()
    result = force_text(base64utils.encodebytes(data))
    return strutils.join_lines(result)

get_md5_base64 = functools.partial(get_hash_base64, method=hashlib.md5)
get_sha_base64 = functools.partial(get_hash_base64, method=hashlib.sha1)
get_sha1_base64 = functools.partial(get_hash_base64, method=hashlib.sha1)
get_sha224_base64 = functools.partial(get_hash_base64, method=hashlib.sha224)
get_sha256_base64 = functools.partial(get_hash_base64, method=hashlib.sha256)
get_sha384_base64 = functools.partial(get_hash_base64, method=hashlib.sha384)
get_sha512_base64 = functools.partial(get_hash_base64, method=hashlib.sha512)


def get_pbkdf2_hmac(text, salt=None, iterations=2048, hash_name="sha256"):
    from zenutils import strutils
    from zenutils import base64utils

    if salt is None:
        salt = strutils.random_string(16, choices=string.ascii_letters)
    text = force_bytes(text)
    salt = force_bytes(salt)
    data = hashlib.pbkdf2_hmac(hash_name, text, salt, iterations)
    return "pbkdf2_{hash_name}${iterations}${salt}${data}".format(
        hash_name=TEXT(hash_name),
        iterations=iterations,
        salt=TEXT(salt),
        data=strutils.join_lines(TEXT(base64utils.encodebytes(data))),
    )

def validate_pbkdf2_hmac(password, text):
    text = force_text(text)
    matches = re.findall("pbkdf2_(.+)\\$(\\d+)\\$(.+)\\$(.+)", text)
    if len(matches) != 1:
        return False
    hash_name, iterations, salt, _ = matches[0]
    if not iterations.isdigit():
        return False
    else:
        iterations = int(iterations)
    data = get_pbkdf2_hmac(password, salt=salt, iterations=iterations, hash_name=hash_name)
    if data == text:
        return True
    else:
        return False

get_pbkdf2_sha512 = functools.partial(get_pbkdf2_hmac, hash_name="sha512")
validate_pbkdf2_sha512 = validate_pbkdf2_hmac

get_pbkdf2_sha384 = functools.partial(get_pbkdf2_hmac, hash_name="sha384")
validate_pbkdf2_sha384 = validate_pbkdf2_hmac

get_pbkdf2_sha256 = functools.partial(get_pbkdf2_hmac, hash_name="sha256")
validate_pbkdf2_sha256 = validate_pbkdf2_hmac

get_pbkdf2_sha224 = functools.partial(get_pbkdf2_hmac, hash_name="sha224")
validate_pbkdf2_sha224 = validate_pbkdf2_hmac

get_pbkdf2_sha1 = functools.partial(get_pbkdf2_hmac, hash_name="sha1")
validate_pbkdf2_sha1 = validate_pbkdf2_hmac

get_pbkdf2_sha = functools.partial(get_pbkdf2_hmac, hash_name="sha1")
validate_pbkdf2_sha = validate_pbkdf2_hmac

get_pbkdf2_md5 = functools.partial(get_pbkdf2_hmac, hash_name="md5")
validate_pbkdf2_md5 = validate_pbkdf2_hmac
