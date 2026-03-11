'use client'

import Link from 'next/link';
import { useRouter, usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function Navbar() {
    const router = useRouter();
    const pathname = usePathname();
    const [user, setUser] = useState(null);

    useEffect(() => {
        const stored = localStorage.getItem('user');
        if (stored) setUser(JSON.parse(stored));
    }, [pathname]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        setUser(null);
        router.push('/login');
    };

    return (
        <nav style={{
            background: '#1a2e35',
            borderBottom: '2px solid #e8927c',
            padding: '1rem 2rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
        }}>
            <Link href="/" style={{ color: '#e8927c', fontWeight: 'bold', fontSize: '1.2rem' }}>
                // DISKUSJONSFORUM
            </Link>

            <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
                {user ? (
                    <>
                        <span style={{ color: '#7a9ba5', fontSize: '0.9rem' }}>
                            {user.name}
                        </span>
                        <span style={{
                            background: user.role === 'admin' ? '#e8927c' :
                                       user.role === 'moderator' ? '#4ecdc4' : '#7a9ba5',
                            color: '#132228',
                            padding: '0.2rem 0.6rem',
                            borderRadius: '20px',
                            fontSize: '0.7rem',
                            fontWeight: 'bold',
                        }}>
                            {user.role}
                        </span>
                        {user.role === 'admin' && (
                            <Link href="/admin" style={{ color: '#f0ebe3', fontSize: '0.9rem' }}>
                                Admin
                            </Link>
                        )}
                        <button onClick={handleLogout} style={{
                            background: '#e8927c',
                            color: '#132228',
                            border: 'none',
                            padding: '0.4rem 1rem',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontWeight: 'bold',
                        }}>
                            Logg ut
                        </button>
                    </>
                ) : (
                    <Link href="/login" style={{
                        background: '#e8927c',
                        color: '#132228',
                        padding: '0.4rem 1rem',
                        borderRadius: '4px',
                        fontWeight: 'bold',
                    }}>
                        Logg inn
                    </Link>
                )}
            </div>
        </nav>
    );
}