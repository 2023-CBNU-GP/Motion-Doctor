import axios, { HeadersDefaults } from 'axios';
import { getCookie } from "@md/hooks/cookies";

const axiosClient = axios.create({
    withCredentials: true,
    baseURL : process.env.NEXT_PUBLIC_API_KEY
});

// axiosClient.interceptors.request.use(
//     config => {
//         const token = getCookie('jwt');
//         if (token) {
//             config.headers = {
//                 "set-cookie": `${token}`,
//                 Accept: "application/json",
//             };
//         }
//         return config;
//     },
//     error => {
//         return Promise.reject(error);
//     }
// );

export default axiosClient;
