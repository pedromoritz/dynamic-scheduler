'use strict';

const express = require('express');
const sha512 = require('crypto-js/sha512');
const Base64 = require('crypto-js/enc-base64');
const PORT = 3000;
const HOST = '0.0.0.0';
const app = express();

function getHeapUsage(step) {
  global.gc();
  let memoryUsage = process.memoryUsage();
  let headUsed = `${Math.round(memoryUsage['heapUsed'] / 1024 / 1024 * 100) / 100}`;
  console.log(`Heap allocated ${step}: ${headUsed} MB\n`);  
}

app.get('/do', (req, res) => {  
  getHeapUsage('initial');
  let array = [];

  for (let i = 0; i < 100000; i++) {
    array.push(
      sha512(
        (Date.now() + Math.random()).toString()
      ).toString()
    );
  }
  getHeapUsage('filled memory');

  while(array.length > 0) {
    array.pop();
  }
  getHeapUsage('after purge');

  res.send('done');
});

process.on('SIGINT', function() {
  process.exit();
});

app.listen(PORT, HOST);
