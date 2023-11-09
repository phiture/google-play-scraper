import re


class Regex:
    NOT_NUMBER = re.compile("[^\d]")
    SCRIPT = re.compile("AF_initDataCallback[\s\S]*?<\/script")
    KEY_DS = re.compile("(ds:.*?)'")
    KEY_HASH = re.compile("(hash: '.*?')")
    VALUE = re.compile("data:([\s\S]*?), sideChannel: {}}\);<\/")
    REVIEWS = re.compile("\)]}'\n\n([\s\S]+)")
    PERMISSIONS = re.compile("\)]}'\n\n([\s\S]+)")
