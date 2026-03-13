import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { QueryProvider } from "@/components/providers/QueryProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Sales.AI | Autonomous Outreach",
  description: "B2B sales orchestration with LangGraph",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} dark bg-surface-950`}>
        <QueryProvider>
          {children}
        </QueryProvider>
      </body>
    </html>
  );
}
