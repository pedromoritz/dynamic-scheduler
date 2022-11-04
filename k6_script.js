import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    //{ duration: '10s', target: 10 },
    { duration: '1m', target: 400 },
    //{ duration: '10s', target: 10 },
  ],
};

const API_BASE_URL = 'http://localhost';

export default function () {
  http.batch([
    ['GET', `${API_BASE_URL}:3000/memory/increase`]
  ]);

  sleep(1);
}
