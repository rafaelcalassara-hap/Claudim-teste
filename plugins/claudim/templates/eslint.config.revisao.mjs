/** Regras que precisam do tipo para funcionar. Rodam só no `/revisar`.
 *
 * Elas montam o programa TypeScript inteiro antes de analisar, o que é lento
 * demais para o hook que roda a cada arquivo salvo. Em compensação, é aqui que
 * mora o achado que mais dói neste stack: a Promise que ninguém esperou.
 *
 *     db.evento.create({ ... });   // sem await — a página responde antes de gravar
 *
 * `tsc --noEmit` não vê isso, a tela não vê, e só aparece como "salvou mas
 * sumiu". Por isso o revisor roda:
 *
 *     npx eslint --config eslint.config.revisao.mjs .
 *
 * Lista curta de propósito: o revisor entrega no máximo 10 achados, então
 * regra de estilo aqui só empurraria achado grave para fora da lista.
 */

import tseslint from "typescript-eslint";

export default tseslint.config(
  { ignores: [".next/**", "node_modules/**", "out/**", "build/**", "next-env.d.ts"] },
  {
    files: ["**/*.ts", "**/*.tsx"],
    extends: [tseslint.configs.base],
    languageOptions: {
      parserOptions: { projectService: true, tsconfigRootDir: import.meta.dirname },
    },
    rules: {
      // Escrita no banco sem await: a action retorna antes de a gravação
      // terminar, e o `revalidatePath` mostra a tela velha.
      "@typescript-eslint/no-floating-promises": "error",

      // Função async passada onde se espera uma síncrona — típico em onClick e
      // em callback de array. O erro lá dentro vira unhandled rejection.
      "@typescript-eslint/no-misused-promises": "error",

      // `await` em coisa que não é Promise, e async sem await: os dois sinalizam
      // que alguém esqueceu o await em outro lugar.
      "@typescript-eslint/await-thenable": "error",
      "@typescript-eslint/require-await": "warn",
    },
  },
);
