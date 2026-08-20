/* META
{
  "id": "C01-001",
  "titulo": "Clientes de São Paulo",
  "nivel": 1,
  "tempo_min": 6,
  "tags": [
    "select",
    "where",
    "order-by",
    "limit"
  ],
  "dicas": [
    "São quatro cláusulas, nesta ordem: SELECT, FROM, WHERE, ORDER BY, LIMIT.",
    "Texto em SQL vai entre aspas simples: uf = 'SP'.",
    "SELECT cliente_id, nome, cidade FROM clientes WHERE ... ORDER BY ... LIMIT 10;"
  ]
}
*/
/* ENUNCIADO
Liste os clientes do estado de São Paulo.

Devolva as colunas `cliente_id`, `nome` e `cidade`, apenas das linhas
em que a `uf` é `SP`, ordenadas por `cliente_id` crescente, e traga
só os **10 primeiros**.

As colunas precisam sair nessa ordem e com esses nomes.
*/

-- O LIMIT age por último — depois do ORDER BY —, então são os 10 menores cliente_id.
SELECT cliente_id, nome, cidade
FROM clientes
WHERE uf = 'SP'
ORDER BY cliente_id
LIMIT 10;
