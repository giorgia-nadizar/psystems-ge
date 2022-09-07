#!/bin/bash

workon psystems

python3 experiments.py send-in 2 30 conf.json send-in-2 &
python3 experiments.py send-in 3 30 conf.json send-in-3 &
python3 experiments.py send-in 4 30 conf.json send-in-4 &
python3 experiments.py send-in 5 30 conf.json send-in-5 &

python3 experiments.py send-out 2 30 conf.json send-out-2 &
python3 experiments.py send-out 3 30 conf.json send-out-3 &
python3 experiments.py send-out 4 30 conf.json send-out-4 &
python3 experiments.py send-out 5 30 conf.json send-out-5 &

python3 experiments.py assignment 2 30 conf.json assignment-2 &
python3 experiments.py assignment 3 30 conf.json assignment-3 &
python3 experiments.py assignment 4 30 conf.json assignment-4 &
python3 experiments.py assignment 5 30 conf.json assignment-5 &

python3 experiments.py tm 2 30 conf-cooperative.json tm-2 &
python3 experiments.py tm 3 30 conf-cooperative.json tm-3 &
python3 experiments.py tm 4 30 conf-cooperative.json tm-4 &
python3 experiments.py tm 5 30 conf-cooperative.json tm-5 &
