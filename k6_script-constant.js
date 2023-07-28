import http from 'k6/http';
import { reportHTML } from "https://raw.githubusercontent.com/fziviello/k6-report-html/main/dist/reportHtml.min.js";
import PD from './node_modules/probability-distributions-k6/index.js';

export const options = {
  scenarios: {
    constant_request_rate: {
      executor: 'constant-arrival-rate',
      rate: parseInt(__ENV.TA),
      timeUnit: '1s',
      duration: '12m',
      preAllocatedVUs: 100,
      maxVUs: 500,
    },
  },
};

const API_BASE_URL = `http://${__ENV.IP}`

const urls = []

for (let i = 0; i < parseInt(__ENV.PA); i++) {
  urls.push(`${API_BASE_URL}:31${String(i+1).padStart(3, '0')}`)
}

let summaryKey = `results/summary_${__ENV.ST}_${__ENV.PA}_${__ENV.TA}_${__ENV.RT}_${__ENV.DI}_${__ENV.ME}.html`;
let summaryValue = `${__ENV.ST} - ${__ENV.PA} pods - ${__ENV.TA} requests per second with ${__ENV.DI} distribution (${__ENV.ME} as metric)`;

export function handleSummary(data) {
  return {
    [summaryKey]: reportHTML(data, {title: summaryValue})
  };
}

export default function () {
  const pods = urls.length;

  let distribution_output = -1;
  while (distribution_output < 1 || distribution_output > pods) {
    switch (__ENV.DI) {
      case 'exponential':
        distribution_output = Math.round(PD.rexp(1, 5 / pods)); // exponential distribution
        break;
      case 'normal':
        distribution_output = Math.round(PD.rnorm(1, (pods + 1) / 2, ((pods + 1) / 2) / 6)); // normal distribution
        break;
    }
  }

  const url = urls[distribution_output - 1];
  http.get(url);
}
