import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://countrypilot.info"),
  title: {
    default: "CountryPilot — Make your next move with confidence",
    template: "%s | CountryPilot",
  },
  description:
    "Independent, practical guides to visas, jobs, study, insurance, banking and moving abroad. Compare your options and plan your next move with confidence.",
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    siteName: "CountryPilot",
    title: "CountryPilot — Make your next move with confidence",
    description:
      "Clear, independent guidance for every step of your move abroad.",
    url: "https://countrypilot.info/",
  },
  twitter: { card: "summary_large_image" },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}