import sys
import click
import yaml
import subprocess
import base64
import pathlib
from yaml.error import YAMLError

from k3sconfig import __version__


@click.command()
@click.version_option(__version__)
@click.option("--k3s-host", "-h")
@click.option("--name", "-n")
@click.argument(
    "config_path", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path)
)
def cli(k3s_host, name, config_path):
    with config_path.open() as f:
        try:
            config = yaml.safe_load(f.read())
        except YAMLError:
            click.secho("File is not in yaml format", err=True, color="red")
            sys.exit(1)

    try:
        ca_data = config["clusters"][0]["cluster"]["certificate-authority-data"]
        cert_data = config["users"][0]["user"]["client-certificate-data"]
        key_data = config["users"][0]["user"]["client-key-data"]
    except KeyError:
        click.secho("File is not a kubeconfig", err=True, color="red")
        sys.exit(1)

    for path, data in [
        ("/tmp/ca.pem", ca_data),
        ("/tmp/cert.pem", cert_data),
        ("/tmp/key.pem", key_data),
    ]:
        with open(path, "w") as fh:
            fh.write(base64.decodebytes(data.encode("utf-8")).decode("utf-8"))

    subprocess.run(
        [
            "kubectl",
            "config",
            "set-cluster",
            name,
            "--certificate-authority=/tmp/ca.pem",
            "--embed-certs=true",
            f"--server={k3s_host}",
        ],
        check=True,
    )
    subprocess.run(
        [
            "kubectl",
            "config",
            "set-credentials",
            name,
            "--client-certificate=/tmp/cert.pem",
            "--client-key=/tmp/key.pem",
            "--embed-certs=true",
        ],
        check=True,
    )
    subprocess.run(
        [
            "kubectl",
            "config",
            "set-context",
            name,
            f"--cluster={name}",
            f"--user={name}",
        ],
        check=True,
    )
