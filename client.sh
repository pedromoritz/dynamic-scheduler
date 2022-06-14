#!/bin/bash
counter=1
while [ $counter -le $2 ]
do
  result=$(curl -s http://$1:31001/ping)
  if [[ "$result" == "pong" ]]; then
    echo "OK"
  else
    echo "===> NOK"
  fi
  counter=$(( $counter + 1 ))
  sleep 1
done