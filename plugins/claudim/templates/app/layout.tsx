import type { Metadata } from "next";
import { ClerkProvider, SignedIn, UserButton } from "@clerk/nextjs";
import { clerkConfigurado } from "@/lib/config";
import "./globals.css";

export const metadata: Metadata = {
  title: "{{NOME_DO_PROJETO}}",
  description: "{{OBJETIVO}}",
};

function Moldura({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen">
        <header className="flex items-center justify-between border-b border-border-muted px-6 py-3">
          <span className="font-semibold">{"{{NOME_DO_PROJETO}}"}</span>
          {clerkConfigurado() && (
            <SignedIn>
              <UserButton />
            </SignedIn>
          )}
        </header>
        <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
      </body>
    </html>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  // Sem chave do Clerk no .env, o ClerkProvider derruba a aplicação na
  // primeira renderização. Enquanto não houver conta, a tela roda sem ele.
  if (!clerkConfigurado()) return <Moldura>{children}</Moldura>;
  return (
    <ClerkProvider>
      <Moldura>{children}</Moldura>
    </ClerkProvider>
  );
}
