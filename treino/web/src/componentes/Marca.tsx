/** O monograma JF: arco vermelho aberto com as iniciais por cima.
 *
 *  É o mesmo desenho do ícone do PWA (`gerar-icones.py`), em SVG para
 *  acompanhar o tema e não borrar em tela de alta densidade.
 */

export function Marca({ tamanho = 30 }: { tamanho?: number }) {
  return (
    <svg
      width={tamanho}
      height={tamanho}
      viewBox="0 0 100 100"
      role="img"
      aria-label="João Filho Treinador"
      focusable="false"
    >
      {/* Arco de 300°: a abertura no canto superior direito é o gesto do logo. */}
      <path
        d="M 76.6 26.7 A 35 35 0 1 0 85 50"
        fill="none"
        stroke="var(--sangue)"
        strokeWidth="7"
        strokeLinecap="butt"
      />
      <text
        x="50"
        y="50"
        textAnchor="middle"
        dominantBaseline="central"
        fill="var(--texto)"
        fontFamily="var(--fonte-titulo)"
        fontSize="42"
        fontWeight="800"
        fontStyle="italic"
        letterSpacing="-2"
      >
        JF
      </text>
    </svg>
  );
}
