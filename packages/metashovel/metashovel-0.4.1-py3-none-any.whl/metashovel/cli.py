import json
import logging

import click

from .client import Client
from .metabase_io import MetabaseIO, broken_cards, broken_dashboards, broken_datamodel
from .splitter import Splitter


@click.group()
def cli():
    pass


@cli.command("export")
@click.option("-c", "--collection", help="Name of the collection to export")
@click.option("-j", "--json-file", default=None, help="path to JSON file to import")
@click.option(
    "-y", "--yaml-dir", default=None, help="path to directory with yaml files"
)
@click.option("-v", "--verbose", is_flag=True, default=False, help="More logging")
def metabase_export(collection, json_file, yaml_dir, verbose):
    set_verbose(verbose)
    client = Client()
    mio = MetabaseIO(client)
    result = mio.export_json(collection)
    if json_file:
        with open(json_file, "w") as out:
            out.write(json.dumps(result, indent=2, sort_keys=True))
    if yaml_dir:
        splitter = Splitter(yaml_dir)
        splitter.store(result)
    if not (json_file or yaml_dir):
        print(json.dumps(result, indent=2, sort_keys=True))


@cli.command("import")
@click.option("-c", "--collection", help="Name of the collection to import into")
@click.option("-j", "--json-file", default=None, help="path to JSON file to import")
@click.option(
    "-y", "--yaml-dir", default=None, help="path to directory with yaml files"
)
@click.option(
    "-m",
    "--metadata",
    is_flag=True,
    help="Also import metadata before importing the collection",
)
@click.option("-o", "--overwrite", is_flag=True, help="Overwrite cards")
@click.option(
    "-D", "--db-map", multiple=True, help="Map Metabase database names fromname:toname."
)
@click.option("-V", "--validate", is_flag=True, help="Validate JSON before load")
@click.option("-v", "--verbose", is_flag=True, default=False, help="More logging")
def metabase_import(
    collection, json_file, metadata, overwrite, db_map, validate, yaml_dir, verbose
):
    set_verbose(verbose)
    client = Client()
    mio = MetabaseIO(client)
    db_mapping = {d1: d2 for (d1, d2) in map(lambda x: x.split(":"), db_map)}
    if json_file:
        with open(json_file, "r") as f:
            source = json.loads(f.read())
    elif yaml_dir:
        splitter = Splitter(yaml_dir)
        source = splitter.load()
    else:
        raise click.Abort(
            "You need to specify json file with -j or yaml directory with -y"
        )

    if validate:
        if verbose:
            click.echo("🔍 Validating import file coherence...")
        bcards = broken_cards(source["items"], source["datamodel"])
        if len(bcards) > 0:
            print("There are broken cards:")
            for bc in bcards:
                print("{}: {}".format(*bc))

        bdashboards = broken_dashboards(source["items"])
        if len(bdashboards) > 0:
            print(
                "There are broken dashboards (with questions outside of imported collection):"
            )
            for bd in bdashboards:
                print("{}: {} (missing card id {})".format(*bd))

        bdatamodel = broken_datamodel(source["datamodel"])
        if len(bdatamodel) > 0:
            print("This is broken in the data model:")
            for bd in bdatamodel:
                print("{}: {} - {}".format(*bd))

        if len(bcards) > 0 or len(bdashboards) > 0 or len(bdatamodel) > 0:
            return 1

    mio.import_json(source, collection, metadata, overwrite, db_mapping)


@cli.command("query")
@click.option(
    "-j", "--json", is_flag=True, default=False, help="Print in JSON instead of Python"
)
@click.argument("model")
@click.argument("oid", default=None, required=False)
@click.argument("sub", default=None, required=False)
def metabase_query(model, oid, sub, **opts):
    from pprint import pprint

    client = Client()

    r = client.get(model, oid, sub)

    if opts["json"]:
        print(json.dumps(r, indent=2))
    else:
        pprint(r)


@cli.command("scroll", context_settings={"ignore_unknown_options": True})
@click.argument("dashboard_id", required=True)
@click.option("-i", "--increment", help="move to apply to all cards")
@click.option(
    "-c", "--clear", help="Area to clear, in the format x,y:WxH"
)
def metabase_scroll(dashboard_id, **opts):
    client = Client()
    dashboard = client.get("dashboard", dashboard_id)
    cards = []

    if opts["clear"]:
        coord, size = opts["clear"].split(":")
        x, y = map(int, coord.split(","))
        w, h = map(int, size.split("x"))
        def intersects(card):
            return not((card["col"] + card["sizeX"] <= x) or (card["row"] + card["sizeY"] <= y) or (card["col"] >= x + w) or (card["row"] >= y + h))
        intersex = list(map(lambda c: c["row"], filter(intersects, dashboard["ordered_cards"])))
        if len(intersex) > 0:
            minx = min(intersex)
            increment = h + max(0, x - minx)
            def should_move(card):
                return (card["row"] >= minx)
        else:
            def should_move(card):
                return False
    else:
        increment = int(opts["increment"])
        def should_move(card):
            return True

    def move_card(row, increment):
        return max(0, row + increment)

    for card in dashboard["ordered_cards"]:
        card = {
            k: card[k]
            for k in card.keys()
            & [
                "id",
                "card_id",
                "parameter_mappings",
                "series",
                "row",
                "col",
                "sizeX",
                "sizeY",
                "visualization_settings",
            ]
        }
        if should_move(card):
            card["row"] = move_card(card["row"], increment)
        cards.append(card)

    client.update_dashboard_cards(cards, dashboard_id)


@cli.command("split")
@click.option("-j", "--json-file", help="path to JSON file to import")
@click.option("-y", "--yaml-dir", help="path to directory with yaml files")
def metabase_split(json_file, yaml_dir):
    data = json.load(open(json_file))
    splitter = Splitter(yaml_dir)
    splitter.store(data)


@cli.command("join")
@click.option("-j", "--json-file", default=None, help="path to JSON file to import")
@click.option("-y", "--yaml-dir", help="path to directory with yaml files")
def metabase_join(json_file, yaml_dir):
    splitter = Splitter(yaml_dir)
    data = splitter.load()
    if json_file:
        with open(json_file, "w") as out:
            out.write(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(json.dumps(data, indent=2, sort_keys=True))


def set_verbose(verbose):
    if verbose:
        logging.basicConfig()
        logging.getLogger("metabase.io").setLevel(logging.INFO)
