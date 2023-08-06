import argparse
import re
import sys
from typing import NamedTuple
from typing import Sequence
from typing import TextIO

__version__ = "0.1.2"
certificate_regex = r"(-----BEGIN CERTIFICATE-----\n[\s\S]*\n-----END CERTIFICATE-----)"


class Keys(NamedTuple):
    private_key: str
    certificate: str


def _retreive_keys(key: TextIO, cert: TextIO) -> Keys:
    cert_contents = cert.read()
    cert_groups = re.search(certificate_regex, cert_contents)

    if cert_groups:
        certificate = cert_groups.group(1)
    private_key = key.read()

    return Keys(private_key, certificate)


def certcv(key: TextIO, cert: TextIO, config: TextIO) -> None:
    keys = _retreive_keys(key, cert)

    cert_tags = "<cert>\n" f"{keys.certificate}\n" "</cert>"
    private_key_tags = "<key>\n" f"{keys.private_key}\n" "</key>"

    text = f"\n\n{cert_tags}\n\n{private_key_tags}"
    config.write(text)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="certcv",
        description="A copy/paster quick-tool for adding private keys and certificate keys to an openVPN configuration file.",
    )
    parser.add_argument(
        "--version",
        help="prints out the current version.",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--key", nargs=1, metavar="filename", required=True, help="required filename."
    )
    parser.add_argument(
        "--cert", nargs=1, metavar="filename", required=True, help="required filename."
    )
    parser.add_argument(
        "--config",
        nargs=1,
        metavar="filename",
        required=True,
        help="required filename.",
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        raise SystemExit()

    args = parser.parse_args(argv)

    with open(args.key[0], "r") as key_file, open(args.cert[0], "r") as cert_file, open(
        args.config[0], "a"
    ) as conf_file:
        certcv(key=key_file, cert=cert_file, config=conf_file)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
