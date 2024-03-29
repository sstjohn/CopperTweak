## This file is part of CopperTweak
## Copyright (C) 2012 Saul St. John <saul.stjohn@gmail.com>
## This program is published under a GPLv2 license

from scapy.all import *
from socket import htons

mmtypes = {
        0x70a0: [
                MACField("peer", "0:0:0:0:0:0"),
                PadField(ByteField("slot", 0), 34)
                ],
        0x71a0: [
                ByteField("tmstatus", 0),
                ByteField("tmslot", 0),
                ByteField("num_tms", 0),
                XShortField("carrier_cnt", 0),
                FieldListField("carriers", [0],
                        XByteField("", 0),
                        count_from = lambda p: htons(p.carrier_cnt) / 2)
                ]
} 
