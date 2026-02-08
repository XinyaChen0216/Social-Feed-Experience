// Axios: used to send HTTP requests from Vue to Django
import axios from "axios";

const api = axios.create({
    baseURL: "/api", // proxy will forward to Django
});

export default api;
