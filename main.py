import argparse
import sys

import yaml

def open_yaml_config(config_path: str):
    with open(config_path, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

def compose_cli() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description = "github profile generator")
    cli.add_argument("-i", "--input", default="config.yml", help="input yaml config file")
    cli.add_argument("-o", "--output", default="output.md", help="ouput MD profile file")
    return cli

def main():
    cli_config = compose_cli().parse_args(sys.argv[1:])
    profile_config = open_yaml_config(cli_config.input)
    print(profile_config)

if __name__ == "__main__":
    main()
