from unittest.mock import Mock
import pytest
from spam.enviador_de_email import Enviador
from spam.main import EnviadorDeSpam
from spam.modelos import Usuario



@pytest.mark.parametrize(
    'usuarios',
    [
        [
            Usuario(nome='Gabriel', email= 'ghcweb@hotmail.com'),
            Usuario(nome= 'Henrique', email= 'bielouco17@hotmail.com')
        ],
        [
            Usuario(nome= 'Henrique', email= 'bielouco17@hotmail.com')
        ]
    ]
)
def test_qde_de_spam(sessao, usuarios):
    for usuario in usuarios:
        sessao.salvar(usuario)
    enviador = Mock()
    envaidor_de_spam = EnviadorDeSpam(sessao,enviador)
    envaidor_de_spam.enviar_emails(
        'ghcweb@hotmail.com',
        'Teste email',
        'Olá isso é um teste'
    )
    assert len(usuarios) == enviador.enviar.call_count


def test_parametros_de_spam(sessao):
    usuario = Usuario(nome= 'Henrique', email= 'bielouco17@hotmail.com')
    sessao.salvar(usuario)
    enviador = Mock()
    envaidor_de_spam = EnviadorDeSpam(sessao,enviador)
    envaidor_de_spam.enviar_emails(
        'ghcweb@hotmail.com',
        'Teste email',
        'Olá isso é um teste'
    )
    enviador.enviar.assert_called_once_with == (
        'ghcweb@hotmail.com',
        'bielouco17@hotmail.com',
        'Teste email',
        'Olá isso é um teste'
    )