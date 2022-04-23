'use strict';

const express = require('express');
const sha512 = require('js-sha512');

const PORT = 8080;
const HOST = '0.0.0.0';

const app = express();

let dataStructure = [];

app.get('/ping', (req, res) => {
  let item = 'object=>' +
    sha512(Math.random().toString()) +
    sha512(Math.random().toString()) +
    sha512(Math.random().toString()) +
    sha512(Math.random().toString()) +
    sha512(Math.random().toString()) +
    sha512(Math.random().toString()) +
    sha512(Math.random().toString()) +
    sha512(Math.random().toString()) +
    sha512(Math.random().toString()) +
    sha512(Math.random().toString());
  dataStructure.push(item);
  console.log(item);
  console.log(dataStructure.length);
  res.send('pong');
});

app.get('/purge', (req, res) => {
  dataStructure.length = 0;
  global.gc();
  console.log('purge');
  res.send('purge');
});

process.on('SIGINT', function() {
    process.exit();
});

app.listen(PORT, HOST);
