#!/usr/bin/python3
from datetime import datetime
import os
from os import path
import subprocess

import pexpect


log_dir = path.abspath("toxlogs")

typecheckers = {
    "BEAR": "beartype",
    "GUARD": "guardtype",
    "NONE": "nonetype"
}

first = True

for i in range(1, 4):
    for checker, checker_name in typecheckers.items():

        logfile_path = path.join(log_dir, f"tox-{checker_name}-{i}.log")

        if not first:
            print()
            print()
        first = False
        print(f"$ TYPECHECKER={checker} tox (run {i}) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        env = os.environ.copy()
        env["TYPECHECKER"] = checker
        with open(logfile_path, "w") as logfile:
            # use ansi2txt unix program to remove ansi escape characters
            ansi2txt = subprocess.Popen(
                ['ansi2txt'],
                stdin=subprocess.PIPE,
                stdout=logfile,
                stderr=subprocess.PIPE,
                text=True
            )
            tox = pexpect.spawn("tox",
                                env=env)
            while True:
                match = tox.expect([pexpect.EOF, '\r\n'], timeout=None)
                line = tox.before.decode('utf-8')
                print(line, flush=True)
                print(line, flush=True, file=ansi2txt.stdin)
                if match == 0:
                    break
            ansi2txt.communicate()
