from __future__ import print_function

import os

from vswmc.cli import utils


def add_metadata(metadata, entry):
    if "=" not in entry:
        raise Exception("Invalid metadata '{}'. Use format 'key=value'".format(entry))

    key, value = entry.split("=")
    metadata[key] = value


def list_(args):
    client = utils.create_client(args)

    rows = [["ID", "TYPE", "RUN", "USAGE"]]
    for product in client.list_products(type=args.type, run=args.run):
        run = None
        if product.get("run"):
            run = (
                product["run"]["simulation"]["name"]
                + " #"
                + str(product["run"]["counter"])
            )
        rows.append(
            [
                product["_id"],
                product["type"],
                run,
                product["remoteDiskUsage"],
            ]
        )
    utils.print_table(rows)


def describe(args):
    client = utils.create_client(args)
    product = client.get_product(args.product)

    if product["metadata"]:
        print("Metadata:")
        for item in product["metadata"].items():
            print(" - " + item[0] + ": " + item[1])
    else:
        print("Metadata: None")

    print("Remote File Count:", product["remoteFileCount"])
    print("Remote Disk Usage:", product["remoteDiskUsage"])
    if product["remoteFiles"]:
        print("Remote Files:")
        for item in product["remoteFiles"]:
            print(" - " + item)
    else:
        print("Remote Files: None")


def create(args):
    metadata = {}
    if args.metadata_file:
        with open(args.metadata_file, "rb") as f:
            for entry in f.readlines():
                entry = entry.strip()
                if entry and not entry.startswith("#"):
                    add_metadata(metadata, entry)

    for metadata_arg in args.metadata or []:
        for entry in metadata_arg:
            add_metadata(metadata, entry)

    client = utils.create_client(args)
    uploads = []
    for attachments in args.attach or []:
        for attachment in attachments:
            path = os.path.expanduser(attachment)
            with open(path, "rb") as f:
                name = os.path.basename(path)
                upload = client.upload_file(f, name)
                uploads.append(upload)

    result = client.create_product(args.type, metadata, uploads)
    errors = result.get("errors", [])
    if errors:
        for error in errors:
            print("Error:", error)
    else:
        print(result["product"]["_id"])


def configure_parser(parser):
    subparsers = parser.add_subparsers(title="Commands", metavar="COMMAND")
    subparsers.required = True

    subparser = subparsers.add_parser("list", help="List products")
    subparser.set_defaults(func=list_)
    subparser.add_argument("--type", type=str, help="Filter by type")
    subparser.add_argument("--run", type=str, help="Filter on run")

    subparser = subparsers.add_parser("describe", help="Describe a product")
    subparser.add_argument(
        "product", metavar="PRODUCT", help="ID of the product to describe"
    )
    subparser.set_defaults(func=describe)

    subparser = subparsers.add_parser("create", help="Create a product")
    subparser.add_argument("type", metavar="TYPE", help="Product type")
    subparser.add_argument("--metadata-file", help="Read metadata from a file")
    subparser.add_argument(
        "--metadata",
        metavar="PARAM=VALUE",
        action="append",
        nargs="+",
        help="Set metadata",
    )
    subparser.add_argument(
        "--attach",
        metavar="FILE",
        action="append",
        nargs="+",
        help="Add file attachment",
    )
    subparser.set_defaults(func=create)
