# -*- coding: utf-8 -*-

def encodeFilename(str):
    enc_str = ''
    for i in range(0, len(str)):
        if (str[i] >= 'a' and str[i] <= 'z') or (str[i] >= 'A' and str[i] <= 'Z') or (str[i] >= '0' and str[i] <= '9') or (str[i] == '-') or (str[i] == '_'):
            enc_str += str[i]
        else:
            enc_str += '_'
    return enc_str
