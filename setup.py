from setuptools import setup

setup(
    name='cartola-stats-cli',
    version='0.1.0',
    url='https://github.com/werberth/cartola-fc-stats',
    license='MIT License',
    author='werberth Vinícius',
    author_email='werberth@gmail.com',
    keywords='cartola-fc cartola football fantasy data analysis pandas',
    description='CLI with data analysis of the game Cartola FC',
    packages=['cartolastats'],
    entry_points = {
        "console_scripts": ['cartola-stats-cli = cartolastats.cartolastats:main']
        },
    include_package_data=True,
    package_data={
        'cartolastats/cartola_csv': [
            'cartolastats/cartola_csv/2016_scouts.csv',
            'cartolastats/cartola_csv/2016_atletas.csv',
            'cartolastats/cartola_csv/posicoes.csv',
            'cartolastats/cartola_csv/2016_clubes.csv',  
        ],
    },
    data_files=[('cartolastats/cartola_csv', 
            [
                'cartolastats/cartola_csv/2016_scouts.csv',
                'cartolastats/cartola_csv/2016_atletas.csv',
                'cartolastats/cartola_csv/posicoes.csv',
                'cartolastats/cartola_csv/2016_clubes.csv',
            ]
        )
    ],
    install_requires=[
        'pandas',
    ],
)


