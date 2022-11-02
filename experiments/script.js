import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2s', target: 10 },
    { duration: '10s', target: 100 },
    { duration: '2s', target: 10 },
  ],
};

const API_BASE_URL = 'http://192.168.59.150';

export default function () {
  http.batch([
    ['GET', `${API_BASE_URL}:31001/stress`]
  ]);

  sleep(1);
}


