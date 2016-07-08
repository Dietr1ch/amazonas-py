#!/bin/zsh
./judge.py --p1 0 --p2 1 $@ > /dev/null &
./judge.py --p1 0 --p2 2 $@ > /dev/null &
./judge.py --p1 0 --p2 3 $@ > /dev/null &
./judge.py --p1 0 --p2 4 $@ > /dev/null &
./judge.py --p1 0 --p2 5 $@ > /dev/null &
./judge.py --p1 0 --p2 6 $@ > /dev/null &
./judge.py --p1 0 --p2 7 $@ > /dev/null &
./judge.py --p1 0 --p2 8 $@ > /dev/null &

./judge.py --p1 1 --p2 2 $@ > /dev/null &
./judge.py --p1 1 --p2 3 $@ > /dev/null &
./judge.py --p1 1 --p2 4 $@ > /dev/null &
./judge.py --p1 1 --p2 5 $@ > /dev/null &
./judge.py --p1 1 --p2 6 $@ > /dev/null &
./judge.py --p1 1 --p2 7 $@ > /dev/null &
./judge.py --p1 1 --p2 8 $@ > /dev/null &

./judge.py --p1 2 --p2 3 $@ > /dev/null &
./judge.py --p1 2 --p2 4 $@ > /dev/null &
./judge.py --p1 2 --p2 5 $@ > /dev/null &
./judge.py --p1 2 --p2 6 $@ > /dev/null &
./judge.py --p1 2 --p2 7 $@ > /dev/null &
./judge.py --p1 2 --p2 8 $@ > /dev/null &

./judge.py --p1 3 --p2 4 $@ > /dev/null &
./judge.py --p1 3 --p2 5 $@ > /dev/null &
./judge.py --p1 3 --p2 6 $@ > /dev/null &
./judge.py --p1 3 --p2 7 $@ > /dev/null &
./judge.py --p1 3 --p2 8 $@ > /dev/null &

./judge.py --p1 4 --p2 5 $@ > /dev/null &
./judge.py --p1 4 --p2 6 $@ > /dev/null &
./judge.py --p1 4 --p2 7 $@ > /dev/null &
./judge.py --p1 4 --p2 8 $@ > /dev/null &

./judge.py --p1 5 --p2 6 $@ > /dev/null &
./judge.py --p1 5 --p2 7 $@ > /dev/null &
./judge.py --p1 5 --p2 8 $@ > /dev/null &

./judge.py --p1 6 --p2 7 $@ > /dev/null &
./judge.py --p1 6 --p2 8 $@ > /dev/null &

./judge.py --p1 7 --p2 8 $@ > /dev/null &
