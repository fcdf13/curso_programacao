/** Os últimos seis meses, um quadradinho por dia: praticou ou não praticou.
 *
 *  O dado é binário (o progresso guarda as datas, não quantas questões saíram em
 *  cada uma), então são dois estados e não uma rampa — pintar degradês aqui
 *  sugeriria uma intensidade que não existe.
 */

const LADO = 11;
const VAO = 3;
const PASSO = LADO + VAO;
const ALTURA_DO_CABECALHO = 16;
const DIAS = 182;

const MESES = ["jan", "fev", "mar", "abr", "mai", "jun",
               "jul", "ago", "set", "out", "nov", "dez"];

interface Celula {
  iso: string;
  data: Date;
  semana: number;
  diaDaSemana: number;
  praticou: boolean;
}

function montarCelulas(praticados: Set<string>): Celula[] {
  const hoje = new Date();
  hoje.setHours(12, 0, 0, 0);

  const inicio = new Date(hoje);
  inicio.setDate(inicio.getDate() - (DIAS - 1));
  // Recua até o domingo, para cada coluna ser uma semana inteira.
  inicio.setDate(inicio.getDate() - inicio.getDay());

  const celulas: Celula[] = [];
  const cursor = new Date(inicio);
  let semana = 0;

  while (cursor <= hoje) {
    const iso = [
      cursor.getFullYear(),
      String(cursor.getMonth() + 1).padStart(2, "0"),
      String(cursor.getDate()).padStart(2, "0"),
    ].join("-");

    celulas.push({
      iso,
      data: new Date(cursor),
      semana,
      diaDaSemana: cursor.getDay(),
      praticou: praticados.has(iso),
    });

    if (cursor.getDay() === 6) semana += 1;
    cursor.setDate(cursor.getDate() + 1);
  }
  return celulas;
}

export function CalendarioDePratica({ dias }: { dias: string[] }) {
  const celulas = montarCelulas(new Set(dias));
  const semanas = Math.max(...celulas.map((c) => c.semana)) + 1;
  const largura = semanas * PASSO;
  const altura = ALTURA_DO_CABECALHO + 7 * PASSO;

  // Um rótulo de mês na primeira semana em que ele aparece.
  const marcosDeMes: { semana: number; texto: string }[] = [];
  let mesAnterior = -1;
  for (const celula of celulas) {
    const mes = celula.data.getMonth();
    if (mes !== mesAnterior && celula.diaDaSemana === 0) {
      marcosDeMes.push({ semana: celula.semana, texto: MESES[mes] });
      mesAnterior = mes;
    }
  }

  return (
    <div className="grafico">
      <h3 className="grafico-titulo">Dias praticados</h3>
      <p className="grafico-nota">
        {dias.length} {dias.length === 1 ? "dia" : "dias"} nos últimos seis meses
      </p>
      <div className="calendario-rolagem">
        <svg
          viewBox={`0 0 ${largura} ${altura}`}
          width={largura}
          height={altura}
          className="svg-calendario"
          role="img"
          aria-label={`Calendário de prática: ${dias.length} dias praticados nos últimos seis meses`}
        >
          {marcosDeMes.map((marco) => (
            <text
              key={`${marco.texto}-${marco.semana}`}
              x={marco.semana * PASSO}
              y={11}
              className="rotulo-eixo"
            >
              {marco.texto}
            </text>
          ))}
          {celulas.map((celula) => (
            <rect
              key={celula.iso}
              x={celula.semana * PASSO}
              y={ALTURA_DO_CABECALHO + celula.diaDaSemana * PASSO}
              width={LADO}
              height={LADO}
              rx="2"
              className={celula.praticou ? "dia praticou" : "dia"}
            >
              <title>
                {celula.data.toLocaleDateString("pt-BR")} —{" "}
                {celula.praticou ? "praticou" : "sem prática"}
              </title>
            </rect>
          ))}
        </svg>
      </div>
      <p className="legenda-do-calendario">
        <span className="amostra" /> praticou
        <span className="amostra vazio" /> não praticou
      </p>
    </div>
  );
}
