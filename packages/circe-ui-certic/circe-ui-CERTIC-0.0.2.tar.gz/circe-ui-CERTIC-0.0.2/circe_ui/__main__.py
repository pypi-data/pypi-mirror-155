import argh
from circe_ui import serve


def run_cli():
    parser = argh.ArghParser()
    parser.add_commands([serve])
    parser.set_default_command(serve)
    parser.dispatch()


if __name__ == "__main__":
    run_cli()
