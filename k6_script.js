const PD = require('./node_modules/probability-distributions-k6/index.js');

for (let i = 0; i < 24000; i++) {
  let pods = 20;
  let distribution_output = -1;
  while (distribution_output < 1 || distribution_output > pods) {
    //distribution_output = Math.round(PD.rexp(1, 5 / pods)); // exponential distribution
    distribution_output = Math.round(PD.rnorm(1, ((pods + 1) / 2) * 1.50, ((pods + 1) / 2) / 4)); // normal distribution
  }
  console.log(distribution_output - 1)
}
