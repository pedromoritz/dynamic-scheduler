'use strict';

const express = require('express');
const sha512 = require('crypto-js/sha512');
const PORT = 3000;
const HOST = '0.0.0.0';
const app = express();

let array = [];

app.get('/do', (req, res) => {
  for (let i = 0; i < 200000; i++) {
    array.push(sha512(Math.random().toString()).toString());
  }

  res.send('done');
});

process.on('SIGINT', function() {
  process.exit();
});

app.listen(PORT, HOST);
