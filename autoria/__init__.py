"""Fonte de autoria dos exercícios.

Escrever 500 exercícios à mão em três árvores paralelas (enunciado, teste, gabarito)
é como o material fica inconsistente: um exercício ganha dicas, outro não; um teste usa
`verificar`, outro usa `assert`. Aqui cada exercício é declarado **uma vez**, num objeto
`Exercicio`, e `construir.py` materializa os três arquivos.

Para produzir o material:

    python -m autoria.construir

Editar um exercício significa editar o módulo de autoria correspondente
(`autoria/bloco_a.py`, etc.) e rodar o comando de novo.
"""
