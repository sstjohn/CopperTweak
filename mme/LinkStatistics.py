from scapy.all import *
from socket import htons

resp_is_tx = lambda p: p.direction == 0x00
resp_is_rx = lambda p: p.direction == 0x01
resp_is_both = lambda p: p.direction == 0x02

resp_has_txstats = lambda p: resp_is_tx(p) or resp_is_both(p)
resp_has_rxstats = lambda p: resp_is_rx(p) or resp_is_both(p)

def rxresp_has_interval(i):
	return lambda p: p.rx_intervals >= i

def gen_interval_field(i, name, ftype):
	return ConditionalField(ConditionalField(
		ftype("%s_%s" % (name, i), 0),
		rxresp_has_interval(i)),
		resp_has_rxstats)

def gen_stats_resp():
	fixed_fields = [
		ByteField("mstatus", 0),
                ByteField("direction", 0),
                ByteField("link_id", 0),
                ByteField("tei", 0),
                ConditionalField(LELongField("tx_mpdu_ack", 0), resp_has_txstats),
                ConditionalField(LELongField("tx_mpdu_coll", 0), resp_has_txstats),
                ConditionalField(LELongField("tx_mpdu_fail", 0), resp_has_txstats),
                ConditionalField(LELongField("tx_pb_passed", 0), resp_has_txstats),
                ConditionalField(LELongField("tx_pb_failed", 0), resp_has_txstats),
                ConditionalField(LELongField("rx_mpdu_ack", 0), resp_has_rxstats),
                ConditionalField(LELongField("rx_mpdu_fail", 0), resp_has_rxstats),
                ConditionalField(LELongField("rx_pb_passed", 0), resp_has_rxstats),
                ConditionalField(LELongField("rx_pb_failed", 0), resp_has_rxstats),
                ConditionalField(LELongField("rx_tbe_passed", 0), resp_has_rxstats),
                ConditionalField(LELongField("rx_tbe_failed", 0), resp_has_rxstats),
                ConditionalField(ByteField("rx_intervals", 0), resp_has_rxstats)]
	for f in fixed_fields:
		yield f
	for i in range(1, 255):
		yield gen_interval_field(i, "phyrate", ByteField)
		yield gen_interval_field(i, "pb_passed", LELongField)
		yield gen_interval_field(i, "pb_failed", LELongField)
		yield gen_interval_field(i, "tbe_passed", LELongField)
		yield gen_interval_field(i, "tbe_failed", LELongField)

mmtypes = {
        0x30a0: [
		ByteField("control", 0),
		ByteField("direction", 0),
		ByteField("link_id", 0),
                PadField(MACField("peer", "0:0:0:0:0:0"), 37),
                ],
        0x31a0: [f for f in gen_stats_resp()]
} 
