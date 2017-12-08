### CLI with data analysis of the game Cartola FC

#### Instalação

```
pip install cartola-stats-cli
```

#### Documentação

  - ```-t10, --top10```: Lista um TOP 10 com os maiores pontuadores:
  	- Ex: ```$ cartola-stats-cli -t10```

  - ```-bop, --bestofposition```: Recebe um argumento (a posição) e retorna o jogador que mais pontuou naquela determina posição (Goleiro, Zagueiro, Lateral, Meia, Atacante, Técnico):
  	- Ex: ```$ cartola-stats-cli -bop Lateral``` ou ```$ cartola-stats-cli -bop Atacante```

  - ```-tp, --tposition```: Lista os jogadores que mais pontuarem de cada posição:
  	- Ex: ```$ cartola-stats-cli -tp```