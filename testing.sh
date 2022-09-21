#!/bin/bash
reset

gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 -c 10 http://192.168.59.122:31001/memory/increase" 
sleep 10
gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 -c 10 http://192.168.59.122:31002/memory/increase" 
sleep 10
gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 -c 10 http://192.168.59.122:31003/memory/increase"
sleep 10
gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 -c 10 http://192.168.59.122:31004/memory/increase"
sleep 10
gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 -c 10 http://192.168.59.122:31005/memory/increase"
sleep 10
gnome-terminal --geometry=58x10+830+270 -- bash -c "hey -n 1000 -c 10 http://192.168.59.122:31006/memory/increase"

