import type { Metadata } from "next";
import { auth, signOut } from "@/auth";
import { authConfigurado } from "@/lib/config";
import "./globals.css";

export const metadata: Metadata = {
  title: "{{NOME_DO_PROJETO}}",
  description: "{{OBJETIVO}}",
};

/** Quem está logado e como sair. Sem login configurado, não aparece nada. */
async function Sessao() {
  if (!authConfigurado()) return null;
  const sessao = await auth();
  if (!sessao?.user?.email) return null;
  return (
    <form
      action={async () => {
        "use server";
        await signOut({ redirectTo: "/entrar" });
      }}
      className="flex items-center gap-3 text-sm text-muted-foreground"
    >
      <span>{sessao.user.email}</span>
      <button type="submit" className="underline">
        sair
      </button>
    </form>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen">
        <header className="flex items-center justify-between border-b border-border-muted px-6 py-3">
          <span className="font-semibold">{"{{NOME_DO_PROJETO}}"}</span>
          <Sessao />
        </header>
        <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
