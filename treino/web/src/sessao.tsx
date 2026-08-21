/** Quem está logado, disponível para o app inteiro. */

import { createContext, useCallback, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

import { api, ErroDaApi } from "./api/cliente";
import type { QuemSouEu } from "./api/tipos";

interface Contexto {
  eu: QuemSouEu | null;
  /** `true` até a primeira resposta de /api/eu — antes disso não dá para saber
   *  se a pessoa está logada, e redirecionar cedo demais expulsa quem está. */
  carregando: boolean;
  entrar: (email: string, senha: string) => Promise<void>;
  sair: () => Promise<void>;
  /** Relê `/api/eu`. Serve para o que muda no servidor e a tela precisa refletir
   *  — trocar a senha tira a marca de provisória, e o aviso some sozinho. */
  recarregar: () => Promise<void>;
}

const SessaoContexto = createContext<Contexto | null>(null);

export function ProvedorDeSessao({ children }: { children: ReactNode }) {
  const [eu, definirEu] = useState<QuemSouEu | null>(null);
  const [carregando, definirCarregando] = useState(true);

  useEffect(() => {
    let vivo = true;

    api
      .eu()
      .then((quem) => vivo && definirEu(quem))
      .catch((erro) => {
        // 401 aqui é o caso normal de quem ainda não entrou, não um problema.
        if (!(erro instanceof ErroDaApi && erro.naoAutenticado)) {
          console.error("Não foi possível confirmar a sessão:", erro);
        }
      })
      .finally(() => vivo && definirCarregando(false));

    return () => {
      vivo = false;
    };
  }, []);

  const entrar = useCallback(async (email: string, senha: string) => {
    definirEu(await api.entrar(email, senha));
  }, []);

  const recarregar = useCallback(async () => {
    definirEu(await api.eu());
  }, []);

  const sair = useCallback(async () => {
    try {
      await api.sair();
    } finally {
      // Mesmo se a chamada falhar, o estado local sai — deixar a tela como se
      // ainda houvesse sessão é pior do que pedir login de novo.
      definirEu(null);
    }
  }, []);

  return (
    <SessaoContexto.Provider value={{ eu, carregando, entrar, sair, recarregar }}>
      {children}
    </SessaoContexto.Provider>
  );
}

export function useSessao(): Contexto {
  const contexto = useContext(SessaoContexto);
  if (contexto === null) {
    throw new Error("useSessao precisa estar dentro de <ProvedorDeSessao>.");
  }
  return contexto;
}
