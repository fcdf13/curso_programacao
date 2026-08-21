/** A fila de séries que ainda não chegaram ao servidor.
 *
 *  Subsolo de academia não tem sinal. Perder a série que o aluno acabou de
 *  registrar é o tipo de falha que faz alguém voltar para o caderninho e não
 *  abrir mais o app — então o registro é gravado **primeiro no aparelho** e só
 *  depois enviado. A tela nunca espera a rede para confirmar.
 *
 *  IndexedDB, e não `localStorage`: o iOS descarta `localStorage` de PWA com
 *  alguma agressividade quando o aparelho está sem espaço, e é justamente o
 *  aparelho no meio do treino que não pode perder nada.
 */

import type { SerieParaEnviar } from "./tipos";

const BANCO = "jf-treino";
const DEPOSITO = "series-pendentes";
const VERSAO = 1;

/** Uma série esperando envio, junto do treino a que pertence. */
export interface Pendente {
  /** `${treinoId}:${chave_local}` — uma linha por série, sobrescrita ao corrigir. */
  id: string;
  treinoId: number;
  serie: SerieParaEnviar;
  /** Quando entrou na fila, para a tela poder dizer "há 3 minutos". */
  em: number;
}

let conexao: Promise<IDBDatabase> | null = null;

function abrir(): Promise<IDBDatabase> {
  if (conexao !== null) return conexao;

  conexao = new Promise((resolver, recusar) => {
    const pedido = indexedDB.open(BANCO, VERSAO);
    pedido.onupgradeneeded = () => {
      const banco = pedido.result;
      if (!banco.objectStoreNames.contains(DEPOSITO)) {
        const deposito = banco.createObjectStore(DEPOSITO, { keyPath: "id" });
        deposito.createIndex("treinoId", "treinoId");
      }
    };
    pedido.onsuccess = () => resolver(pedido.result);
    pedido.onerror = () => recusar(pedido.error);
  });

  return conexao;
}

function transacao<T>(
  modo: IDBTransactionMode,
  acao: (deposito: IDBObjectStore) => IDBRequest<T>,
): Promise<T> {
  return abrir().then(
    (banco) =>
      new Promise<T>((resolver, recusar) => {
        const tx = banco.transaction(DEPOSITO, modo);
        const pedido = acao(tx.objectStore(DEPOSITO));
        pedido.onsuccess = () => resolver(pedido.result);
        pedido.onerror = () => recusar(pedido.error);
      }),
  );
}

/** Guarda (ou corrige) uma série na fila. */
export async function enfileirar(treinoId: number, serie: SerieParaEnviar): Promise<void> {
  const pendente: Pendente = {
    id: `${treinoId}:${serie.chave_local}`,
    treinoId,
    serie,
    em: Date.now(),
  };
  await transacao("readwrite", (deposito) => deposito.put(pendente));
}

export async function remover(treinoId: number, chaveLocal: string): Promise<void> {
  await transacao("readwrite", (deposito) => deposito.delete(`${treinoId}:${chaveLocal}`));
}

export async function pendentes(treinoId: number): Promise<Pendente[]> {
  const todas = await transacao<Pendente[]>("readonly", (deposito) => deposito.getAll());
  return todas.filter((item) => item.treinoId === treinoId).sort((a, b) => a.em - b.em);
}

export async function todasPendentes(): Promise<Pendente[]> {
  const todas = await transacao<Pendente[]>("readonly", (deposito) => deposito.getAll());
  return todas.sort((a, b) => a.em - b.em);
}

/** Tira da fila o que o servidor confirmou ter recebido. */
export async function confirmar(treinoId: number, chaves: string[]): Promise<void> {
  await Promise.all(chaves.map((chave) => remover(treinoId, chave)));
}

/** `true` quando o navegador não expõe IndexedDB (modo privado antigo, etc.).
 *
 *  Não é motivo para bloquear o treino: sem fila, a tela cai no envio direto e
 *  avisa quando falhar. Pior seria recusar-se a funcionar.
 */
export function disponivel(): boolean {
  try {
    return typeof indexedDB !== "undefined" && indexedDB !== null;
  } catch {
    return false;
  }
}
