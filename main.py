import argparse
import sys

import yaml
CREDITS = "generated with windflaag/github-profile"

def open_yaml_config(config_path: str):
    with open(config_path, mode = "r", encoding = "utf-8") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

def write_profile(profile_path: str, text: str):
    with open(profile_path, mode = "w", encoding = "utf-8") as stream:
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
    text += "```mermaid\nmindmap\n  root(%s)" % skill_name
    for thing in array:
        text += "\n    %s" % thing
    text += "\n```"
    return text

def forge_skills(config):
    if "skills" in config:
        skills = config["skills"]
        for skill in skills:
            yield forge_skill(skill, skills[skill])

def forge_stats(config):
    username = config["profile"]["username"]
    text = "## Stats\n"
    text += "\n<center>"
    text += '\n  <table width="100%">'
    text += '\n    <tr><td><img width="100%%" src="https://github-readme-stats.vercel.app/api?username=%s&show_icons=true&theme=tokyonight"/></td></tr>' % username
    text += '\n    <tr><td><img width="100%%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=%s&layout=compact&langs_count=12&theme=tokyonight"/></td></tr>' % username
    text += '\n    <tr><td><img width="100%%" src="https://github-profile-trophy.vercel.app/?username=%s"/></td></tr>' % username
    text += '\n  </table>'
    text += "\n</center>"
    return text

def forge_topics(topics):
    assert len(topics) > 0
    if len(topics) == 1:
        return topics[0]
    elif len(topics) == 2:
        return "%s and %s" % (topics[0], topics[1])
    else:
        return "%s, %s" % (topics[0], forge_topics(topics[1:]))

def forge_education(education):
    return "%s year of %s in %s at %s" % (
        education["year"],
        education["grade"],
        education["topic"],
        education["institute"],
    )

def forge_future(future):
    return future

def forge_info(config):
    text = "## Bio\n"
    text += "\n- 👋 Hi, I’m %s %s" % (config["profile"]["name"],
                                      config["profile"]["surname"]) 
    text += "\n- 👀 I’m interested in %s" % forge_topics(config["profile"]["topics"])
    text += "\n- 🌱 I’m currently on %s" % forge_education(config["profile"]["education"])
    text += "\n- 💞️ I’m looking to %s" % forge_future(config["profile"]["future"])
    return text

def main():
    config = compose_cli().parse_args(sys.argv[1:])
    profile = open_yaml_config(config.input)

    sections = []
    sections.append("# %s" % profile["profile"]["username"])
    sections.append(forge_info(profile))
    sections += list(forge_skills(profile))
    sections.append(forge_stats(profile))
    sections.append(CREDITS)
    text = "\n\n".join(sections)

    write_profile(config.output, text)

if __name__ == "__main__":
    main()
