import argparse
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

resultados = pd.read_csv(os.path.join(BASE_DIR, 'cartola_csv/2016_scouts.csv')).sort_index()
jogadores = pd.read_csv(os.path.join(BASE_DIR, 'cartola_csv/2016_atletas.csv')).sort_index()
posicoes = pd.read_csv(os.path.join(BASE_DIR, 'cartola_csv/posicoes.csv'))
clubes = pd.read_csv(os.path.join(BASE_DIR, 'cartola_csv/2016_clubes.csv'))

resultados.rename(columns={'pontos_num': 'pontuacao' , 'media_num': 'media',
                           'preco_num': 'preco', 'variacao_num': 'variacao'}, inplace=True)
jogadores.rename(columns={'id':'atleta_id','apelido': 'nome'}, inplace=True)
posicoes.rename(columns={'id': 'posicao_id', 'nome': 'posicao'}, inplace=True)
clubes.rename(columns={'id': 'clube_id', 'nome':'clube'}, inplace=True)

resultados = pd.merge(resultados, jogadores, on=["atleta_id", "clube_id"])
resultados = pd.merge(resultados, posicoes, on=["posicao_id"])
resultados = pd.merge(resultados, clubes, on=["clube_id"])


final = resultados[['nome', 'posicao', 'rodada', 'clube', 'participou', 'pontuacao',
       'media', 'preco', 'variacao']]

agrupamente_pontos= final.groupby(['posicao', 'nome', 'clube'], as_index=False)

resultado_final = agrupamente_pontos.pontuacao.sum()
resultado_final.rename(
    columns={
        'pontuacao': 'Pontuação total', 
        'nome': 'Nome', 
        'posicao': 'Posição', 
        'clube': 'Clube'
    }, 
    inplace=True
)


def max_for_position(position):
    all_position = resultado_final[resultado_final['Posição'] == position]
    player = all_position[all_position['Pontuação total'] == all_position['Pontuação total'].max()]
    return player


def header(title):
    print('\n%s' % ('*' * 100))
    print('%s %s' % (' ' * 20, title))
    print('%s\n' % ('*' * 100) )

def get_best_player_of(position):
    position = position.title() #capitalize the first letter
    consulta = posicoes[posicoes['posicao'].isin([position])]
    if consulta.posicao.any():
        player = max_for_position(position)
        header('Melhor %s de 2016' % position)
        print(player)
        print('\n%s\n' %('*' * 100))
    else:
        print('Invalid Position, Please Try Again.')


def top_for_position():
    header('Jogadores de cada posição que mais pontuaram no cartola de 2016')
    top_all_positions_player = [max_for_position(posicao) for posicao in posicoes['posicao']]
    resultado = pd.DataFrame()
    for i in range(0, len(top_all_positions_player)):
        resultado = resultado.append(top_all_positions_player[i])
    print(resultado)
    print('\n%s\n' %('*' * 100))

def top_all():
    header('TOP 10 dos jogadores que mais pontuaram no cartola de 2016')
    resultado = resultado_final.sort_values(by='Pontuação total', ascending=False)[:10]
    print(resultado)
    print('\n%s\n' %('*' * 100))

def main():
    parser = argparse.ArgumentParser(
        prog='Cartola_Stats',
        description='CLI with data analysis of the game Cartola FC.'
    )

    parser.add_argument(
        '-t10', '--top10',
        action='store_true',
        help="Listing of the best players of each position"
    )

    parser.add_argument(
        '-bop', '--bestofposition',
        type=str, 
        help="selecting the player of a certain position \
            that had the highest total score."
    )

    parser.add_argument(
        '-tp', '--tposition',
        action='store_true',
        help="List of the top 10 players in a given year"
    )

    args = parser.parse_args()

    if args.top10:
        top_all()
    elif args.tposition:
        top_for_position()
    elif args.bestofposition:
        get_best_player_of(args.bestofposition)
    else:
        print('Invalid command!')
