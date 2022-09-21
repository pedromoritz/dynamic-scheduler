#!/bin/bash
reset

gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 http://192.168.59.121:31001/memory/increase" 
sleep 10
gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 http://192.168.59.121:31002/memory/increase" 
sleep 10
gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 http://192.168.59.121:31003/memory/increase"
sleep 10
gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 http://192.168.59.121:31004/memory/increase"
sleep 10
gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 http://192.168.59.121:31005/memory/increase"
sleep 10
gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 http://192.168.59.121:31006/memory/increase"
sleep 10

./monitoring.py