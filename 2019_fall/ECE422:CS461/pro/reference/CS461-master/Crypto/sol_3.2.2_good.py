#!/usr/bin/python
# -*- coding: utf-8 -*-
a = "I come in peace."
b = "Prepare to be destroyed!"
blob = """
                     �L����2��A��{��
f-�W�R*2ڋ����$b���:���x6M.K�U�u�Z"��b�,��co@���e�+��X.%D�.���7�M��ѧ�p�|æzJY��D1<�8)/����%�f�Ԕ�"""
from hashlib import sha256
c = sha256(blob).hexdigest()
if c == "f26036470839c9a4c366125cd065f39ee2b173e6ca73d6289ae1f1997223dc0e":
	print a
else:
	print b
