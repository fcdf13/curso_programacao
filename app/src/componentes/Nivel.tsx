/** As bolinhas de dificuldade, iguais às do CLI. */

const COR = ["", "var(--nivel-1)", "var(--nivel-1)", "var(--nivel-3)",
             "var(--nivel-5)", "var(--nivel-5)"];

export function Nivel({ nivel }: { nivel: number }) {
  return (
    <span
      className="nivel"
      style={{ color: COR[nivel] ?? "var(--texto-fraco)" }}
      title={`nível ${nivel} de 5`}
      aria-label={`nível ${nivel} de 5`}
    >
      {"●".repeat(nivel)}
      <span className="vazias">{"○".repeat(5 - nivel)}</span>
    </span>
  );
}
