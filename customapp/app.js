'use strict';

const express = require('express');
const inefficient = require('inefficient');

const PORT = 3000;
const HOST = '0.0.0.0';
const app = express();

app.get('/stress', inefficient);
app.listen(PORT, HOST);