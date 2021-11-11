'use strict';

const express = require('express');
const sha512 = require('js-sha512');

const PORT = 8080;
const HOST = '0.0.0.0';

const app = express();

let dataStructure = [];

app.get('/ping', (req, res) => {
  let item = sha512(Date());
  console.log(item);
  dataStructure.push(item);
  console.log(dataStructure.length);
  res.send('pong');
});

process.on('SIGINT', function() {
    process.exit();
});

app.listen(PORT, HOST);
