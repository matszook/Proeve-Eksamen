import './globals.css';

export const metadata = {
    title: 'Diskusjonsforum',
    description: 'Et enkelt diskusjonsforum',
};

export default function RootLayout({ children }) {
    return (
        <html lang="no">
            <body>
                {children}
            </body>
        </html>
    );
}