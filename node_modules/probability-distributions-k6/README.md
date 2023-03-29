# Probability Distributions Library for JavaScript
Functions for sampling random variables from probability distributions. Uses the same function names as R.

Adapted from https://github.com/Mattasher/probability-distributions in order to use its functions in https://k6.io/ scripts without any external dependencies.


## Installation

`npm install --save probability-distributions-k6`

`import PD from './node_modules/probability-distributions-k6/index.js';`

## Documentation and examples
**See <a href="http://statisticsblog.com/probability-distributions/">http://statisticsblog.com/probability-distributions/</a>**


## Currently supported

- Binomial distribution

- Beta distribution

- Cauchy distribution

- Chi-Squared distribution

- Exponential distribution

- F distribution

- Gamma distribution

- Laplace distribution

- Log Normal distribution

- Negative Binomial distribution

- Normal (Gaussian) distribution

- Poisson distribution (not recommended for lambda > 100)

- Sample (shuffle an array, or select items using optional array of weights)

- Uniform distribution (with entropy option for standard uniform)

- Uniform limited to whole numbers

- Words (generate random words from a library of characters)

- Visualization (show the values of a random variable in an animated loop)


## Warning

This package contains additional distributions marked as "experimental". Use these with extreme caution.


## License

MIT