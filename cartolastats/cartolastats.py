from os import path
import argparse
import pandas as pd

BASE_DIR = path.dirname(path.realpath(__file__))


def header(title):
    '''Simple header'''
    print('\n%s' % ('*' * 100))
    print('%s %s' % (' ' * 20, title))
    print('%s\n' % ('*' * 100))


class CartolaStats:
    '''Calculates the final data and provide the reports'''

    def __init__(self):
        '''Load data and parse into resultado_final'''

        resultados = pd.read_csv(path.join(BASE_DIR,
                                           'cartola_csv/2016_scouts.csv'))
        jogadores = pd.read_csv(path.join(BASE_DIR,
                                          'cartola_csv/2016_atletas.csv'))
        clubes = pd.read_csv(path.join(BASE_DIR,
                                       'cartola_csv/2016_clubes.csv'))
        self.posicoes = pd.read_csv(path.join(BASE_DIR,
                                              'cartola_csv/posicoes.csv'))

        resultados.rename(columns={'pontos_num': 'pontuacao',
                                   'media_num': 'media',
                                   'preco_num': 'preco',
                                   'variacao_num': 'variacao'}, inplace=True)
        jogadores.rename(columns={'id': 'atleta_id',
                                  'apelido': 'nome'}, inplace=True)
        clubes.rename(columns={'id': 'clube_id',
                               'nome': 'clube'}, inplace=True)
        self.posicoes.rename(columns={'id': 'posicao_id',
                                      'nome': 'posicao'}, inplace=True)

        resultados = pd.merge(resultados, jogadores, on=["atleta_id", "clube_id"])
        resultados = pd.merge(resultados, clubes, on=["clube_id"])
        resultados = pd.merge(resultados, self.posicoes, on=["posicao_id"])

        final = resultados[['nome', 'posicao', 'rodada', 'clube', 'participou',
                            'pontuacao', 'media', 'preco', 'variacao']]

        agrupamente_pontos = final.groupby(['posicao', 'nome', 'clube'],
                                           as_index=False)

        self.resultado_final = agrupamente_pontos.pontuacao.sum()
        self.resultado_final.rename(
            columns={
                'pontuacao': 'Pontuação total',
                'nome': 'Nome',
                'posicao': 'Posição',
                'clube': 'Clube'
            },
            inplace=True
        )

    def max_for_position(self, position):
        '''Returns the best player for a given position'''
        all_position = self.resultado_final[self.resultado_final['Posição'] == position]
        player = all_position[all_position['Pontuação total'] == all_position['Pontuação total'].max()]
        return player


    def get_best_player_of(self, position):
        '''Prints the best player for a given position'''
        position = position.title() #capitalize the first letter
        consulta = self.posicoes[self.posicoes['posicao'].isin([position])]
        if consulta.posicao.any():
            player = self.max_for_position(position)
            header('Melhor %s de 2016' % position)
            print(player)
            print('\n%s\n' %('*' * 100))
        else:
            print('Invalid Position, Please Try Again.')
            print('Valid positions:', ' / '.join(self.posicoes['posicao']))


    def top_for_position(self):
        '''Returns the best player for each position'''
        header('Jogadores de cada posição que mais pontuaram no cartola de 2016')
        top_all_positions_player = [self.max_for_position(posicao) for posicao in self.posicoes['posicao']]
        resultado = pd.DataFrame()
        for i in range(0, len(top_all_positions_player)):
            resultado = resultado.append(top_all_positions_player[i])
        print(resultado)
        print('\n%s\n' % ('*' * 100))

    def top_all(self):
        '''Top 10 players of the 2016 season'''
        header('TOP 10 dos jogadores que mais pontuaram no cartola de 2016')
        resultado = self.resultado_final.sort_values(by='Pontuação total', ascending=False)[:10]
        print(resultado)
        print('\n%s\n' % ('*' * 100))


def main():
    parser = argparse.ArgumentParser(
        prog='Cartola_Stats',
        description='CLI with data analysis of the game Cartola FC.'
    )
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        '-t10', '--top10',
        action='store_true',
        help="Listing of the best players of each position"
    )

    group.add_argument(
        '-bop', '--bestofposition',
        type=str,
        help="selecting the player of a certain position \
            that had the highest total score."
    )

    group.add_argument(
        '-tp', '--tposition',
        action='store_true',
        help="List of the top 10 players in a given year"
    )

    args = parser.parse_args()
    stats = CartolaStats()

    if args.top10:
        stats.top_all()
    elif args.tposition:
        stats.top_for_position()
    elif args.bestofposition:
        stats.get_best_player_of(args.bestofposition)
    else:
        print('Invalid command!')
        parser.print_help()
