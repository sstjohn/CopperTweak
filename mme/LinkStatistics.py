from scapy.all import *
from socket import htons

resp_is_tx = lambda p: p.direction = 0x00
resp_is_rx = lambda p: p.direction = 0x01
resp_is_both = lambda p: p.direction = 0x02

resp_has_txstats = lambda p: resp_is_tx(p) or resp_is_both(p)
resp_has_rxstats = lambda p: resp_is_rx(p) or resp_is_both(p)

mmtypes = {
        0x30a0: [
		ByteField("control", 0),
		ByteField("direction", 0),
		ByteField("link_id", 0),
                MACField("peer", "0:0:0:0:0:0"),
                ],
        0x31a0: [
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
		ConditionalField(ByteField("intervals", 0), resp_has_rxstats),
                ]
} 
