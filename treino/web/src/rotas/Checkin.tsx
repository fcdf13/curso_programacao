/** O check-in da semana, pela mão do aluno.
 *
 *  Tudo é opcional de propósito: um check-in com só o peso vale mais que um
 *  formulário completo que ninguém preenche. As escalas de 1 a 5 vão todas na
 *  mesma direção — 5 é sempre o melhor — para ninguém responder no automático
 *  e errar o sentido.
 */

import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";

import { api, ErroDaApi } from "../api/cliente";
import type { Checkin as CheckinDaSemana, NovoCheckin } from "../api/tipos";
import { useSessao } from "../sessao";
import "./checkin.css";
import "./paginas.css";

const ESCALAS = [
  { campo: "qualidade_do_sono", rotulo: "Qualidade do sono", pior: "Péssima", melhor: "Ótima" },
  { campo: "disposicao", rotulo: "Disposição", pior: "No chão", melhor: "Ótima" },
  { campo: "recuperacao", rotulo: "Recuperação muscular", pior: "Dolorido", melhor: "Recuperado" },
] as const;

type Campos = Record<string, string>;

function segundaDestaSemana(): string {
  const hoje = new Date();
  // getDay() põe o domingo em 0; a semana do app começa na segunda.
  const desde = (hoje.getDay() + 6) % 7;
  const segunda = new Date(hoje);
  segunda.setDate(hoje.getDate() - desde);
  return segunda.toISOString().slice(0, 10);
}

function doCheckin(checkin: CheckinDaSemana | null): Campos {
  const texto = (valor: number | null | undefined) =>
    valor === null || valor === undefined ? "" : String(valor);
  return {
    peso_kg: texto(checkin?.peso_kg),
    horas_de_sono: texto(checkin?.horas_de_sono),
    passos_por_dia: texto(checkin?.passos_por_dia),
    qualidade_do_sono: texto(checkin?.qualidade_do_sono),
    disposicao: texto(checkin?.disposicao),
    recuperacao: texto(checkin?.recuperacao),
    aderencia_dieta: texto(checkin?.aderencia_dieta),
    aderencia_treino: texto(checkin?.aderencia_treino),
    observacoes: checkin?.observacoes ?? "",
    cintura_cm: texto(checkin?.medidas?.cintura_cm),
    quadril_cm: texto(checkin?.medidas?.quadril_cm),
    torax_cm: texto(checkin?.medidas?.torax_cm),
    braco_cm: texto(checkin?.medidas?.braco_cm),
    coxa_cm: texto(checkin?.medidas?.coxa_cm),
    panturrilha_cm: texto(checkin?.medidas?.panturrilha_cm),
  };
}

const numeroOuNulo = (valor: string) =>
  valor.trim() === "" ? null : Number(valor.replace(",", "."));

export function Checkin() {
  const { eu } = useSessao();
  const navegar = useNavigate();
  const alunoId = eu?.aluno_id ?? null;

  const [campos, definirCampos] = useState<Campos>(() => doCheckin(null));
  const [existente, definirExistente] = useState<CheckinDaSemana | null>(null);
  const [medindo, definirMedindo] = useState(false);
  const [erro, definirErro] = useState<string | null>(null);
  const [enviando, definirEnviando] = useState(false);
  const [salvo, definirSalvo] = useState(false);

  useEffect(() => {
    if (alunoId === null) return;
    const semana = segundaDestaSemana();
    api
      .listarCheckins(alunoId, 2)
      .then((lista) => {
        // Preencher o que já existe evita o 409 e deixa o aluno corrigir o que
        // mandou na segunda depois de pesar de novo na quinta.
        const desta = lista.find((item) => item.semana === semana) ?? null;
        definirExistente(desta);
        definirCampos(doCheckin(desta));
        if (desta?.medidas) definirMedindo(true);
      })
      .catch(() => undefined);
  }, [alunoId]);

  function alterar(campo: string, valor: string) {
    definirCampos((atual) => ({ ...atual, [campo]: valor }));
    definirSalvo(false);
  }

  async function enviar(evento: FormEvent) {
    evento.preventDefault();
    if (alunoId === null) return;

    definirErro(null);
    definirEnviando(true);

    const medidas = {
      cintura_cm: numeroOuNulo(campos.cintura_cm ?? ""),
      quadril_cm: numeroOuNulo(campos.quadril_cm ?? ""),
      torax_cm: numeroOuNulo(campos.torax_cm ?? ""),
      braco_cm: numeroOuNulo(campos.braco_cm ?? ""),
      coxa_cm: numeroOuNulo(campos.coxa_cm ?? ""),
      panturrilha_cm: numeroOuNulo(campos.panturrilha_cm ?? ""),
    };

    const dados: NovoCheckin = {
      semana: segundaDestaSemana(),
      peso_kg: numeroOuNulo(campos.peso_kg ?? ""),
      horas_de_sono: numeroOuNulo(campos.horas_de_sono ?? ""),
      passos_por_dia: numeroOuNulo(campos.passos_por_dia ?? ""),
      qualidade_do_sono: numeroOuNulo(campos.qualidade_do_sono ?? ""),
      disposicao: numeroOuNulo(campos.disposicao ?? ""),
      recuperacao: numeroOuNulo(campos.recuperacao ?? ""),
      aderencia_dieta: numeroOuNulo(campos.aderencia_dieta ?? ""),
      aderencia_treino: numeroOuNulo(campos.aderencia_treino ?? ""),
      observacoes: (campos.observacoes ?? "").trim() || null,
      medidas: Object.values(medidas).some((valor) => valor !== null) ? medidas : null,
    };

    try {
      const salvoAgora = existente
        ? await api.editarCheckin(existente.id, dados)
        : await api.registrarCheckin(alunoId, dados);
      definirExistente(salvoAgora);
      definirSalvo(true);
    } catch (falha) {
      definirErro(falha instanceof ErroDaApi ? falha.message : "Não foi possível salvar.");
    } finally {
      definirEnviando(false);
    }
  }

  return (
    <main className="conteudo pilha">
      <div className="titulo-da-pagina">
        <div>
          <p className="rotulo">
            Semana de{" "}
            {new Date(`${segundaDestaSemana()}T00:00:00`).toLocaleDateString("pt-BR")}
          </p>
          <h1>{existente ? "Editar o check-in" : "Check-in da semana"}</h1>
        </div>
      </div>

      <form className="painel pilha" onSubmit={enviar}>
        <p className="dica">
          Preencha o que souber. Um check-in só com o peso já vale — o que não
          serve é a semana em branco.
        </p>

        <div className="linha-de-campos">
          <label className="campo">
            <span>Peso (kg)</span>
            <input
              type="number"
              inputMode="decimal"
              step="0.1"
              min="20"
              max="400"
              value={campos.peso_kg}
              onChange={(evento) => alterar("peso_kg", evento.target.value)}
            />
          </label>
          <label className="campo">
            <span>Sono (h por noite)</span>
            <input
              type="number"
              inputMode="decimal"
              step="0.5"
              min="0"
              max="16"
              value={campos.horas_de_sono}
              onChange={(evento) => alterar("horas_de_sono", evento.target.value)}
            />
          </label>
          <label className="campo">
            <span>Passos por dia</span>
            <input
              type="number"
              inputMode="numeric"
              step="500"
              min="0"
              value={campos.passos_por_dia}
              onChange={(evento) => alterar("passos_por_dia", evento.target.value)}
            />
          </label>
        </div>

        {ESCALAS.map((escala) => (
          <fieldset className="escala" key={escala.campo}>
            <legend>{escala.rotulo}</legend>
            <div className="escala-notas">
              <span className="escala-ponta">{escala.pior}</span>
              {[1, 2, 3, 4, 5].map((nota) => (
                <label
                  key={nota}
                  className={`nota ${campos[escala.campo] === String(nota) ? "marcada" : ""}`}
                >
                  <input
                    type="radio"
                    name={escala.campo}
                    value={nota}
                    checked={campos[escala.campo] === String(nota)}
                    onChange={() => alterar(escala.campo, String(nota))}
                  />
                  {nota}
                </label>
              ))}
              <span className="escala-ponta">{escala.melhor}</span>
            </div>
          </fieldset>
        ))}

        <div className="linha-de-campos">
          <label className="campo">
            <span>Aderência à dieta (%)</span>
            <input
              type="number"
              inputMode="numeric"
              step="5"
              min="0"
              max="100"
              value={campos.aderencia_dieta}
              onChange={(evento) => alterar("aderencia_dieta", evento.target.value)}
            />
          </label>
          <label className="campo">
            <span>Aderência ao treino (%)</span>
            <input
              type="number"
              inputMode="numeric"
              step="5"
              min="0"
              max="100"
              value={campos.aderencia_treino}
              onChange={(evento) => alterar("aderencia_treino", evento.target.value)}
            />
          </label>
        </div>

        <div>
          <button
            type="button"
            className="botao discreto"
            onClick={() => definirMedindo((aberto) => !aberto)}
            aria-expanded={medindo}
          >
            {medindo ? "Esconder as medidas" : "Adicionar medidas de fita"}
          </button>
          {medindo && (
            <div className="linha-de-campos" style={{ marginTop: 12 }}>
              {[
                ["cintura_cm", "Cintura"],
                ["quadril_cm", "Quadril"],
                ["torax_cm", "Tórax"],
                ["braco_cm", "Braço"],
                ["coxa_cm", "Coxa"],
                ["panturrilha_cm", "Panturrilha"],
              ].map(([campo, rotulo]) => (
                <label className="campo" key={campo}>
                  <span>{rotulo} (cm)</span>
                  <input
                    type="number"
                    inputMode="decimal"
                    step="0.5"
                    min="10"
                    value={campos[campo!] ?? ""}
                    onChange={(evento) => alterar(campo!, evento.target.value)}
                  />
                </label>
              ))}
            </div>
          )}
        </div>

        <label className="campo">
          <span>Como foi a semana</span>
          <textarea
            rows={3}
            value={campos.observacoes}
            onChange={(evento) => alterar("observacoes", evento.target.value)}
            placeholder="Dormi mal na terça, o resto foi tranquilo."
          />
        </label>

        {erro !== null && (
          <p className="aviso erro" role="alert">
            {erro}
          </p>
        )}

        {salvo && (
          <p className="aviso certo" role="status">
            Check-in salvo. Você pode editar até o fim da semana.
          </p>
        )}

        <div className="acoes-do-checkin">
          <button type="submit" className="botao" disabled={enviando}>
            {enviando ? "Salvando…" : existente ? "Salvar alterações" : "Enviar check-in"}
          </button>
          <button
            type="button"
            className="botao secundario"
            onClick={() => navegar("/inicio")}
          >
            Voltar
          </button>
        </div>
      </form>
    </main>
  );
}
