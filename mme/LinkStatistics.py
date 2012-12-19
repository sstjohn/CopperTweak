from scapy.all import *
from socket import htons

resp_is_tx = lambda p: p.direction == 0x00
resp_is_rx = lambda p: p.direction == 0x01
resp_is_both = lambda p: p.direction == 0x02

resp_has_txstats = lambda p: resp_is_tx(p) or resp_is_both(p)
resp_has_rxstats = lambda p: resp_is_rx(p) or resp_is_both(p)

def rxresp_has_interval(i):
	return lambda p: p.intervals >= i

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
                ConditionalField(LongField("mpdu_ack", 0), resp_has_txstats),
                ConditionalField(LongField("mpdu_coll", 0), resp_has_txstats),
                ConditionalField(LongField("mpdu_fail", 0), resp_has_txstats),
                ConditionalField(LongField("pb_passed", 0), resp_has_txstats),
                ConditionalField(LongField("pb_failed", 0), resp_has_txstats),
                ConditionalField(LongField("mpdu_ack", 0), resp_has_rxstats),
                ConditionalField(LongField("mpdu_fail", 0), resp_has_rxstats),
                ConditionalField(LongField("pb_passed", 0), resp_has_rxstats),
                ConditionalField(LongField("pb_failed", 0), resp_has_rxstats),
                ConditionalField(LongField("tbe_passed", 0), resp_has_rxstats),
                ConditionalField(LongField("tbe_failed", 0), resp_has_rxstats),
                ConditionalField(ByteField("intervals", 0), resp_has_rxstats)]
	for f in fixed_fields:
		yield f
	for i in range(1, 255):
		yield gen_interval_field(i, "phyrate", ByteField)
		yield gen_interval_field(i, "pb_passed", LongField)
		yield gen_interval_field(i, "pb_failed", LongField)
		yield gen_interval_field(i, "tbe_passed", LongField)
		yield gen_interval_field(i, "tbe_failed", LongField)

mmtypes = {
        0x30a0: [
		ByteField("control", 0),
		ByteField("direction", 0),
		ByteField("link_id", 0),
                MACField("peer", "0:0:0:0:0:0"),
                ],
        0x31a0: [f for f in gen_stats_resp()]
} 
