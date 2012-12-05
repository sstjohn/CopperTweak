from scapy.all import *
from socket import htons

HPAV_IFACE = "eth0"
DEST_MAC = "00:b0:52:00:00:01"
#PEER_MAC = "cc:5d:4e:96:54:29"
#PEER_MAC = "b0:b2:dc:61:7d:cc"
PEER_MAC = "cc:5d:4e:96:1c:7f"

mme_packet_types = {
	0x70a0: [
		MACField("peer", PEER_MAC),
		PadField(ByteField("slot", 0), 34)
		],
	0x71a0: [
		ByteField("mstatus", 0),
		ByteField("tmslot", 0),
		ByteField("num_tms", 0),
		XShortField("carrier_cnt", 0),
		FieldListField("carriers", [0],
			XByteField("", 0),
			count_from = lambda p: htons(p.carrier_cnt) / 2)
		]
}

def TypeConditionalField(t, f):
	cond = lambda p: p.mmtype == t
	return ConditionalField(f, cond)

def GetMMEFields():
	yield ByteField("mmver", 0)
	yield XShortField("mmtype", 0)
	yield X3BytesField("OUI", 0x00b052)
	for t in mme_packet_types:
		for f in mme_packet_types[t]:
			yield TypeConditionalField(t, f)

class MME(Packet):
	cnt_to_fl_len = lambda p: htons(p.carrier_cnt) / 2	
	fields_desc = [f for f in GetMMEFields()]

bind_layers(Ether, MME, type=0x88e1)

def score_carrier(value):
	try:
		return [0, 2, 4, 8, 16, 64, 256, 1024, 4096][value]
	except:
		raise Exception("unknown carrier value %i" % value)

def get_tmi_score(index, interface, dest_mac, peer_mac):
	req = Ether(dst = dest_mac, type=0x88e1) 
	req /= MME(mmtype = 0x70a0, peer = peer_mac)
	req[MME].slot = index 
	resp = srp1(req, iface = interface, timeout=1, 
			filter="ether proto 0x88e1", verbose = 0)
	if resp[MME].mstatus != 0:
		raise Exception("response status %i" % resp[MME].mstatus)
	score = 0
	for c in resp[MME].carriers:
		score += score_carrier((0xF0 & c) >> 4)
		score += score_carrier(0xF & c)
	return score / (2 * len(resp[MME].carriers))

def get_tm_score(interface, dest_mac, peer_mac):
	index = 0
	scores_sum = 0
	try:
		while True:
			scores_sum += get_tmi_score(index, interface, 
						dest_mac, peer_mac)
			index += 1
	except:
		pass
	if index != 0:
		return scores_sum / index
	return 0

def get_def_tmi_score(index):
	return get_tmi_score(index, HPAV_IFACE, DEST_MAC, PEER_MAC)

def get_def_tm_score():
	return get_tm_score(HPAV_IFACE, DEST_MAC, PEER_MAC)

if __name__ == "__main__":
	print "Overall tone map score is %i" % get_def_tm_score()

