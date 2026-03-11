import './globals.css';
import Navbar from '@/components/navbar';

export const metadata = {
    title: 'Diskusjonsforum',
    description: 'Et enkelt diskusjonsforum',
};

export default function RootLayout({ children }) {
    return (
        <html lang="no">
            <body>
                <Navbar />
                {children}
            </body>
        </html>
    );
}