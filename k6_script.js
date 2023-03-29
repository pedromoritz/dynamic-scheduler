import http from 'k6/http';
import PD from './node_modules/probability-distributions-k6/index.js';
import { sleep } from 'k6';

export const options = {
  discardResponseBodies: true,
  scenarios: {
    contacts: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30m', target: 1000},
      ],
      gracefulRampDown: '0s',
    },
  },
};

const API_BASE_URL = 'http://url'

const urls = []

for (let i = 0; i < 6; i++) {
  urls.push(`${API_BASE_URL}:31${String(i+1).padStart(3, '0')}`)
}

export default function () {
  const rnorm_output = PD.rnorm(1, Math.round(urls.length / 2), 1)
  const round_rnorm_output = Math.round(rnorm_output)
  const limited_round_rnorm_output = Math.min(urls.length, Math.max(1, round_rnorm_output))
  console.log(limited_round_rnorm_output)
  const url = urls[limited_round_rnorm_output - 1]
  http.get(url)
  sleep(0.5);
}
