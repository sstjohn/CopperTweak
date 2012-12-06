from scapy.all import *
from mme import MME

HPAV_IFACE = "eth0"
DEST_MAC = "00:b0:52:00:00:01"
#PEER_MAC = "cc:5d:4e:96:54:29"
#PEER_MAC = "b0:b2:dc:61:7d:cc"
PEER_MAC = "cc:5d:4e:96:1c:7f"

def score_carrier(value):
	try:
		return [0, 2, 4, 8, 16, 64, 256, 1024, 4096][value]
	except:
		raise Exception("unknown carrier value %i" % value)

class TestException(Exception):
	pass

def get_tmi_score(index, interface, dest_mac, peer_mac):
	req = Ether(dst = dest_mac, type=0x88e1) 
	req /= MME(mmtype = 0x70a0, peer = peer_mac)
	req[MME].slot = index 
	resp = srp1(req, iface = interface, timeout=1, 
			filter="ether proto 0x88e1", verbose = 0)
	if resp[MME].mstatus != 0:
		return -1
	score = 0
	for c in resp[MME].carriers:
		score += score_carrier((0xF0 & c) >> 4)
		score += score_carrier(0xF & c)
	return score / (2 * len(resp[MME].carriers))

def get_tm_score(interface, dest_mac, peer_mac):
	index = 0
	scores_sum = 0
	last_score = 0
	while last_score != -1:
		scores_sum += last_score
		last_score = get_tmi_score(index, interface, 
					dest_mac, peer_mac)
		index += 1
	if index > 1:
		return scores_sum / (index - 1)
	return 0

def get_def_tmi_score(index):
	return get_tmi_score(index, HPAV_IFACE, DEST_MAC, PEER_MAC)

def get_def_tm_score():
	return get_tm_score(HPAV_IFACE, DEST_MAC, PEER_MAC)

if __name__ == "__main__":
	print "Overall tone map score is %i" % get_def_tm_score()

