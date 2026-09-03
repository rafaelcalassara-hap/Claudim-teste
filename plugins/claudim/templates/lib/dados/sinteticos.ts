/** Gerador de dado falso.
 *
 * Existe por uma razão: dado de pessoa real não entra em arquivo, nem em
 * seed, nem em CSV de exemplo. Se você precisa de uma tabela para montar a
 * tela antes de o banco existir, gere aqui.
 *
 * Os números saem com dígito verificador válido para o app conseguir
 * validá-los, mas são gerados na hora e nunca gravados em arquivo — o hook do
 * plugin bloqueia se alguém tentar salvar um deles no repositório.
 */

const PRIMEIROS = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Felipe", "Gabriela",
  "Heitor", "Isabel", "João", "Karina", "Lucas", "Mariana", "Nuno", "Olívia",
  "Paulo", "Renata", "Sérgio", "Tatiana", "Vitor"];
const SOBRENOMES = ["Almeida", "Barbosa", "Cardoso", "Dias", "Esteves", "Ferreira",
  "Gomes", "Henriques", "Ibrahim", "Jardim", "Lima", "Moreira", "Nogueira",
  "Oliveira", "Pereira", "Queiroz", "Ramos", "Santos"];
const CANAIS = ["busca paga", "orgânico", "meta ads", "whatsapp", "corretor", "e-mail"];
const UFS = ["SP", "RJ", "MG", "BA", "CE", "PE", "PR", "RS", "GO", "PA"];

/** Aleatório com semente: a mesma semente dá sempre a mesma tabela. */
function gerador(semente: number) {
  let estado = semente >>> 0;
  return () => {
    estado = (estado * 1664525 + 1013904223) >>> 0;
    return estado / 0x100000000;
  };
}

const inteiro = (r: () => number, min: number, max: number) =>
  min + Math.floor(r() * (max - min + 1));
const escolher = <T,>(r: () => number, lista: T[]) => lista[inteiro(r, 0, lista.length - 1)];

function digito(digitos: number[]): number {
  const pesoInicial = digitos.length + 1;
  const soma = digitos.reduce((acc, d, i) => acc + d * (pesoInicial - i), 0);
  return ((soma * 10) % 11) % 10;
}

export function cpfFicticio(r: () => number = Math.random): string {
  const base: number[] = Array.from({ length: 9 }, () => inteiro(r, 0, 9));
  base.push(digito(base));
  base.push(digito(base));
  const d = base.join("");
  return `${d.slice(0, 3)}.${d.slice(3, 6)}.${d.slice(6, 9)}-${d.slice(9)}`;
}

/** CNS com 15 dígitos que fecha na regra de módulo 11. */
export function cnsFicticio(r: () => number = Math.random): string {
  for (let tentativa = 0; tentativa < 500; tentativa++) {
    const base = [escolher(r, [1, 2, 7, 8, 9]), ...Array.from({ length: 13 }, () => inteiro(r, 0, 9))];
    const soma = base.reduce((acc, d, i) => acc + d * (15 - i), 0);
    const ultimo = ((-soma % 11) + 11) % 11;
    if (ultimo < 10) return [...base, ultimo].join("");
  }
  throw new Error("não consegui gerar um CNS válido");
}

export function nomeFicticio(r: () => number = Math.random): string {
  return `${escolher(r, PRIMEIROS)} ${escolher(r, SOBRENOMES)}`;
}

export function emailFicticio(nome: string, r: () => number = Math.random): string {
  const usuario = nome.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/\s+/g, ".");
  return `${usuario}${inteiro(r, 1, 99)}@exemplo.invalid`;
}

export function telefoneFicticio(r: () => number = Math.random): string {
  return `(${escolher(r, [11, 21, 31, 71, 85])}) 9${inteiro(r, 1000, 9999)}-${inteiro(r, 1000, 9999)}`;
}

export type LinhaExemplo = {
  id: string;
  criadoEm: string;
  nome: string;
  email: string;
  telefone: string;
  uf: string;
  canal: string;
  valor: number;
};

/**
 * Tabela pronta para montar a tela enquanto o banco não está configurado.
 *
 * Sem coluna de condição de saúde — de propósito. Se a sua tela precisa de
 * uma, invoque a skill `dados-sensiveis` antes de inventar uma aqui.
 */
export function tabelaExemplo(linhas = 100, semente = 42): LinhaExemplo[] {
  const r = gerador(semente);
  const agora = Date.now();
  return Array.from({ length: linhas }, (_, i) => {
    const nome = nomeFicticio(r);
    return {
      id: String(10_000 + i),
      criadoEm: new Date(agora - inteiro(r, 0, 24 * 180) * 3_600_000).toISOString(),
      nome,
      email: emailFicticio(nome, r),
      telefone: telefoneFicticio(r),
      uf: escolher(r, UFS),
      canal: escolher(r, CANAIS),
      valor: Math.round(inteiro(r, 12_000, 240_000)) / 100,
    };
  }).sort((a, b) => b.criadoEm.localeCompare(a.criadoEm));
}
