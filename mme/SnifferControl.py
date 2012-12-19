## This file is part of CopperTweak
## Copyright (C) 2012 Saul St. John <saul.stjohn@gmail.com>
## This program is published under a GPLv2 license

from scapy.all import *
from socket import htons

mmtypes = {
	#sniff request
        0x34a0: [
		ByteField("control", 0),
                PadField(ByteField("reserved", 0), 4),
                ],
	#sniff request confirmation
        0x35a0: [
		ByteField("mstatus", 0),
		ByteField("state", 0),
		PadField(ByteField("da", 0), 6),
                ],
	#sniff indicate
	0x36a0: [
		ByteField("type", 0),
		ByteField("direction", 0),
		LongField("systime", 0),
		IntField("beacontime", 0),
		#...followed by an frame-control field as yet undissected
		]
} 
