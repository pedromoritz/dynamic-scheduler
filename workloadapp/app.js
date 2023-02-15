'use strict';

const express = require('express');
const PORT = 3000;
const HOST = '0.0.0.0';
const app = express();

const memoryLeakAllocations = [];
const allocationStep = 10000 * 1024;

function allocateMemory(size) {
  const numbers = size / 8;
  const arr = [];
  arr.length = numbers;
  for (let i = 0; i < numbers; i++) {
    arr[i] = i;
  }
  return arr;
}

function memoryPurge() {
  memoryLeakAllocations.length = 0;
  global.gc();
}

app.get('/memory/increase', (req, res) => {
  const allocation = allocateMemory(allocationStep);
  const memoryLeakAllocations = [];
  memoryLeakAllocations.push(allocation);
  const memoryUsage = process.memoryUsage();
  const gbNow = memoryUsage['heapUsed'] / 1024 / 1024 / 1024;
  const gbRounded = Math.round(gbNow * 100) / 100;
 
  setTimeout(function() {
    memoryLeakAllocations.length = 0;
    global.gc();
    res.send(`Heap allocated ${gbRounded} GB\n`);
  }, 5000);
});

app.get('/memory/purge', (req, res) => {
  memoryPurge();
  console.log('purge');
  res.send('purge\n');
});

process.on('SIGINT', function() {
  process.exit();
});

app.listen(PORT, HOST);
