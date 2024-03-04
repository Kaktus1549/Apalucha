import type { Metadata } from "next";
import './style/global.css';

export const metadata: Metadata = {
  title: "Apalucha 2024",
  description: "Simple website made for film voting!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
