"""Constants used throughout project and that can be used by user"""
from collections import namedtuple
from enum import Enum


LidarModel = namedtuple("LidarModel", ("id", "name"))


# TLV constant
_Tlv = namedtuple("TLV", "type length value")
_TreeNode = namedtuple("TreeNode", "type children leaf_value")
# Structure Format definition (see https://docs.python.org/3/library/struct.html#format-strings):
# Meant to be used as: _STRUCT_FORMAT % length
_STRUCT_FORMAT = "<"  # little endian
_STRUCT_FORMAT += "L"  # unsigned long        (field 'T' ie. 'Type')
_STRUCT_FORMAT += "L"  # unsigned long        (field 'L' ie. 'Length')
_STRUCT_FORMAT += "%ds"  # buffer of fixed size (field 'V' ie. 'Value')
