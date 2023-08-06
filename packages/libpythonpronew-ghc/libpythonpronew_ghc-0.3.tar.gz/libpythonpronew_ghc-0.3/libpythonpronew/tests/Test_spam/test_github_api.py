from libpythonpronew import github_api

def test_buscar_avatar():
   url = github_api.buscar_avatar('Gh-Cunha')
   assert 'https://avatars.githubusercontent.com/u/48072308?v=4' == url
