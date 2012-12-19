## This file is part of CopperTweak
## Copyright (C) 2012 Saul St. John <saul.stjohn@gmail.com>
## This program is published under a GPLv2 license

from scapy.all import *
from socket import htons
from scapy.fields import Field
from _internal_types import *

#structure:
# sta_macaddr[6]
# sta_tei
# bridge_macaddr[6]
# avg_phy_tx_rate
# avg_phy_rx_rate

class VendorStaInfoField(Field):
	def __init__(self, name, default):
		Field.__init__(self, name, None, "15B")

		# macaddress
		# byte: avg_phy_dr_tx
		# byte: avg_phy_dr_rx
class StaInfoField(Field):
	def __init__(self, name, default):
		Field.__init__(self, name, None, "8B")

info_cnt = lambda p: p.sta_info_count

def gen_network_info_confirm():
	fixed_fields = [
                ByteField("num_avlns", 0),
                ArrayField("nid", 0, ByteField("", 0), 7),
                ByteField("snid", 0),
                ByteField("tei", 0),
                ByteField("sta_role", 0),
                MACField("cco_macaddr", "0:0:0:0:0:0"),
                ByteField("cco_tei", 0),
                ByteField("sta_info_count", 0)]
	for f in fixed_fields:
		yield f
	for i in range(1, 255):
		has_field = lambda p: p.sta_info_count >= i
		yield ConditionalField(MACField(
			"sta_macaddr_%s" % i, "0:0:0:0:0:0"),
			has_field)
		yield ConditionalField(ByteField(
			"sta_tei_%s" % i, 0),
			has_field)
		yield ConditionalField(MACField(
			"bridge_macaddr_%s" % i, "0:0:0:0:0:0"),
			has_field)
		yield ConditionalField(ByteField(
			"avg_phy_tx_rate_%s" % i, 0),
			has_field)
		yield ConditionalField(ByteField(
			"avg_phy_rx_rate_%s" % i, 0),
			has_field)



mmtypes = {
        0x4860: [
                ],
        0x4960: [
		FieldLenField("sta_info_count", None, count_of="sta_info"),
		FieldListField("sta_info", None, 
				StaInfoField("", None),
				count_from = info_cnt)
                ],
	0x38a0: [
		],
	0x39a0: [f for f in gen_network_info_confirm()]
} 
