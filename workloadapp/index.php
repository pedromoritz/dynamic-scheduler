<?php
$array = array();
foreach (range(0, 10000) as $number) {
	array_push($array, bin2hex(random_bytes(20)));
}
?>