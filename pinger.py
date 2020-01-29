#!/usr/bin/env python3

import subprocess

def ping(host):
    count = 3

    # Ping
    try:
        cmd_ping = subprocess.check_output(["ping",host,"-c",str(count)])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    ping("")

if __name__ == "__main__":
    main()