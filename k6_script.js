import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '5s', target: 10 },
    { duration: '10s', target: 50 },
    { duration: '5s', target: 10 },
  ],
};

const API_BASE_URL = 'http://192.168.59.100';

export default function () {
  http.batch([
    ['GET', `${API_BASE_URL}:31001/memory/increase`]
  ]);

  sleep(1);
}
