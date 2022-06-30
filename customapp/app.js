'use strict';

const express = require('express');
const sha512 = require('js-sha512');
const PORT = 8080;
const HOST = '0.0.0.0';
const app = express();
let dataStructure = [];

app.get('/memory/increase', (req, res) => {
  let item = randomString(100000);
  dataStructure.push(item);
  //console.log(item);
  //console.log('length: ' + dataStructure.length);
  const used = process.memoryUsage().heapUsed / 1024 / 1024;
  console.log(`The script uses approximately ${Math.round(used * 100) / 100} MB`);
  res.send('increase\n');
});

app.get('/memory/purge', (req, res) => {
  dataStructure.length = 0;
  global.gc();
  console.log('purge');
  res.send('purge\n');
});

app.get('/ping', (req, res) => {
  res.send('pong\n');
});

process.on('SIGINT', function() {
  process.exit();
});

function randomString(length = 50) {
  return [...Array(length + 10)].map((value) => (Math.random() * 1000000).toString(36).replace('.', '')).join('').substring(0, length);
};

app.listen(PORT, HOST);
