import http from 'k6/http';
import { reportHTML } from "https://raw.githubusercontent.com/fziviello/k6-report-html/main/dist/reportHtml.min.js";
import PD from './node_modules/probability-distributions-k6/index.js';

export const options = {
  scenarios: {
    constant_request_rate: {
      executor: 'constant-arrival-rate',
      rate: parseInt(__ENV.VIRTUAL_USERS),
      timeUnit: '1s',
      duration: '30m',
      preAllocatedVUs: 100,
      maxVUs: 500,
    },
  },
};

const API_BASE_URL = `http://${__ENV.SVC_IP}`

const urls = []

for (let i = 0; i < parseInt(__ENV.POD_AMOUNT); i++) {
  urls.push(`${API_BASE_URL}:31${String(i+1).padStart(3, '0')}`)
}

export function handleSummary(data) {
  return {
    [`results/summary_${__ENV.SCHEDULER_TYPE}_${__ENV.POD_AMOUNT}_${__ENV.VIRTUAL_USERS}.html`]: reportHTML(data, {title:`${__ENV.SCHEDULER_TYPE} - ${__ENV.POD_AMOUNT} pods - ${__ENV.VIRTUAL_USERS} maximum virtual users`})
  };
}

export default function () {
  const pods = urls.length;

  // exponential distribution
  const rate = 5 / pods;
  let round_rexp_output = pods;
  while (round_rexp_output > (pods - 1)) {
    round_rexp_output = Math.round(PD.rexp(1, rate));
  }
  const url = urls[round_rexp_output];
  /*
  // normal distribution
  const mu = (pods - 1) / 2;
  const sigma = mu / 5;
  let round_rnorm_output = -1;
  while (round_rnorm_output < 0 || round_rnorm_output > (pods - 1)) {
    round_rnorm_output = Math.round(PD.rnorm(1, mu, sigma));
  }
  const url = urls[round_rnorm_output];
  */  
  http.get(url);
}
