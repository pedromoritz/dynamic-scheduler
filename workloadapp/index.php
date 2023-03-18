<?php
ini_set('memory_limit', '1024M');

$array = array();

foreach (range(0, 100000) as $number) {
	array_push($array, $number);
}

echo '<pre>'.count($array).'</pre>';
?>