import { chromium } from "/opt/node22/lib/node_modules/playwright/index.mjs";
const saida = process.argv[2];
const nav = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await (await nav.newContext({ viewport: { width: 390, height: 844 } })).newPage();
const erros = [];
p.on("pageerror", (e) => erros.push(String(e)));

await p.goto("http://localhost:8779/entrar");
await p.fill('input[type="email"]', "filipe@jftreino.com.br");
await p.fill('input[type="password"]', "demonstracao-2026");
await p.click('button[type="submit"]');
await p.waitForLoadState("networkidle");

await p.goto("http://localhost:8779/inicio");
await p.click(".lista-de-blocos a");
await p.waitForSelector(".titulo-do-treino");
await p.click('a:has-text("Treinar")');
await p.waitForSelector(".serie-da-academia", { timeout: 10000 });

// A segunda linha do supino já vem prefilled com 8x70kg de verdade (VALIDA).
await p.locator(".botao.registrar").nth(1).click();
await p.waitForTimeout(900);

await p.goto("http://localhost:8779/inicio");
await p.waitForSelector("text=Sua força");
await p.waitForTimeout(600);
await p.click('.linha-de-forca');
await p.waitForTimeout(400);
await p.screenshot({ path: `${saida}/forca-aluno.png`, fullPage: true });
const forcaTexto = await p.locator(".linha-de-forca").first().innerText();

const joao = await (await nav.newContext({ viewport: { width: 900, height: 900 } })).newPage();
await joao.goto("http://localhost:8779/entrar");
await joao.fill('input[type="email"]', "joao@jftreino.com.br");
await joao.fill('input[type="password"]', "demonstracao-2026");
await joao.click('button[type="submit"]');
await joao.waitForLoadState("networkidle");
await joao.goto("http://localhost:8779/periodizacoes/1");
await joao.waitForSelector(".prescricao-carga.sugestao");
await joao.waitForTimeout(500);
const sugestaoTexto = await joao.locator(".prescricao-carga.sugestao").first().innerText();
await joao.screenshot({ path: `${saida}/sugestao-joao.png`, fullPage: true });

console.log("força (aluno):", JSON.stringify(forcaTexto.replace(/\n/g, " | ")));
console.log("sugestão (João):", JSON.stringify(sugestaoTexto));
console.log("erros:", JSON.stringify(erros));
await nav.close();
