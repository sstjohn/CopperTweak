from scapy.all import *
from socket import htons

HPAV_IFACE = "eth0"
DEST_MAC = "00:b0:52:00:00:01"
#PEER_MAC = "cc:5d:4e:96:54:29"
#PEER_MAC = "b0:b2:dc:61:7d:cc"
PEER_MAC = "cc:5d:4e:96:1c:7f"

class MME(Packet):
	is_tm_req = lambda p: p.mmtype == 0x70a0
	is_tm_resp = lambda p: p.mmtype == 0x71a0
	fields_desc = [ ByteField("mmver", 0),
			XShortField("mmtype", 0),
			X3BytesField("OIU", 0x00b052),
			ConditionalField(
				MACField("peer", PEER_MAC),
				is_tm_req),
			ConditionalField(
				PadField(ByteField("slot", 0), 34),
				is_tm_req),
			ConditionalField(
				ByteField("mstatus", 0),
				is_tm_resp),
			ConditionalField(
				ByteField("tmslot", 0),
				is_tm_resp),
			ConditionalField(
				ByteField("num_tms", 0),
				is_tm_resp),
			ConditionalField(
				XShortField("carrier_cnt", 0),
				is_tm_resp),
			ConditionalField(
				FieldListField("carriers", [0],
						XByteField("", 0),
						count_from = lambda p: 
							htons(p.carrier_cnt) / 2),
				is_tm_resp) ]

if __name__ == "__main__":
	bind_layers(Ether, MME, type=0x88e1)
	req = Ether(dst = DEST_MAC, type=0x88e1) 
	req /= MME(mmtype = 0x70a0)
	resp = srp1(req, iface = HPAV_IFACE, timeout=1)
	score = 0
	for c in resp[MME].carriers:
		high = (0xF0 & c) >> 4
		low = 0xF & c
		score += (high + low)
	print "Overall tone map score is %i" % score

