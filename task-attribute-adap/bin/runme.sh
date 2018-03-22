#!/bin/bash

export RADICAL_PILOT_DBURL="mongodb://entk:entk@ds125126.mlab.com:25126/adbms-1"
export RADICAL_ENTK_PROFILE=True
export RADICAL_PILOT_PROFILE=True
export RADICAL_ENTK_VERBOSE=INFO
export RP_ENABLE_OLD_DEFINES=True

stages="32 64"
for s in $stages; do
    mkdir dur-60-attr-$s
    python task_attr_adap.py 60 $s
    mv *.prof rp.session.* dur-60-attr-$s/
done
