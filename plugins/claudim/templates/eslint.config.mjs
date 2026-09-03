/** Regras de código que rodam a cada arquivo salvo.
 *
 * Divisão de trabalho, para as duas ferramentas não brigarem:
 *   - prettier decide a **forma** (aspas, vírgula, quebra de linha);
 *   - eslint decide o que é **erro** (bug, vazamento, padrão proibido aqui).
 * `eslint-config-prettier` entra por último e desliga toda regra do eslint que
 * opinasse sobre forma.
 *
 * Quem roda isso é um hook do plugin, sozinho, depois de cada escrita: ele
 * conserta o que dá para consertar e devolve o resto para o Claude arrumar.
 * Você não precisa rodar nada à mão.
 */

import { dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { FlatCompat } from "@eslint/eslintrc";
import prettier from "eslint-config-prettier";

const compat = new FlatCompat({ baseDirectory: dirname(fileURLToPath(import.meta.url)) });

export default [
  { ignores: [".next/**", "node_modules/**", "out/**", "build/**", "next-env.d.ts"] },

  ...compat.extends("next/core-web-vitals", "next/typescript"),

  {
    rules: {
      // `any` desliga a única verificação automática que este projeto tem.
      // O erro de tipo que ele cala costuma ser um bug de verdade.
      "@typescript-eslint/no-explicit-any": "error",

      // Variável começando com `_` é descarte proposital (`_anterior` das
      // server actions). O resto é sobra de código — some.
      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          caughtErrorsIgnorePattern: "^_",
          ignoreRestSiblings: true,
        },
      ],

      // Texto vindo do banco entrando como HTML é XSS.
      "react/no-danger": "error",

      // Buscar dado da própria aplicação no navegador é uma volta a mais e
      // manda para o cliente o que não precisava sair do servidor.
      // Server Component + await no Prisma resolve. Ver a skill next-padroes.
      "no-restricted-syntax": [
        "error",
        {
          selector:
            "CallExpression[callee.name='useEffect'] CallExpression[callee.name='fetch']",
          message:
            "Não busque dado da própria aplicação com useEffect + fetch. Busque no Server Component, com await no Prisma (skill next-padroes).",
        },
        {
          selector:
            "CallExpression[callee.property.name='findMany'] > ObjectExpression:not(:has(Property[key.name='take']))",
          message:
            "findMany sem `take`. Toda consulta de lista precisa de um teto de linhas — tabela grande sem limite derruba a página.",
        },
        {
          selector: "CallExpression[callee.property.name='findMany'][arguments.length=0]",
          message:
            "findMany sem argumento nenhum lê a tabela inteira. Passe ao menos `take` e `select`.",
        },
      ],

      // Console fica: é como o projeto registra o que aconteceu. Só `console.log`
      // solto vira aviso, para não virar depuração esquecida no código.
      "no-console": ["warn", { allow: ["info", "warn", "error"] }],

      eqeqeq: ["error", "always", { null: "ignore" }],
      "prefer-const": "error",
      "no-var": "error",
    },
  },

  {
    // O gerador de dado falso monta CPF e CNS dígito a dígito; as regras de
    // índice e de laço aqui só atrapalhariam.
    files: ["lib/dados/sinteticos.ts", "prisma/seed.ts"],
    rules: { "no-restricted-syntax": "off", "no-console": "off" },
  },

  {
    // Arquivo de configuração exporta um objeto anônimo por convenção — o aviso
    // padrão sobre isso apareceria em toda rodada e viraria ruído no /revisar.
    files: ["*.config.mjs", "*.config.ts", "*.config.js"],
    rules: { "import/no-anonymous-default-export": "off" },
  },

  prettier,
];
