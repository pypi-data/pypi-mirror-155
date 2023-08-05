# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Text encoding utilities, text file I/O

Functions 'get_coding', 'decode', 'encode'  come from Eric4
source code (Utilities/__init___.py) Copyright © 2003-2009 Detlev Offenbach
"""


import locale
import os
import re
import sys
from codecs import BOM_UTF8, BOM_UTF16, BOM_UTF32

PREFERRED_ENCODING = locale.getpreferredencoding()


def transcode(text, input=PREFERRED_ENCODING, output=PREFERRED_ENCODING):
    """Transcode a text string"""
    try:
        return text.decode("cp437").encode("cp1252")
    except UnicodeError:
        try:
            return text.decode("cp437").encode(output)
        except UnicodeError:
            return text


# ------------------------------------------------------------------------------
#  Functions for encoding and decoding bytes that come from
#  the *file system*.
# ------------------------------------------------------------------------------

# The default encoding for file paths and environment variables should be set
# to match the default encoding that the OS is using.
def getfilesystemencoding():
    """
    Query the filesystem for the encoding used to encode filenames
    and environment variables.
    """
    encoding = sys.getfilesystemencoding()
    if encoding is None:
        # Must be Linux or Unix and nl_langinfo(CODESET) failed.
        encoding = PREFERRED_ENCODING
    return encoding


FS_ENCODING = getfilesystemencoding()

# ------------------------------------------------------------------------------
#  Functions for encoding and decoding *text data* itself, usually originating
#  from or destined for the *contents* of a file.
# ------------------------------------------------------------------------------

# Codecs for working with files and text.
CODING_RE = re.compile(r"coding[:=]\s*([-\w_.]+)")
CODECS = [
    "utf-8",
    "iso8859-1",
    "iso8859-15",
    "ascii",
    "koi8-r",
    "cp1251",
    "koi8-u",
    "iso8859-2",
    "iso8859-3",
    "iso8859-4",
    "iso8859-5",
    "iso8859-6",
    "iso8859-7",
    "iso8859-8",
    "iso8859-9",
    "iso8859-10",
    "iso8859-13",
    "iso8859-14",
    "latin-1",
    "utf-16",
]


def get_coding(text):
    """
    Function to get the coding of a text.
    @param text text to inspect (string)
    @return coding string
    """
    for line in text.splitlines()[:2]:
        try:
            result = CODING_RE.search(str(line))
        except UnicodeDecodeError:
            # This could fail because str assume the text
            # is utf8-like and we don't know the encoding to give
            # it to str
            pass
        else:
            if result:
                codec = result.group(1)
                # sometimes we find a false encoding that can
                # result in errors
                if codec in CODECS:
                    return codec


def decode(text):
    """
    Function to decode a text.
    @param text text to decode (bytes)
    @return decoded text and encoding
    """
    try:
        if text.startswith(BOM_UTF8):
            # UTF-8 with BOM
            return str(text[len(BOM_UTF8) :], "utf-8"), "utf-8-bom"
        elif text.startswith(BOM_UTF16):
            # UTF-16 with BOM
            return str(text[len(BOM_UTF16) :], "utf-16"), "utf-16"
        elif text.startswith(BOM_UTF32):
            # UTF-32 with BOM
            return str(text[len(BOM_UTF32) :], "utf-32"), "utf-32"
        coding = get_coding(text)
        if coding:
            return str(text, coding), coding
    except (UnicodeError, LookupError):
        pass
    # Assume UTF-8
    try:
        return str(text, "utf-8"), "utf-8-guessed"
    except (UnicodeError, LookupError):
        pass
    # Assume Latin-1 (behaviour before 3.7.1)
    return str(text, "latin-1"), "latin-1-guessed"


def encode(text, orig_coding):
    """
    Function to encode a text.
    @param text text to encode (string)
    @param orig_coding type of the original coding (string)
    @return encoded text and encoding
    """
    if orig_coding == "utf-8-bom":
        return BOM_UTF8 + text.encode("utf-8"), "utf-8-bom"

    # Try saving with original encoding
    if orig_coding:
        try:
            return text.encode(orig_coding), orig_coding
        except (UnicodeError, LookupError):
            pass

    # Try declared coding spec
    coding = get_coding(text)
    if coding:
        try:
            return text.encode(coding), coding
        except (UnicodeError, LookupError):
            raise RuntimeError("Incorrect encoding (%s)" % coding)
    if (
        orig_coding
        and orig_coding.endswith("-default")
        or orig_coding.endswith("-guessed")
    ):
        coding = orig_coding.replace("-default", "")
        coding = orig_coding.replace("-guessed", "")
        try:
            return text.encode(coding), coding
        except (UnicodeError, LookupError):
            pass

    # Try saving as ASCII
    try:
        return text.encode("ascii"), "ascii"
    except UnicodeError:
        pass

    # Save as UTF-8 without BOM
    return text.encode("utf-8"), "utf-8"


def write(text, filename, encoding="utf-8", mode="wb"):
    """
    Write 'text' to file ('filename') assuming 'encoding'
    Return (eventually new) encoding
    """
    text, encoding = encode(text, encoding)
    with open(filename, mode) as textfile:
        textfile.write(text)
    return encoding


def writelines(lines, filename, encoding="utf-8", mode="wb"):
    """
    Write 'lines' to file ('filename') assuming 'encoding'
    Return (eventually new) encoding
    """
    return write(os.linesep.join(lines), filename, encoding, mode)


def read(filename, encoding="utf-8"):
    """
    Read text from file ('filename')
    Return text and encoding
    """
    text, encoding = decode(open(filename, "rb").read())
    return text, encoding


def readlines(filename, encoding="utf-8"):
    """
    Read lines from file ('filename')
    Return lines and encoding
    """
    text, encoding = read(filename, encoding)
    return text.split(os.linesep), encoding
