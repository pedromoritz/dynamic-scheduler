import http from 'k6/http';
import { sleep } from 'k6';
import { reportHTML } from "https://raw.githubusercontent.com/fziviello/k6-report-html/main/dist/reportHtml.min.js";
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';
import { getNormallyDistributedRandomNumber } from './pdf.js';

export const options = {
  stages: [
    { duration: '30m', target: parseInt(__ENV.VIRTUAL_USERS)},
  ],
};

const API_BASE_URL = `http://${__ENV.SVC_IP}`

const urls = []

for (let i = 0; i < parseInt(__ENV.POD_AMOUNT); i++) {
  urls.push(`${API_BASE_URL}:31${String(i+1).padStart(3, '0')}`)
}

export function handleSummary(data) {
  return {
    [`results/summary_${__ENV.SCHEDULER_TYPE}_${__ENV.POD_AMOUNT}_${__ENV.VIRTUAL_USERS}.html`]: reportHTML(data, {title:`${__ENV.SCHEDULER_TYPE} - ${__ENV.POD_AMOUNT} pods - ${__ENV.VIRTUAL_USERS} virtual users`})
  };
}

export default function () {
  //const url = urls[randomIntBetween(0, urls.length - 1)]
  const url = urls[getNormallyDistributedRandomNumber(urls.length)]
  const res = http.get(url)
  sleep(0.5);
}
