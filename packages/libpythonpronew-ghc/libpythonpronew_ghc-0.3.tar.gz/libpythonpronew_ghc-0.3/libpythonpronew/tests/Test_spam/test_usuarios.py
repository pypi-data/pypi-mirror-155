from spam.modelos import Usuario



def test_salvar_usuario(sessao):
    usuario = Usuario(nome= 'Gabriel', email= 'ghcweb@hotmail.com')
    sessao.salvar(usuario)
    assert isinstance(usuario.id, int)
   
    


def test_listar_usuarios(sessao):
    usuarios = [Usuario(nome= 'Gabriel', email= 'ghcweb@hotmail.com'), 
    Usuario(nome= 'Henrique', email= 'bielouco17@hotmail.com')]
    for usuario in usuarios:
        sessao.salvar(usuario)
    assert usuarios == sessao.listar()
   