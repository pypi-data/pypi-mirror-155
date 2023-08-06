import pytest
from spam.enviador_de_email import Enviador  # no vscode e no escopo do projeto / onde ta o workflow
from spam.enviador_de_email import EmailInvalido

def test_criar_enviador_de_email():
    enviador = Enviador()
    assert enviador is not None

@pytest.mark.parametrize( #sempre coloca o parametro que quer usar ou seja no caso é destinatario
    'destinatario',
    ['bielouco17@hotmail.com', 'gabrielcunha.space@gmail.com'] # e depois coloque uma lista 
)
def test_remetente(destinatario):
    enviador = Enviador()
    resultado = enviador.enviar(
        destinatario,
        'ghcweb@hotmail.com',
        'Teste email',
        'Olá isso é um teste'
    )
    assert destinatario in resultado


@pytest.mark.parametrize( 
    'remetente',
    ['', 'gabrielcunha.space'] 
)
def test_remetente_invalido(remetente):
    enviador = Enviador()
    with pytest.raises(EmailInvalido):
        enviador.enviar(
            remetente,
            'ghcweb@hotmail.com',
            'Teste email',
            'Olá isso é um teste'
        )
    