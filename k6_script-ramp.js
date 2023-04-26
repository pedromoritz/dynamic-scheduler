import http from 'k6/http';
import { reportHTML } from "https://raw.githubusercontent.com/fziviello/k6-report-html/main/dist/reportHtml.min.js";
import PD from './node_modules/probability-distributions-k6/index.js';
import { sleep } from 'k6';

export const options = {
  discardResponseBodies: true,
  scenarios: {
    contacts: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30m', target: parseInt(__ENV.VIRTUAL_USERS)},
      ],
      gracefulRampDown: '0s',
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

  let distribution_output = -1;
  while (distribution_output < 1 || distribution_output > pods) {
    distribution_output = Math.round(PD.rexp(1, 5 / pods)); // exponential distribution
//  distribution_output = Math.round(PD.rnorm(1, (pods + 1) / 2, ((pods + 1) / 2) / 5)); // normal distribution
  }

  const url = urls[distribution_output];
  http.get(url);
  sleep(0.5);
}
