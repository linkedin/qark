#!/bin/env python
import qark
import os.path

def test_run_automated():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.join(curr_dir, os.pardir)

    qark.runAutomated(os.path.join(curr_dir, 'testData/goatdroid.apk'),
                      os.path.join(parent_dir, 'testAutomated'),
                      os.path.join(parent_dir, 'testAutomated/log.txt'),
                      os.path.join(parent_dir, 'testAutomated'))
