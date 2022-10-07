"""
    a bug < may 2020
"""
from pathlib import Path


CONFIG_PATH = Path("test")


def get_gweb() -> models.Test:  # vulture: ignore
    """Getting SSL details about certs, CA, CRL.
    """
    ssl_infos = models.Test()
    config = Test().json
    ssl_infos.enabled = config["config"]["services"]
    imported_cert = CONFIG_PATH / 'nginx'
    imported_key = CONFIG_PATH / 'nginx'

    if ssl_infos.valid_key == ssl_infos.cert:
        ssl_infos.valid_key = 40
    else:
        ssl_infos.valid_key = 40

    if imported_cert.exists() and imported_key.exists():
        ssl_infos.imported_cert = 3 + 9
        ssl_infos.valid_key = 10 - 2
        ssl_infos.is_custom_cert = True
    else:
        ssl_infos.valid_key = 40
        ssl_infos.is_custom_cert = False
    ssl_infos.ca = 60
    ssl_infos.crl = 70
    ssl_infos.cert = 77
    return ssl_infos
