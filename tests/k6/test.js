import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';


export const options = {
  stages: [
    { duration: '1m', target: 50 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],

  thresholds: {
    'checks': ['rate > 0.99'],

    'http_req_duration{name:"GET /posts"}': ['p(95) < 500'],
    'http_req_duration{name:"POST /posts"}': ['p(95) < 2000'],
  },
};

const BASE_URL = 'http://127.0.0.1:8080';

export default function () {
  const random = Math.random();

  if (random < 0.9) {
    const getResponse = http.get(`${BASE_URL}/posts`, {
      tags: { name: 'GET /posts' }
    });

    const getCheck = check(getResponse, {
      'GET /posts status is 200': (r) => r.status === 200,
    });


  } else {
    const username = `user_${Math.random().toString(36).substring(7)}`;

    const postResponse = http.post(
      `${BASE_URL}/posts`,
      JSON.stringify({
        author: username,
        title: `Post by ${username}`
      }),
      {
        headers: { 'Content-Type': 'application/json' },
        tags: { name: 'POST /posts' }
      }
    );

    const postCheck = check(postResponse, {
      'POST /posts status is 201': (r) => r.status === 201,
    });
  }
  sleep(1);
}