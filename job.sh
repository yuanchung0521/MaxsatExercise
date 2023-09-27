#!/bin/sh
python pysat_lib.py
python pysat_try.py
./EvalMaxSAT_bin pysat_test.wcnf --old > 1.sol
python test_read_sol.py > 1.txt