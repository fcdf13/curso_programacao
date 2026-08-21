import { chromium } from "/opt/node22/lib/node_modules/playwright/index.mjs";
const saida = process.argv[2];
const nav = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
const p = await (await nav.newContext({ viewport: { width: 390, height: 844 } })).newPage();

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

await p.locator(".campo-grande input").first().fill("8");
await p.locator(".campo-grande input").nth(1).fill("70");
await p.locator(".botao.registrar").first().click();
await p.waitForTimeout(1000);

await p.goto("http://localhost:8779/inicio");
await p.waitForTimeout(1000);
await p.screenshot({ path: `${saida}/debug-inicio.png`, fullPage: true });
console.log(await p.content().then(h => h.includes("Sua força")));
await nav.close();
