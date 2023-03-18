<?php 
$array = array();

foreach (range(0, 100000) as $number) {
	array_push($array, $number);
}

echo '<pre>'.print_r($array, 1).'</pre>';
?>