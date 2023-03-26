<?php
$array = array();
for ($i = 0; $i < 100000; $i++) {
   array_push($array, md5(microtime(true).mt_Rand()));
}
$used_mem = round(memory_get_usage(false) / 1024);      
echo $used_mem . 'KB';