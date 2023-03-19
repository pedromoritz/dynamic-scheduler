import pkg from './pdf.js';
const { getNormallyDistributedRandomNumber } = pkg;

const mean = 30.0, stddev = 2.0;

const generatedNumbers = []
for (let i = 0; i < 100000; i += 1) {
    generatedNumbers.push(GetNormallyDistributedRandomNumber(mean, stddev))
}

console.log(generatedNumbers)