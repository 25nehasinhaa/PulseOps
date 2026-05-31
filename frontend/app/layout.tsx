import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CoralOps",
  description: "AI SRE agent powered by Coral SQL joins and streaming diagnosis"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
