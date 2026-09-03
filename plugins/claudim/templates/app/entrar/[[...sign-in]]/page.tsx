import { SignIn } from "@clerk/nextjs";
import { clerkConfigurado } from "@/lib/config";

export default function Pagina() {
  if (!clerkConfigurado()) {
    return (
      <p className="rounded-lg border border-border-muted p-6 text-center text-muted-foreground">
        O login ainda não foi configurado neste projeto.
      </p>
    );
  }
  return (
    <div className="flex flex-col items-center gap-4 py-12">
      <SignIn />
      {/* Não existe tela de criar conta: acesso é concedido, não solicitado. */}
      <p className="text-sm text-muted-foreground">
        Não consegue entrar? Peça acesso a quem criou esta aplicação.
      </p>
    </div>
  );
}
