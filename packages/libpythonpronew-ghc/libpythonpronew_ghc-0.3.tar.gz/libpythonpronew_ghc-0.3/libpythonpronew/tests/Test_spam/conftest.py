import pytest
from spam.db import Conexao


@pytest.fixture(scope='session') #neste modo esta fixture executará apenas 1 vez p/ os dois testes.No session é o mesmo porem pra todos os testes que chama sessão como parametro.
def conexao():
    #setup
    conexao_obj = Conexao()
    yield conexao_obj # yield -> Função geradora é uma função que retorna mais do que um valor - retorna uma série de valores.
    #tear Down
    conexao_obj.fechar()

@pytest.fixture # pode depender de outra fixture 
def sessao(conexao):
    sessao_obj = sessao = conexao.gerar_sessao()
    yield sessao_obj
    sessao_obj.roll_back()
    sessao_obj.fechar()

    
#o conftest libera todas as fixures para os modulos dentro da pasta onde coloca.