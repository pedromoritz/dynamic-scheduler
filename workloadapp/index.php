<?php
ini_set('memory_limit', '2048M');

$array = array();

foreach (range(0, 200000) as $number) {
	array_push($array, $number);
}

echo '<pre>'.count($array).'</pre>';
?>