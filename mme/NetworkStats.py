from scapy.all import *
from socket import htons
from scapy.fields import Field

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
	0x39a0: [
		ByteField("num_avlns", 0),
		FieldListField("nid", [0, 0, 0, 0, 0, 0, 0],
				ByteField("", 0),
				count_from = lambda p: 7),
		ByteField("snid", 0),
		ByteField("tei", 0),
		ByteField("sta_role", 0),
		MACField("cco_macaddr", "0:0:0:0:0:0"),
		ByteField("cco_tei", 0),
		FieldLenField("sta_info_count", None, count_of="sta_info"),
		FieldListField("sta_info", None,
				VendorStaInfoField("", None), 
				count_from = info_cnt),
		]
} 
