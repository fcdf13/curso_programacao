/* META
{
  "id": "C01-002",
  "titulo": "Os cinco produtos mais caros",
  "nivel": 2,
  "tempo_min": 7,
  "tags": [
    "select",
    "alias",
    "order-by",
    "desc"
  ],
  "requer": [
    "C01-001"
  ],
  "dicas": [
    "AS dá um apelido à coluna: SELECT nome AS produto.",
    "Para ordenar do maior para o menor, use ORDER BY preco DESC.",
    "WHERE ativo filtra os ativos; LIMIT 5 corta no fim."
  ]
}
*/
/* ENUNCIADO
Monte a vitrine dos produtos mais caros que ainda estão à venda.

Traga os **5 produtos ativos de maior preço**, com duas colunas:

    produto        o nome do produto
    preco_atual    o preço

Ou seja: as colunas `nome` e `preco` precisam sair **renomeadas** com
`AS`. Ordene do mais caro para o mais barato.

A coluna `ativo` já é booleana — `WHERE ativo` basta, sem `= true`.
*/

-- O ORDER BY pode usar a coluna original (preco) mesmo com o apelido no SELECT.
SELECT nome AS produto, preco AS preco_atual
FROM produtos
WHERE ativo
ORDER BY preco DESC
LIMIT 5;
