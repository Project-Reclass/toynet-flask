#!/usr/bin/env bash
service openvswitch-switch start
ovs-vsctl set-manager ptcp:6640
pytest -v --ignore tests/test_orchestration.py $1
