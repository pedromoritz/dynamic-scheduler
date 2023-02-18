'use strict';

const express = require('express');
const sha512 = require('crypto-js/sha512');
const PORT = 3000;
const HOST = '0.0.0.0';
const app = express();

function showHeapUsage(step) {
  global.gc();
  let memoryUsage = process.memoryUsage();
  let headUsed = `${Math.round(memoryUsage['heapUsed'] / 1024 / 1024 * 100) / 100}`;
  console.log(`Heap allocated ${step}: ${headUsed} MB\n`);  
}

app.get('/do', (req, res) => {  
  showHeapUsage('initial');
  let array = [];

  for (let i = 0; i < 50000; i++) {
    array.push(
      sha512(
        (Date.now() + Math.random()).toString()
      ).toString()
    );
  }

  showHeapUsage('filled memory');

  while(array.length > 0) {
    array.pop();
  }

  showHeapUsage('after purge');
  res.send('done');
});

process.on('SIGINT', function() {
  process.exit();
});

app.listen(PORT, HOST);
