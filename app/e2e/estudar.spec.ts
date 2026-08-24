/** O ciclo de estudo pelo navegador, contra o backend de verdade.
 *
 *  Não há mock: o servidor é o mesmo `curso web`, a correção roda pytest, e o
 *  progresso é gravado. É o teste que prova que as peças se encaixam.
 */

import { expect, test } from "@playwright/test";

const CERTO = "def resolver(a, b):\n    return a + b\n";
const ERRADO = "def resolver(a, b):\n    return a - b\n";

/** Substitui todo o conteúdo do editor — CodeMirror não é um <textarea>.
 *
 *  Espera o texto aparecer de volta na tela antes de devolver: `insertText`
 *  devolve o controle antes de o CodeMirror propagar a mudança para o React,
 *  e clicar em "Corrigir" cedo demais manda o código antigo.
 */
async function escreverNoEditor(page: import("@playwright/test").Page, codigo: string) {
  await page.locator(".cm-content").click();
  await page.keyboard.press("ControlOrMeta+a");
  await page.keyboard.press("Delete");
  await page.keyboard.insertText(codigo);

  const primeiraLinha = codigo.trim().split("\n")[0];
  await expect(page.locator(".cm-content")).toContainText(primeiraLinha);

  // O texto na tela já mudou (CodeMirror atualiza o próprio DOM na hora), mas
  // o onChange que avisa o React ainda pode não ter disparado — sem essa
  // folga, "Corrigir" clicado cedo demais manda o código antigo.
  await page.waitForTimeout(300);
}

test("o plano do dia lista exercícios novos", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Plano de hoje" })).toBeVisible();
  await expect(page.locator(".linha").first()).toContainText("A01-001");
});

test("errar mostra o esperado e o obtido; acertar agenda a revisão", async ({ page }) => {
  await page.goto("/exercicio/A01-005");
  await expect(page.getByRole("heading", { name: "Somar dois números" })).toBeVisible();

  await escreverNoEditor(page, ERRADO);
  await page.getByRole("button", { name: /Corrigir/ }).click();

  const resultado = page.locator(".resultado");
  await expect(resultado).toHaveClass(/errado/);
  await expect(resultado).toContainText("O valor devolvido não bate");
  await expect(resultado.locator("dd.ok")).toHaveText("5");
  await expect(resultado.locator("dd.nao")).toHaveText("-1");

  await escreverNoEditor(page, CERTO);
  await page.getByRole("button", { name: /Corrigir/ }).click();

  await expect(resultado).toHaveClass(/certo/);
  await expect(resultado).toContainText("Passou");
  await expect(resultado).toContainText("Volta para revisão amanhã");
});

test("uma falha de Pandas vira duas tabelas lado a lado", async ({ page }) => {
  await page.goto("/exercicio/B05-001");
  await escreverNoEditor(
    page,
    'import pandas as pd\n\n\ndef resolver(produtos, preco_minimo):\n    return produtos[produtos["preco"] >= preco_minimo]\n',
  );
  await page.getByRole("button", { name: /Corrigir/ }).click();

  const comparacao = page.locator(".comparacao");
  await expect(comparacao).toBeVisible();
  await expect(comparacao.locator(".quadro.esperado .quadro-contagem")).toHaveText("1 linha");
  await expect(comparacao.locator(".quadro.obtido .quadro-contagem")).toHaveText("2 linhas");
  await expect(comparacao.locator(".quadro.obtido tbody tr")).toHaveCount(2);
  await expect(comparacao.locator(".quadro.obtido")).toContainText("Notebook");
});

test("as dicas saem uma de cada vez", async ({ page }) => {
  await page.goto("/exercicio/A02-002");
  await page.getByRole("button", { name: /Pedir uma dica/ }).click();
  await expect(page.locator(".dica")).toHaveCount(1);
  await page.getByRole("button", { name: /Mais uma dica/ }).click();
  await expect(page.locator(".dica")).toHaveCount(2);
  await expect(page.locator(".dica").first()).toContainText("%");
});

test("a teoria do módulo abre ao lado do enunciado", async ({ page }) => {
  await page.goto("/exercicio/A01-001");
  await page.getByRole("button", { name: "Teoria do módulo" }).click();
  await expect(page.locator(".painel-de-leitura")).toContainText("print não é return");
});

test("o catálogo filtra por bloco e por busca", async ({ page }) => {
  await page.goto("/catalogo");
  await expect(page.locator(".linha")).toHaveCount(115);

  await page.getByRole("button", { name: "SQL", exact: true }).click();
  await expect(page.locator(".linha")).toHaveCount(3);

  await page.getByRole("button", { name: "Tudo" }).click();
  await page.getByPlaceholder("buscar").fill("fizzbuzz");
  await expect(page.locator(".linha")).toHaveCount(1);
  await expect(page.locator(".linha")).toContainText("A06-015");
});

test("solução correta mas lenta mostra o tempo, e a eficiente passa", async ({ page }) => {
  // A09-007 pede dedup preservando ordem; a versão ingênua abaixo dá a
  // resposta certa mas é O(n²) — o teste cronometrado precisa reprovar por
  // lentidão, não por resultado errado.
  await page.goto("/exercicio/A09-007");
  await escreverNoEditor(
    page,
    "def resolver(itens: list) -> list:\n" +
      "    resultado = []\n" +
      "    for item in itens:\n" +
      "        if item not in resultado:\n" +
      "            resultado.append(item)\n" +
      "    return resultado\n",
  );
  await page.getByRole("button", { name: /Corrigir/ }).click();

  const resultado = page.locator(".resultado");
  await expect(resultado).toHaveClass(/errado/, { timeout: 15_000 });
  await expect(resultado).toContainText("lenta demais");
  await expect(resultado).toContainText("limite é");

  await escreverNoEditor(
    page,
    "def resolver(itens: list) -> list:\n" +
      "    vistos = set()\n" +
      "    resultado = []\n" +
      "    for item in itens:\n" +
      "        if item not in vistos:\n" +
      "            vistos.add(item)\n" +
      "            resultado.append(item)\n" +
      "    return resultado\n",
  );
  await page.getByRole("button", { name: /Corrigir/ }).click();
  await expect(resultado).toHaveClass(/certo/, { timeout: 15_000 });
});

test("o painel conta o que foi resolvido e desenha os gráficos", async ({ page }) => {
  await page.goto("/exercicio/A01-003");
  await escreverNoEditor(page, 'def resolver() -> str:\n    return "Olá, Aurora!"\n');
  await page.getByRole("button", { name: /Corrigir/ }).click();
  await expect(page.locator(".resultado")).toHaveClass(/certo/);

  await page.goto("/progresso");
  await expect(page.locator(".numero-grande").first()).toContainText("/115");
  await expect(page.getByText("Revisões nos próximos 30 dias")).toBeVisible();
  await expect(page.getByText("Dias praticados")).toBeVisible();
  await expect(page.locator(".svg-calendario .dia.praticou")).toHaveCount(1);
  await expect(page.locator(".barra-preenchida").first()).toBeVisible();
});
