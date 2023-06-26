<?php
ini_set('max_execution_time', '-1');
ini_set('memory_limit', '-1');
ignore_user_abort(true);
set_time_limit(0);

$sum = 0;
for ($i = 0; $i < 10000; $i++) {
   for ($j = 0; $j < 1000; $j++) {
     $sum++;
   } 
}

echo 'sum: ' . $sum;
