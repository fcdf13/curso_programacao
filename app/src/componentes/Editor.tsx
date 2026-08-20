/** CodeMirror configurado para o curso: Python ou SQL, tema conforme o sistema. */

import { python } from "@codemirror/lang-python";
import { sql } from "@codemirror/lang-sql";
import { githubDark, githubLight } from "@uiw/codemirror-theme-github";
import CodeMirror from "@uiw/react-codemirror";
import { useEffect, useState } from "react";

import type { Linguagem } from "../api/tipos";

function usaTemaEscuro(): boolean {
  const [escuro, setEscuro] = useState(
    () => window.matchMedia?.("(prefers-color-scheme: dark)").matches ?? false,
  );
  useEffect(() => {
    const consulta = window.matchMedia("(prefers-color-scheme: dark)");
    const aoMudar = (evento: MediaQueryListEvent) => setEscuro(evento.matches);
    consulta.addEventListener("change", aoMudar);
    return () => consulta.removeEventListener("change", aoMudar);
  }, []);
  return escuro;
}

interface Props {
  codigo: string;
  linguagem: Linguagem;
  onMudar: (codigo: string) => void;
  onCorrigir: () => void;
  altura?: string;
}

export function Editor({ codigo, linguagem, onMudar, onCorrigir, altura }: Props) {
  const escuro = usaTemaEscuro();

  return (
    <div
      className="editor"
      // Ctrl+Enter corrige de qualquer lugar do editor. Fica na captura para
      // vencer os atalhos internos do CodeMirror.
      onKeyDownCapture={(evento) => {
        if ((evento.ctrlKey || evento.metaKey) && evento.key === "Enter") {
          evento.preventDefault();
          onCorrigir();
        }
      }}
    >
      <CodeMirror
        value={codigo}
        height={altura ?? "100%"}
        theme={escuro ? githubDark : githubLight}
        extensions={[linguagem === "sql" ? sql() : python()]}
        onChange={onMudar}
        basicSetup={{
          lineNumbers: true,
          foldGutter: false,
          highlightActiveLine: true,
          autocompletion: true,
          tabSize: 4,
        }}
      />
    </div>
  );
}
