/** O cronômetro entre séries.
 *
 *  O descanso já está prescrito; o que faltava era não precisar do relógio do
 *  celular com a mão suada. Conta para baixo, avisa com uma vibração curta — e
 *  continua certo se a tela apagar, porque o tempo é calculado a partir do
 *  instante em que começou, não somando ticks que o navegador pode não entregar.
 */

import { useEffect, useRef, useState } from "react";

import "./cronometro.css";

function relogio(segundos: number): string {
  const minutos = Math.floor(Math.abs(segundos) / 60);
  const resto = Math.abs(segundos) % 60;
  const sinal = segundos < 0 ? "+" : "";
  return `${sinal}${minutos}:${String(resto).padStart(2, "0")}`;
}

export function CronometroDeDescanso({
  segundos,
  aoFechar,
}: {
  segundos: number;
  aoFechar: () => void;
}) {
  const comeco = useRef(Date.now());
  const [restante, definirRestante] = useState(segundos);
  const jaAvisou = useRef(false);

  useEffect(() => {
    const passo = setInterval(() => {
      // A partir do instante inicial: um `setInterval` de fundo perde ticks
      // quando a tela apaga, e o descanso sairia curto sem ninguém notar.
      const decorrido = Math.round((Date.now() - comeco.current) / 1000);
      definirRestante(segundos - decorrido);
    }, 250);
    return () => clearInterval(passo);
  }, [segundos]);

  useEffect(() => {
    if (restante > 0 || jaAvisou.current) return;
    jaAvisou.current = true;
    // Vibração curta: no meio da série ninguém está olhando para a tela.
    if (typeof navigator !== "undefined" && "vibrate" in navigator) {
      navigator.vibrate?.([200, 100, 200]);
    }
  }, [restante]);

  return (
    <div className={`cronometro${restante <= 0 ? " acabou" : ""}`} role="timer">
      <div>
        <p className="rotulo">{restante <= 0 ? "Descanso completo" : "Descanso"}</p>
        <p className="cronometro-tempo">{relogio(restante)}</p>
      </div>
      <button type="button" className="botao secundario" onClick={aoFechar}>
        {restante <= 0 ? "Fechar" : "Pular"}
      </button>
    </div>
  );
}
