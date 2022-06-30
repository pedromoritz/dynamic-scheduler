#!/bin/bash
reset

gnome-terminal --geometry=80x10+50+270 -- bash -c "./dynamic-scheduler.py" 
gnome-terminal --geometry=140x10+50+0 -- bash -c "watch -n 1 kubectl get pods --namespace lab1 -o wide" 
gnome-terminal --geometry=58x10+830+270 -- bash -c "watch -n 1 kubectl top node --namespace lab1"
