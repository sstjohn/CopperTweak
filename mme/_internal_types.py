## This file is part of CopperTweak
## Copyright (C) 2012 Saul St. John <saul.stjohn@gmail.com>
## This program is published under a GPLv2 license

from scapy.fields import FieldListField, ConditionalField, Field

def TypeConditionalField(t, f):
        cond = lambda p: p.mmtype == t
        return ConditionalField(f, cond)

def ArrayField(name, default, field, count):
	return FieldListField(name, [default] * count, field, 
				count_from = lambda p: count)
