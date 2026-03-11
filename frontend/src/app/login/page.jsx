'use client'

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { login, register } from '@/lib/api';

export default function LoginPage() {
    const router = useRouter();
    const [tab, setTab] = useState('login');
    const [error, setError] = useState('');
    const [form, setForm] = useState({ username: '', password: '', name: '' });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const res = await login({ username: form.username, password: form.password });
            localStorage.setItem('token', res.data.token);
            localStorage.setItem('user', JSON.stringify({
                username: res.data.username,
                name: res.data.name,
                role: res.data.role,
            }));
            router.push('/');
        } catch (err) {
            setError(err.response?.data?.error || 'Noe gikk galt');
        }
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const res = await register({ username: form.username, password: form.password, name: form.name });
            localStorage.setItem('token', res.data.token);
            localStorage.setItem('user', JSON.stringify({
                username: res.data.username,
                name: res.data.name,
                role: res.data.role,
            }));
            router.push('/');
        } catch (err) {
            setError(err.response?.data?.error || 'Noe gikk galt');
        }
    };

    return (
        <div style={{ maxWidth: '460px', margin: '4rem auto', padding: '0 1rem' }}>
            <h1 style={{ marginBottom: '2rem', textAlign: 'center' }}>
                Velkommen <span style={{ color: '#e8927c' }}>tilbake</span>
            </h1>

            <div style={{ display: 'flex' }}>
                {['login', 'register'].map((t) => (
                    <button key={t} onClick={() => setTab(t)} style={{
                        flex: 1,
                        padding: '0.9rem',
                        background: tab === t ? '#1a2e35' : '#132228',
                        color: tab === t ? '#e8927c' : '#7a9ba5',
                        border: '1px solid rgba(232,146,124,0.2)',
                        cursor: 'pointer',
                        fontWeight: 'bold',
                        fontSize: '0.85rem',
                        letterSpacing: '1px',
                    }}>
                        {t === 'login' ? 'LOGG INN' : 'REGISTRER'}
                    </button>
                ))}
            </div>

            <div style={{
                background: '#1a2e35',
                border: '1px solid rgba(232,146,124,0.2)',
                borderTop: 'none',
                borderRadius: '0 0 8px 8px',
                padding: '2rem',
            }}>
                {error && (
                    <div style={{
                        background: 'rgba(232,146,124,0.2)',
                        border: '1px solid #e8927c',
                        color: '#e8927c',
                        padding: '0.8rem',
                        borderRadius: '5px',
                        marginBottom: '1rem',
                        fontSize: '0.9rem',
                    }}>
                        {error}
                    </div>
                )}

                <form onSubmit={tab === 'login' ? handleLogin : handleRegister}>
                    {tab === 'register' && (
                        <div style={{ marginBottom: '1rem' }}>
                            <label style={{ display: 'block', color: '#7a9ba5', fontSize: '0.75rem', marginBottom: '0.4rem', letterSpacing: '2px' }}>
                                FULLT NAVN
                            </label>
                            <input
                                type="text"
                                name="name"
                                value={form.name}
                                onChange={handleChange}
                                required
                                style={{
                                    width: '100%',
                                    background: '#132228',
                                    border: '1px solid rgba(232,146,124,0.3)',
                                    borderRadius: '5px',
                                    padding: '0.8rem',
                                    color: '#f0ebe3',
                                    fontSize: '0.9rem',
                                    outline: 'none',
                                }}
                            />
                        </div>
                    )}

                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ display: 'block', color: '#7a9ba5', fontSize: '0.75rem', marginBottom: '0.4rem', letterSpacing: '2px' }}>
                            BRUKERNAVN
                        </label>
                        <input
                            type="text"
                            name="username"
                            value={form.username}
                            onChange={handleChange}
                            required
                            style={{
                                width: '100%',
                                background: '#132228',
                                border: '1px solid rgba(232,146,124,0.3)',
                                borderRadius: '5px',
                                padding: '0.8rem',
                                color: '#f0ebe3',
                                fontSize: '0.9rem',
                                outline: 'none',
                            }}
                        />
                    </div>

                    <div style={{ marginBottom: '1.5rem' }}>
                        <label style={{ display: 'block', color: '#7a9ba5', fontSize: '0.75rem', marginBottom: '0.4rem', letterSpacing: '2px' }}>
                            PASSORD
                        </label>
                        <input
                            type="password"
                            name="password"
                            value={form.password}
                            onChange={handleChange}
                            required
                            style={{
                                width: '100%',
                                background: '#132228',
                                border: '1px solid rgba(232,146,124,0.3)',
                                borderRadius: '5px',
                                padding: '0.8rem',
                                color: '#f0ebe3',
                                fontSize: '0.9rem',
                                outline: 'none',
                            }}
                        />
                    </div>

                    <button type="submit" style={{
                        width: '100%',
                        padding: '1rem',
                        background: '#e8927c',
                        color: '#132228',
                        border: 'none',
                        borderRadius: '5px',
                        fontWeight: 'bold',
                        fontSize: '1rem',
                        letterSpacing: '2px',
                        cursor: 'pointer',
                    }}>
                        {tab === 'login' ? 'LOGG INN →' : 'REGISTRER →'}
                    </button>
                </form>
            </div>
        </div>
    );
}