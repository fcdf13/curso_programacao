"""Listas de nomes usadas pelo gerador. Ficam aqui só para não poluir gerar.py."""

PRIMEIROS_NOMES = [
    "Ana", "Beatriz", "Carla", "Daniela", "Eduarda", "Fernanda", "Gabriela",
    "Helena", "Isabela", "Juliana", "Larissa", "Mariana", "Natália", "Patrícia",
    "Rafaela", "Sofia", "Tatiana", "Vitória", "Camila", "Letícia", "Amanda",
    "André", "Bruno", "Carlos", "Daniel", "Eduardo", "Felipe", "Gustavo",
    "Henrique", "Igor", "João", "Lucas", "Marcelo", "Nelson", "Otávio",
    "Paulo", "Rafael", "Sérgio", "Thiago", "Vinícius", "Rodrigo", "Matheus",
    "Alice", "Benício", "Cecília", "Davi", "Elisa", "Théo", "Manuela", "Arthur",
]

SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves",
    "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho",
    "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa", "Rocha",
    "Dias", "Nascimento", "Andrade", "Moreira", "Nunes", "Marques", "Machado",
    "Mendes", "Freitas", "Cardoso", "Ramos", "Gonçalves", "Santana", "Teixeira",
]

# (sigla, cidade principal, peso populacional aproximado)
ESTADOS = [
    ("SP", "São Paulo", 22.0), ("MG", "Belo Horizonte", 10.5),
    ("RJ", "Rio de Janeiro", 8.5), ("BA", "Salvador", 7.0),
    ("PR", "Curitiba", 5.6), ("RS", "Porto Alegre", 5.4),
    ("PE", "Recife", 4.7), ("CE", "Fortaleza", 4.4),
    ("PA", "Belém", 4.1), ("SC", "Florianópolis", 3.7),
    ("GO", "Goiânia", 3.5), ("MA", "São Luís", 3.4),
    ("PB", "João Pessoa", 2.0), ("ES", "Vitória", 2.0),
    ("AM", "Manaus", 2.0), ("MT", "Cuiabá", 1.8),
    ("RN", "Natal", 1.7), ("PI", "Teresina", 1.6),
    ("AL", "Maceió", 1.6), ("DF", "Brasília", 1.5),
    ("MS", "Campo Grande", 1.4), ("SE", "Aracaju", 1.1),
    ("RO", "Porto Velho", 0.9), ("TO", "Palmas", 0.9),
    ("AC", "Rio Branco", 0.5), ("AP", "Macapá", 0.5),
    ("RR", "Boa Vista", 0.4),
]

PROVEDORES_DE_EMAIL = ["gmail.com", "hotmail.com", "outlook.com", "yahoo.com.br",
                       "uol.com.br", "terra.com.br", "icloud.com"]

CANAIS_DE_AQUISICAO = ["organico", "busca_paga", "indicacao", "redes_sociais", "email_mkt"]
PESOS_DE_AQUISICAO = [0.32, 0.26, 0.14, 0.20, 0.08]

# categoria -> (subcategorias, faixa de preço, faixa de peso em kg)
CATALOGO = {
    "Eletrônicos": (
        ["Celulares", "Notebooks", "Fones", "Acessórios", "TVs"],
        (89.0, 6500.0), (0.05, 18.0),
    ),
    "Casa": (
        ["Cozinha", "Decoração", "Cama e Banho", "Organização", "Jardim"],
        (19.9, 1200.0), (0.2, 25.0),
    ),
    "Moda": (
        ["Camisetas", "Calçados", "Bolsas", "Relógios", "Óculos"],
        (29.9, 890.0), (0.1, 2.5),
    ),
    "Esporte": (
        ["Corrida", "Musculação", "Ciclismo", "Natação", "Camping"],
        (24.9, 2400.0), (0.1, 30.0),
    ),
    "Livros": (
        ["Ficção", "Técnico", "Infantil", "Biografia", "Autoajuda"],
        (14.9, 220.0), (0.15, 1.8),
    ),
    "Beleza": (
        ["Cabelos", "Perfumes", "Maquiagem", "Skincare", "Barba"],
        (12.9, 480.0), (0.05, 1.2),
    ),
    "Alimentos": (
        ["Cafés", "Suplementos", "Doces", "Bebidas", "Mercearia"],
        (9.9, 320.0), (0.1, 6.0),
    ),
}

ADJETIVOS_DE_PRODUTO = [
    "Compacto", "Premium", "Clássico", "Ultra", "Essencial", "Pro", "Max",
    "Leve", "Reforçado", "Slim", "Duplo", "Portátil", "Smart", "Vintage",
]

LINHAS_DE_PRODUTO = ["Aurora", "Nimbus", "Vertex", "Lumen", "Órion", "Cobalto",
                     "Âmbar", "Zênite", "Praia", "Serra", "Atlas", "Duna"]

STATUS_DE_PEDIDO = ["entregue", "enviado", "processando", "cancelado", "devolvido"]
PESOS_DE_STATUS = [0.74, 0.09, 0.05, 0.08, 0.04]

CANAIS_DE_VENDA = ["site", "app", "marketplace", "telefone"]
PESOS_DE_CANAL = [0.44, 0.36, 0.17, 0.03]

CUPONS = ["BEMVINDO10", "FRETEGRATIS", "BLACK20", "VOLTEI15", "APP5", "INDICA25"]

METODOS_DE_PAGAMENTO = ["cartao_credito", "pix", "boleto", "cartao_debito"]
PESOS_DE_PAGAMENTO = [0.52, 0.31, 0.09, 0.08]

DISPOSITIVOS = ["mobile", "desktop", "tablet"]
PESOS_DE_DISPOSITIVO = [0.63, 0.32, 0.05]

# Funil de eventos: cada etapa só acontece se a anterior aconteceu.
ETAPAS_DO_FUNIL = ["visita", "ver_produto", "adicionar_carrinho",
                   "iniciar_checkout", "compra"]
RETENCAO_POR_ETAPA = [1.00, 0.62, 0.28, 0.16, 0.09]

COMENTARIOS_DE_AVALIACAO = [
    "Chegou antes do prazo, recomendo.", "Produto bom, embalagem amassada.",
    "Não era o que eu esperava.", "Excelente custo-benefício!",
    "Demorou demais para entregar.", "Perfeito, comprarei de novo.",
    "Veio com defeito, pedi troca.", "Qualidade acima da média.",
    "Preço justo pelo que entrega.", "Atendimento péssimo no suporte.",
    "", "   ", "Muito bom!!!", "ruim", "SUPEROU AS EXPECTATIVAS",
]
