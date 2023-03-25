import http from 'k6/http';
import { reportHTML } from "https://raw.githubusercontent.com/fziviello/k6-report-html/main/dist/reportHtml.min.js";
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';
import { getNormallyDistributedRandomNumber } from './pdf.js';

export const options = {
  scenarios: {
    constant_request_rate: {
      executor: 'constant-arrival-rate',
      rate: __ENV.REQUESTS_RATE,
      timeUnit: '1s',
      duration: '10m',
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
    [`results/summary_${__ENV.SCHEDULER_TYPE}_${__ENV.POD_AMOUNT}_${__ENV.REQUESTS_RATE}.html`]: reportHTML(data, {title:`${__ENV.SCHEDULER_TYPE} - ${__ENV.POD_AMOUNT} pods - ${__ENV.REQUESTS_RATE} requests/second`})
  };
}

export default function () {
  const url = urls[getNormallyDistributedRandomNumber(urls.length)]
  http.get(url)
}

