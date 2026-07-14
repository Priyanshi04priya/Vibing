import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'VibeTrip AI',
  description: 'Plan experiences, not trips.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
