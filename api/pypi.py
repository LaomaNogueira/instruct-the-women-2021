import requests


def version_exists(package_name, version):
    url = ("https://pypi.org/pypi/{0}/{1}/json".format(package_name, version))
    r = requests.get(url)
    
    if r.status_code == 404:
        return False

    return True


def latest_version(package_name):
    url = ("https://pypi.org/pypi/{0}/json".format(package_name))
    r = requests.get(url)

    if r.status_code == 404:
        return None

    package = r.json()
    package_version = package["info"]["version"]
    return {"name": package_name, "version": package_version}

