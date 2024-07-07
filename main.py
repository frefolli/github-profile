import argparse
from io import StringIO
import sys
import yaml

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

def cli() -> argparse.Namespace:
  cli = argparse.ArgumentParser(description = "github profile generator")
  cli.add_argument("-i", "--input", default="config.yml", help="input yaml config file")
  cli.add_argument("-o", "--output", default="output.md", help="ouput MD profile file")
  return cli.parse_args(sys.argv[1:])

class Mermaid:
  def __init__(self, config: dict, root: str) -> None:
    self.config: dict = config
    self.root: str = root
    self.out: StringIO = StringIO()

  def process_subgraph(self, subgraph: dict|list, level: int) -> None:
    if isinstance(subgraph, dict):
      indent = "  " * level
      for key in subgraph:
        self.out.write("%s((%s))\n" % (indent, key))
        self.process_subgraph(subgraph[key], level + 1)
    elif isinstance(subgraph, list):
      indent = "  " * level
      for datum in subgraph:
        self.out.write("%s%s\n" % (indent, datum))
    else:
      raise ValueError("subgraph (%s) is not a dict nor a list" % subgraph)

  def process(self) -> str:
    self.out.write("```mermaid\n")
    self.out.write("mindmap\n")
    self.out.write("  root(%s)\n" % self.root)
    self.process_subgraph(self.config, 2)
    self.out.write("```\n")
    return self.out.getvalue()

class Processor:
  def __init__(self, config: dict) -> None:
    self.config: dict = config
    self.out: StringIO = StringIO()

  def process(self) -> str:
    self.process_profile()
    self.process_skills()
    self.process_projects()
    self.process_stats()
    return self.out.getvalue()

  def process_profile_intro(self) -> None:
    self.out.write("I'm %s %s, %s, from %s.\n\n" % (self.config["Profile"]["surname"], self.config["Profile"]["name"], self.config["Profile"]["age"], self.config["Profile"]["country"]))
    if "twinname" in self.config["Profile"]:
      self.out.write("My second Github account is [%s](https://github.com/%s)\n\n" % (
        self.config["Profile"]["twinname"],
        self.config["Profile"]["twinname"]
      ))

  def process_profile_interests(self) -> None:
    self.out.write("## Interests\n\n")
    self.out.write("%s\n\n" % Mermaid(self.config["Profile"]["Interests"], "Interests").process())

  def process_profile_education(self) -> None:
    self.out.write("## Education\n\n")
    if "Now" in self.config["Profile"]["Education"]:
      edu = self.config["Profile"]["Education"]["Now"]
      self.out.write("### %s\n\n" % (edu["grade"]))
      self.out.write("I'm currently studying for the %s year of %s in %s at %s\n\n" % (edu["year"], edu["grade"], edu["topic"], edu["institute"]))
    if "Olds" in self.config["Profile"]["Education"]:
      for edu in self.config["Profile"]["Education"]["Olds"]:
        self.out.write("### %s\n\n" % (edu["grade"]))
        self.out.write("I used to study %s in %s at %s.\n\n" % (edu["grade"], edu["topic"], edu["institute"]))
        self.out.write("My thesis was \"%s\"\n\n" % (edu["thesis"]))
        self.out.write("I graduated with %s out of %s\n\n" % (edu["mark"], edu["max_mark"]))

  def process_profile_jobs(self) -> None:
    self.out.write("## Jobs\n\n")
    if "Now" in self.config["Profile"]["Jobs"]:
      edu = self.config["Profile"]["Jobs"]["Now"]
      self.out.write("### %s\n\n" % (edu["profession"]))
      self.out.write("I'm currently working for %s as %s.\n\n" % (edu["place"], edu["profession"]))
      if "Contribution" in edu:
        self.out.write("Some notable contributions:\n\n")
        for contribution in edu["Contribution"]:
          self.out.write(" - %s\n" % (contribution))
        self.out.write("\n")
    if "Olds" in self.config["Profile"]["Jobs"]:
      for edu in self.config["Profile"]["Jobs"]["Olds"]:
        self.out.write("### %s\n\n" % (edu["profession"]))
        self.out.write("I used to work for %s as %s.\n\n" % (edu["place"], edu["profession"]))
        if "Contribution" in edu:
          self.out.write("Some notable contributions:\n\n")
          for contribution in edu["Contribution"]:
            self.out.write(" - %s\n" % (contribution))
          self.out.write("\n")

  def process_profile_future(self) -> None:
    self.out.write("## My Future\n\n")
    self.out.write("Here are some funny things I would like to do in the future:\n\n")
    for thing in self.config["Profile"]["Future"]:
      self.out.write(" - %s\n" % (thing))
    self.out.write("\n")

  def process_profile(self) -> None:
    self.out.write("# %s \n\n" % self.config["Profile"]["username"])
    self.process_profile_intro()
    self.process_profile_interests()
    self.process_profile_education()
    self.process_profile_jobs()
    self.process_profile_future()

  def process_skills(self) -> None:
    self.out.write("# Skills \n\n")
    for skill_name, skill_data in self.config["Skills"].items():
      self.out.write("## %s\n\n" % skill_name)
      self.out.write("%s\n\n" % Mermaid(skill_data, skill_name).process())

  def process_projects(self) -> None:
    self.out.write("# Projects \n\n")
    self.out.write("%s\n\n" % Mermaid(self.config["Projects"], "Projects").process())

  def process_stats(self) -> None:
    conf = (self.config.get("Stats") or {})
    stats = []
    if conf.get("timeline"):
      stats.append("    <tr><td><img width=\"100%%\" src=\"https://github-readme-stats.vercel.app/api?username=%s&show_icons=true&theme=tokyonight\"/></td></tr>\n" % (self.config["Profile"]["username"]))
    if conf.get("languages"):
      stats.append("    <tr><td><img width=\"100%%\" src=\"https://github-readme-stats.vercel.app/api/top-langs/?username=%s&layout=compact&langs_count=12&theme=tokyonight\"/></td></tr>\n" % (self.config["Profile"]["username"]))
    if conf.get("trophies"):
      stats.append("    <tr><td><img width=\"100%%\" src=\"https://github-profile-trophy.vercel.app/?username=%s\"/></td></tr>\n" % (self.config["Profile"]["username"]))

    if len(stats) > 0:
      self.out.write("# Stats \n\n")
      self.out.writelines([
        "<center>\n",
        "  <table width=\"100%\">\n"] + stats + [
        "  </table>\n",
        "</center>\n"
      ])
      self.out.write("\n\n")

if __name__ == "__main__":
  options = cli()
  config = open_yaml_config(options.input)
  profile = Processor(config).process()
  write_profile(options.output, profile)
