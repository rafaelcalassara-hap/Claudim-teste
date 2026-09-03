# Buscar dado

Busque no servidor, com `await`. Nada de `useEffect` + `fetch` para dado da
própria aplicação — é uma volta a mais e vaza para o navegador o que não
precisava sair do servidor.

Mas a página não chama o Prisma. **Consulta mora em `lib/dados/<tabela>.ts`**,
um arquivo por tabela, com toda leitura e toda escrita daquela tabela:

```ts
// lib/dados/eventos.ts
import "server-only";

const TETO = 1000;

export async function listarEventos({ dias }: { dias: number }) {
  if (!bancoConfigurado()) return mascararRegistros(exemploFormatado());

  const linhas = await db.evento.findMany({
    where: { criadoEm: { gte: new Date(Date.now() - dias * 86_400_000) } },
    select: { id: true, criadoEm: true, canal: true, uf: true, valorCentavos: true },
    orderBy: { criadoEm: "desc" },
    take: TETO,
  });

  return mascararRegistros(linhas.map(paraTela));
}
```

```tsx
// app/page.tsx — sessão, filtro, e o que aparece. Só isso.
export default async function Pagina({ searchParams }) {
  await exigirSessao();
  const { dias } = await searchParams;
  return <Tabela linhas={await listarEventos({ dias: Number(dias) || 30 })} />;
}
```

**Por que esse arquivo existe.** Quatro regras deste projeto vivem juntas nele:
`take`, `select` explícito, mascaramento antes de sair do servidor, e centavos
virando reais. Espalhadas por página e action, as quatro dependem de alguém
lembrar de cada uma toda vez. Num arquivo por tabela, é um lugar só para
conferir — e é onde o `/revisar` olha.

**O que ele não é.** Funções `async` exportadas, e pronto. Sem classe, sem
`BaseRepository`, sem interface, sem par entidade/DTO, sem mapper. O que a
função devolve é exatamente o que a tela mostra — já mascarado, já formatado.
Como o mascaramento é obrigatório, só existe uma forma de saída legal, e é essa;
por isso não há camada de conversão para inventar. Tabela nova é **arquivo
novo**, nunca camada nova.

MVC e MVVM não se aplicam aqui: um Server Component já é a view e o controller
ao mesmo tempo, uma action já é o controller de escrita, e o Prisma já é o
model. Não crie `controllers/`, `models/`, `services/` nem `viewmodels/`.

Filtro vai na URL (`searchParams`), não em estado de React: o servidor refaz a
busca, o link fica compartilhável e a tela funciona sem JavaScript.

Schema, tipos do SQLite, dinheiro em centavos e migração: skill `consultar-banco`.
