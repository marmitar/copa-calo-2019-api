from enum import Enum, unique
from app.tracks.track import Track


@unique
class Sex(Enum):
    female = 'feminino'
    male = 'masculino'


@unique
class Status(Enum):
    not_started = 'começar'
    started = 'acontecendo'
    ended = 'acabou'


@unique
class TrackType(Enum):
    cem_m = Track('100 metros')
    quatrocentos_m = Track('400 metros')
    oitocentos_m = Track('800 metros')
    quatro_cem_m = Track('4 x 100 metros')
    mil_quinhentos_m = Track('1500 metros')
    salto_distancia = Track('Salto em Distância')
    salto_altura = Track('Salto em Altura')
    arremesso_peso = Track('Arremesso de Peso')
