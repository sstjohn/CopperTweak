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
	cnt_to_fl_len = lambda p: htons(p.carrier_cnt) / 2	
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
						count_from = cnt_to_fl_len),
				is_tm_resp) ]

def score_carrier(value):
	try:
		return [0, 2, 4, 8, 16, 64, 256, 1024, 4096][value]
	except:
		raise Exception("unknown carrier value %i" % value)

def get_tm_score(interface, dest_mac, peer_mac):
	bind_layers(Ether, MME, type=0x88e1)
	req = Ether(dst = dest_mac, peer = peer_mac, type=0x88e1) 
	req /= MME(mmtype = 0x70a0)
	last_res = 0
	score = 0
	while last_res == 0:
		resp = srp1(req, iface = interface, timeout=1, 
				filter="ether proto 0x88e1", verbose = 0)
		last_res = resp[MME].mstatus
		if last_res == 0:
			for c in resp[MME].carriers:
				score += score_carrier((0xF0 & c) >> 4)
				score += score_carrier(0xF & c)
		req[MME].slot += 1
	return score

if __name__ == "__main__":
	score = get_tm_score(HPAV_IFACE, DEST_MAC, PEER_MAC)
	print "Overall tone map score is %i" % score

