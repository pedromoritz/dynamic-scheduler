import http from 'k6/http';
import { sleep } from 'k6';
import { htmlReport } from "https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js";

export const options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 200 },
    { duration: '30s', target: 10 },
  ],
};

const API_BASE_URL = 'http://192.168.59.100';

export function handleSummary(data) {
  return {
    "summary_testcase-2.html": htmlReport(data),
  };
}

export default function () {
  http.batch([
    ['GET', `${API_BASE_URL}:31001/memory/increase?load=10&duration=10`]
  ]);

  sleep(1);
}
