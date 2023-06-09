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

def write_profile(profile_path: str, text: str):
    with open(profile_path, "w") as stream:
        try:
            stream.write(text)
        except Exception as exc:
            print(exc)
            exit(1)

def compose_cli() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description = "github profile generator")
    cli.add_argument("-i", "--input", default="config.yml", help="input yaml config file")
    cli.add_argument("-o", "--output", default="output.md", help="ouput MD profile file")
    return cli

def forge_skill(skill_name, array):
    text = "## %s\n\n" % skill_name
    text += "```mermaid\nmindmap\n\troot(mindmap)"
    for thing in array:
        text += "\n    \"%s\"" % thing
    text += "```"
    return text

def forge_skills(config):
    if "skills" in config:
        skills = config["skills"]
        for skill in skills:
            yield forge_skill(skill, skills[skill])

def main():
    config = compose_cli().parse_args(sys.argv[1:])
    profile = open_yaml_config(config.input)

    sections = []
    sections += list(forge_skills(profile))
    text = "\n\n".join(sections)

    write_profile(config.output, text)

if __name__ == "__main__":
    main()
