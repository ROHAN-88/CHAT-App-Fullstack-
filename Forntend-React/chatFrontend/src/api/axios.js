import axios from axios

export const $axios = axios.create({
  baseURL: 'http://localhost:5001',
  timeout: 5000,
//   headers: {'X-Custom-Header': 'foobar'}
});


$axios.interceptors.request.use(function (config) {
  // extract accesstoken from local storage
  const accesstoken = localStorage.getItem("accesstoken");

  // if token, set it to every request
  if (accesstoken) {
    config.headers.Authorization = `Bearer ${accesstoken}`;
  }

  return config;
});