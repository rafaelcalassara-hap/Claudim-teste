import { signIn } from "@/auth";
import { authConfigurado } from "@/lib/config";

export default function Pagina() {
  if (!authConfigurado()) {
    return (
      <p className="rounded-lg border border-border-muted p-6 text-center text-muted-foreground">
        O login ainda não foi configurado neste projeto.
      </p>
    );
  }
  return (
    <div className="flex flex-col items-center gap-4 py-12">
      <form
        action={async () => {
          "use server";
          await signIn("google", { redirectTo: "/" });
        }}
      >
        <button
          type="submit"
          className="rounded-lg border border-border-muted px-6 py-3 font-medium"
        >
          Entrar com a conta da empresa
        </button>
      </form>
      {/* Não existe tela de criar conta: a conta é a do Google da empresa, e o
          acesso a esta aplicação é concedido, não solicitado. */}
      <p className="text-sm text-muted-foreground">
        Não consegue entrar? Peça acesso a quem criou esta aplicação.
      </p>
    </div>
  );
}
