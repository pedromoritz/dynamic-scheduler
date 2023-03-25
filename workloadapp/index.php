<?php
$array = array();
foreach (range(0, 50000) as $number) {
	array_push($array, bin2hex(random_bytes(20)));
}
?>