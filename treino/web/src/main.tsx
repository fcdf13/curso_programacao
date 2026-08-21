import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import { App } from "./App";
import { ProvedorDeSessao } from "./sessao";
import "./estilo/base.css";

const raiz = document.getElementById("raiz");
if (raiz === null) throw new Error("Não encontrei #raiz no index.html.");

createRoot(raiz).render(
  <StrictMode>
    <BrowserRouter>
      <ProvedorDeSessao>
        <App />
      </ProvedorDeSessao>
    </BrowserRouter>
  </StrictMode>,
);
