import axios, { HeadersDefaults } from 'axios';

const axiosClient = axios.create();

axiosClient.defaults.baseURL = process.env.NEXT_PUBLIC_API_KEY;

type headers = {
    'Content-Type': string;
    Accept: string;
    Authorization: string;
};

axiosClient.defaults.headers = {
    withCredentials: true,
} as headers & HeadersDefaults;

axiosClient.interceptors.request.use(
    config => {
        const token = sessionStorage.getItem('md-access-token');
        if (token) {
            config.headers!['Authorization'] = token;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

export default axiosClient;
