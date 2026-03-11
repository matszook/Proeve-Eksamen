'use client'

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { getThreads, deleteThread } from '@/lib/api';

export default function Home() {
    const router = useRouter();
    const [threads, setThreads] = useState([]);
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState(null);

    useEffect(() => {
        const stored = localStorage.getItem('user');
        if (stored) setUser(JSON.parse(stored));
        fetchThreads();
    }, []);

    const fetchThreads = async () => {
        try {
            const res = await getThreads();
            setThreads(res.data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (!confirm('Er du sikker på at du vil slette denne tråden?')) return;
        try {
            await deleteThread(id);
            setThreads(threads.filter(t => t._id !== id));
        } catch (err) {
            alert(err.response?.data?.error || 'Noe gikk galt');
        }
    };

    if (loading) return <div style={{ padding: '2rem' }}>Laster...</div>;

    return (
        <div style={{ maxWidth: '800px', margin: '2rem auto', padding: '0 1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Tråder <span style={{ color: '#e8927c' }}>({threads.length})</span></h1>
                {user && user.role !== 'guest' && (
                    <button onClick={() => router.push('/threads/new')} style={{
                        background: '#e8927c',
                        color: '#132228',
                        border: 'none',
                        padding: '0.7rem 1.5rem',
                        borderRadius: '5px',
                        fontWeight: 'bold',
                        cursor: 'pointer',
                    }}>
                        + Ny tråd
                    </button>
                )}
            </div>

            {threads.length === 0 ? (
                <div style={{
                    background: '#1a2e35',
                    border: '1px solid rgba(232,146,124,0.2)',
                    borderRadius: '8px',
                    padding: '2rem',
                    textAlign: 'center',
                    color: '#7a9ba5',
                }}>
                    Ingen tråder enda. Vær den første til å starte en diskusjon!
                </div>
            ) : (
                threads.map(thread => (
                    <div key={thread._id} style={{
                        background: '#1a2e35',
                        border: '1px solid rgba(232,146,124,0.2)',
                        borderRadius: '8px',
                        padding: '1.5rem',
                        marginBottom: '1rem',
                    }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                            <div>
                                <Link href={`/threads/${thread._id}`} style={{ fontSize: '1.2rem', fontWeight: 'bold', color: '#f0ebe3' }}>
                                    {thread.title}
                                </Link>
                                <p style={{ color: '#7a9ba5', fontSize: '0.85rem', marginTop: '0.4rem' }}>
                                    av {thread.author_name} · {thread.comment_count} kommentarer
                                </p>
                            </div>
                            {user && (user.role === 'admin' || user.role === 'moderator' || user.username === thread.author) && (
                                <button onClick={() => handleDelete(thread._id)} style={{
                                    background: 'transparent',
                                    color: '#e8927c',
                                    border: '1px solid #e8927c',
                                    padding: '0.3rem 0.8rem',
                                    borderRadius: '4px',
                                    cursor: 'pointer',
                                    fontSize: '0.8rem',
                                }}>
                                    Slett
                                </button>
                            )}
                        </div>
                    </div>
                ))
            )}
        </div>
    );
}