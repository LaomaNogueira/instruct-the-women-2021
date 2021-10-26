import requests

# Referências sobre o uso do requests:
#
# Fazendo requisições:
# https://docs.python-requests.org/en/master/user/quickstart/#make-a-request
# Usando JSON retornado:
# https://docs.python-requests.org/en/master/user/quickstart/#json-response-content


def version_exists(package_name, version):
    # TODO
    # Fazer requisição na API do PyPI para checar se a versão existe
    print('segundo_com versão')
    url = ('https://pypi.org/pypi/{0}/{1}/json'.format(package_name, version))
    r = requests.get(url)
    
    if r.status_code == 404:
        return False

    return True


def latest_version(package_name):
    # TODO
    # Fazer requisição na API do PyPI para descobrir a última versão
    # de um pacote. Retornar None se o pacote não existir.
    print('segundo_sem versão')
    url = ('https://pypi.org/pypi/{0}/json'.format(package_name))
    r = requests.get(url)

    if r.status_code == 404:
        return None

    package = r.json()
    
    package_version = package['info']['version']

    return {'name': package_name, 'version': package_version}

