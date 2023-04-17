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
  const mu = (urls.length - 1) / 2;
  const sigma = mu / 3;
  let round_rnorm_output = -1;
  while (round_rnorm_output < 0 || round_rnorm_output > (urls.length - 1)) {
    round_rnorm_output = Math.round(PD.rnorm(1, mu, sigma));
  }
  http.get(url);
}
