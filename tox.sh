#!/usr/bin/sh
tox | tee tox-1.log ; tox | tee tox-2.log; tox | tee tox-3.log
