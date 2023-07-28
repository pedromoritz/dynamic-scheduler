import http from 'k6/http';

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

export default function () {
  http.get(`http://${__ENV.IP}:31001`);
}
