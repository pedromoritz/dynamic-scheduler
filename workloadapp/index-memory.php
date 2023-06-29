<?php
ini_set('max_execution_time', '-1');
ini_set('memory_limit', '-1');
ignore_user_abort(true);
set_time_limit(0);

$array = array();
for ($i = 0; $i < 100000; $i++) {
   array_push($array, md5(microtime(true).mt_Rand())+microtime(time));
}

$used_mem = round(memory_get_usage(false) / 1024);
$alloc_mem = round(memory_get_usage(true) / 1024);
echo 'used: ' . $used_mem . 'KB, allocated: ' . $alloc_mem . 'KB';
