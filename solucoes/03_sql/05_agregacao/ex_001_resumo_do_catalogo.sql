/* META
{
  "id": "C05-001",
  "titulo": "Resumo do catálogo",
  "nivel": 2,
  "tempo_min": 8,
  "tags": [
    "agregacao",
    "count",
    "avg",
    "min-max"
  ],
  "dicas": [
    "São quatro funções de agregação num SELECT só, separadas por vírgula.",
    "Contar valores diferentes é COUNT(DISTINCT coluna).",
    "SELECT COUNT(*) AS total_produtos, COUNT(DISTINCT categoria) AS categorias, ..."
  ]
}
*/
/* ENUNCIADO
Monte o resumo do catálogo inteiro, em **uma única linha**, com quatro
colunas nesta ordem e com estes nomes:

    total_produtos    quantos produtos existem
    categorias        quantas categorias diferentes existem
    preco_medio       o preço médio (sem arredondar)
    preco_maximo      o preço mais alto

Considere todos os produtos, ativos ou não.

Duas coisas para prestar atenção: `categorias` pede valores **distintos**,
e `preco_medio` não deve ser arredondado — arredondamento em SQL tem
pegadinhas de dialeto que ficam para um módulo mais à frente.
*/

-- Sem GROUP BY, as agregações espremem a tabela inteira numa linha só.
SELECT
    COUNT(*)                    AS total_produtos,
    COUNT(DISTINCT categoria)   AS categorias,
    AVG(preco)                  AS preco_medio,
    MAX(preco)                  AS preco_maximo
FROM produtos;
