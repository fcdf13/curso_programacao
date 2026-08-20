/** As dicas já liberadas, uma abaixo da outra. */

interface Props {
  dicas: string[];
  total: number;
  onPedir: () => void;
  ocupado?: boolean;
}

export function Dicas({ dicas, total, onPedir, ocupado }: Props) {
  const restantes = total - dicas.length;
  if (total === 0) return null;

  return (
    <section className="dicas">
      {dicas.map((texto, i) => (
        <div key={i} className="dica">
          <span className="dica-numero">dica {i + 1}</span>
          <p>{texto}</p>
        </div>
      ))}
      {restantes > 0 ? (
        <button onClick={onPedir} disabled={ocupado} className="pedir-dica">
          {dicas.length === 0 ? "Pedir uma dica" : "Mais uma dica"}
          <span className="fraco"> · {restantes} de {total}</span>
        </button>
      ) : (
        <p className="fraco">Todas as {total} dicas já foram liberadas.</p>
      )}
    </section>
  );
}
