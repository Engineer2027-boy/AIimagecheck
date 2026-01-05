import "./globals.css"; // This links your Tailwind styles

export const metadata = {
  title: "AI Image Detector",
  description: "Check if your image is AI generated",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}