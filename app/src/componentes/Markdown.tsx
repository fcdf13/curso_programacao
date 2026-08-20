/** Enunciados e teoria são Markdown; blocos indentados viram exemplos de código. */

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function Markdown({ texto }: { texto: string }) {
  return (
    <div className="md">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{texto}</ReactMarkdown>
    </div>
  );
}
