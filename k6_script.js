import http from 'k6/http';
import { sleep } from 'k6';
import { reportHTML } from "https://raw.githubusercontent.com/fziviello/k6-report-html/main/dist/reportHtml.min.js";
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';

export const options = {
  stages: [
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS)},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 2},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 3},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 4},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 5},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 6},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 7},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 8},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 9},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 10},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 11},
    { duration: '5m', target: parseInt(__ENV.VIRTUAL_USERS) * 12},
  ],
};

const API_BASE_URL = `http://${__ENV.SVC_IP}`

const urls = []

for (let i = 0; i < Math.ceil(parseInt(__ENV.POD_AMOUNT)/2); i++) {
  urls.push(`${API_BASE_URL}:31${String(i+1).padStart(3, '0')}/do`)
}

export function handleSummary(data) {
  return {
    [`summary_${__ENV.SCHEDULER_TYPE}_${__ENV.POD_AMOUNT}_${__ENV.VIRTUAL_USERS}.html`]: reportHTML(data, {title:`${__ENV.SCHEDULER_TYPE} - ${__ENV.POD_AMOUNT} pods - ${__ENV.VIRTUAL_USERS} virtual users`})
  };
}

export default function () {
  const url = urls[randomIntBetween(0, urls.length - 1)]
  const res = http.get(url)
  sleep(1);
}
