import os
import sys

from importlib import import_module
from scapy.all import *

from _internal_types import TypeConditionalField

known_mme = {}
mme_packet_types = {}


def register_mme():
	files = os.listdir(__file__.rsplit('/', 1)[0])

	for f in files:
		name = ""
		if f.startswith("_"):
			continue
		if f.endswith(".py") or f.endswith(".pyc"):
			name = f.rsplit(".",1)[0]
		else:
			continue
		if name in known_mme:
			continue

		known_mme[name] = import_module(__package__ + "." + name, globals())
		mme_packet_types.update(known_mme[name].mmtypes)

def GetMMEFields():
        yield ByteField("mmver", 0)
        yield XShortField("mmtype", 0)
        yield X3BytesField("OUI", 0x00b052)
        for t in mme_packet_types:
                for f in mme_packet_types[t]:
                        yield TypeConditionalField(t, f)

register_mme()

class MME(Packet):
        cnt_to_fl_len = lambda p: htons(p.carrier_cnt) / 2
        fields_desc = [f for f in GetMMEFields()]

bind_layers(Ether, MME, type=0x88e1)
