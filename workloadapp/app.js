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
let array = [];
app.get('/do', (req, res) => {  
//  showHeapUsage('initial');

//  let array = [];

  for (let i = 0; i < 500000; i++) {
    array.push(sha512((Date.now() + Math.random()).toString()).toString());
  }

//  showHeapUsage('filled memory');

//  while(array.length > 0) {
//    array.pop();
//  }

//  showHeapUsage('after purge');
  res.send('done');
});

process.on('SIGINT', function() {
  process.exit();
});

app.listen(PORT, HOST);


// 'use strict';

// const express = require('express');
// const PORT = 3000;
// const HOST = '0.0.0.0';
// const app = express();

// const memoryLeakAllocations = [];
// const allocationStep = 10000 * 1024;

// function allocateMemory(size) {
//   const numbers = size / 8;
//   const arr = [];
//   arr.length = numbers;
//   for (let i = 0; i < numbers; i++) {
//     arr[i] = i;
//   }
//   return arr;
// }

// function memoryPurge() {
//   memoryLeakAllocations.length = 0;
//   global.gc();
// }

// app.get('/do', (req, res) => {
//   const allocation = allocateMemory(allocationStep);
//   const memoryLeakAllocations = [];
//   memoryLeakAllocations.push(allocation);
//   const memoryUsage = process.memoryUsage();
//   const gbNow = memoryUsage['heapUsed'] / 1024 / 1024 / 1024;
//   const gbRounded = Math.round(gbNow * 100) / 100;
 
//   console.log(`1 -> Heap allocated ${gbRounded} GB\n`);
//   setTimeout(function() {
//     memoryLeakAllocations.length = 0;
//     global.gc();
//     console.log(`Deallocating memory...`);
//     res.send(`Heap allocated ${gbRounded} GB\n`);
//   }, 10000);
//   // console.log(`The script uses approximately ${Math.round(used * 100) / 100} MB`);
// });

// process.on('SIGINT', function() {
//   process.exit();
// });

// app.listen(PORT, HOST);
