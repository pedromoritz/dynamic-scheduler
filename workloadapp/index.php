<?php 
$array = array();

foreach (range(0, 1000000) as $number) {
	array_push($array, $number);
}

echo '<pre>'.print_r($array, 1).'</pre>';
?>