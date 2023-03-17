'use strict';

const express = require('express');
const sha512 = require('crypto-js/sha512');
const PORT = 3000;
const HOST = '0.0.0.0';
const app = express();

function showHeapUsage(step) {
  let memoryUsage = process.memoryUsage();
  let headUsed = `${Math.round(memoryUsage['heapUsed'] / 1024 / 1024 * 100) / 100}`;
  console.log(`Heap allocated ${step}: ${headUsed} MB\n`);
}

app.get('/do', (req, res) => {
  showHeapUsage('before');
  const array = Array.from({length: 10000000}, () => Math.random() * 10);
  //const arr = new Array(10000000).fill(1);
  showHeapUsage('after');
  res.send('done');
});

process.on('SIGINT', function() {
  process.exit();
});

app.listen(PORT, HOST);
