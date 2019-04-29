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
    cem_m = Track('cem metros')
    quatrocentos_m = Track('quatrocentos metros')
    oitocentos_m = Track('oitocentos metros')
    quatro_cem_m = Track('quatro por cem metros')
    mil_quinhentos_m = Track('mil e quinhentos metros')
    salto_distancia = Track('salto em distância')
    salto_altura = Track('salto em altura')
    arremesso_peso = Track('arremesso de peso')
