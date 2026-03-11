import axios from 'axios';

const API = axios.create({
    baseURL: 'http://localhost:5001/api',
});

// Legg til token automatisk på alle forespørsler
API.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// ── Auth ──────────────────────────────────────────────────────────────────────
export const login = (data) => API.post('/login', data);
export const register = (data) => API.post('/register', data);

// ── Tråder ────────────────────────────────────────────────────────────────────
export const getThreads = () => API.get('/threads');
export const getThread = (id) => API.get(`/threads/${id}`);
export const createThread = (data) => API.post('/threads', data);
export const deleteThread = (id) => API.delete(`/threads/${id}`);

// ── Kommentarer ───────────────────────────────────────────────────────────────
export const addComment = (threadId, data) => API.post(`/threads/${threadId}/comments`, data);
export const deleteComment = (threadId, commentId) => API.delete(`/threads/${threadId}/comments/${commentId}`);

// ── Admin ─────────────────────────────────────────────────────────────────────
export const getUsers = () => API.get('/admin/users');
export const updateRole = (username, role) => API.put(`/admin/users/${username}/role`, { role });
export const deleteUser = (username) => API.delete(`/admin/users/${username}`);