#!/usr/bin/env python
import commands
import zmq
from datetime import datetime

disk_use = commands.getoutput("df -m /mnt/data |grep -v Filesystem |awk '{print $3}'")

socket = zmq.Context().socket(zmq.PUSH)
socket.connect("tcp://expcont:6668")

msg = {}

msg["service"] = "diskmon-fpmaster"
msg["prio"] = 2
msg["time"] = str(datetime.utcnow())
msg["varname"] = "disk-used-mnt-data"
msg["value"] = disk_use
socket.send_json(msg) 
