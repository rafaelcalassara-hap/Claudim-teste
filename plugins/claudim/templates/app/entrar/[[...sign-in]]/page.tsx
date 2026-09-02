import { SignIn } from "@clerk/nextjs";
import { clerkConfigurado } from "@/lib/config";

export default function Pagina() {
  if (!clerkConfigurado()) {
    return (
      <p className="rounded-padrao border border-borda p-6 text-center text-texto-suave">
        O login ainda não foi configurado neste projeto.
      </p>
    );
  }
  return (
    <div className="flex flex-col items-center gap-4 py-12">
      <SignIn />
      {/* Não existe tela de criar conta: acesso é concedido, não solicitado. */}
      <p className="text-sm text-texto-suave">
        Não consegue entrar? Peça acesso a quem criou esta aplicação.
      </p>
    </div>
  );
}
