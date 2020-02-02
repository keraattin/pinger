#!/usr/bin/env python3

import subprocess

# Ping command
def ping(host,count=3):
    try:
        cmd_ping = subprocess.check_output(["ping",host,"-c",str(count)])
        return True
    except subprocess.CalledProcessError:
        return False

