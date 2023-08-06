import requests


def buscar_avatar(nome_do_usuario):
    """
    busca o avatar de um usuario no github
    :param nome_do_usuario: str com o nome de usuario no github
    :return: str com o link do avatar
    """
    url = f'https://api.github.com/users/{nome_do_usuario}'
    resp = requests.get(url)
    return resp.json()['avatar_url']


if __name__ == '__main__':
    print(buscar_avatar('renzon'))
