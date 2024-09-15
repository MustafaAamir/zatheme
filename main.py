#!/usr/bin/python

import os
import sys
import json
from dataclasses import dataclass
import argparse

# json config
@dataclass
class ColourConfig:
    Page : str
    Text : str
    Background : str
    Highlight : str
    Highlight_active : str
    Error : str

# parsing args
def setDefaultConfig(filepath):
    try:
        file = open(filepath, "r")
        dc = open("defaultconfig", "w")
        dc.writelines(file.readlines())
        file.close()
        dc.close()
    except FileNotFoundError:
        print("config filepath cannot be resolved")

def defaultConfig():
    file = open("defaultconfig", "r")
    defaultconfig = file.readlines()
    file.close()
    return defaultconfig

def setTheme(filepath):
    try:
        json_data = open(filepath, "r")
        json_obj = json.load(json_data)
        json_data.close()
        try:
            currentColourConfig = ColourConfig(
                    Page = json_obj["page"],
                    Text = json_obj["text"],
                    Background = json_obj["background"],
                    Highlight = json_obj["highlight"],
                    Highlight_active = json_obj["highlight_active"],
                    Error = json_obj["error"]
                    )
            home = str(os.path.expanduser('~'))
            try:
                zathurarc = open(home + "/.config/zathura/zathurarc", "w")
                zathurarc.writelines(defaultConfig())
                zathurarc.write("# ----- colour config ----- \n")
                zathurarc.write("set notification-error-bg \"" + currentColourConfig.Background + "\"\n")
                zathurarc.write("set notification-error-fg \"" + currentColourConfig.Error + "\"\n")
                zathurarc.write("set notification-warning-bg \"" + currentColourConfig.Background + "\"\n")
                zathurarc.write("set notification-warning-fg \"" + currentColourConfig.Error + "\"\n")
                zathurarc.write("set notification-bg \"" + currentColourConfig.Background + "\"\n")
                zathurarc.write("set notification-fg \"" + currentColourConfig.Error + "\"\n")
                zathurarc.write("set completion-group-bg \"" + currentColourConfig.Background + "\"\n")
                zathurarc.write("set completion-group-fg \"" + currentColourConfig.Highlight + "\"\n")
                zathurarc.write("set completion-bg \"" + currentColourConfig.Page + "\"\n")
                zathurarc.write("set completion-fg \"" + currentColourConfig.Text + "\"\n")
                zathurarc.write("set completion-highlight-bg \"" + currentColourConfig.Highlight + "\"\n")
                zathurarc.write("set completion-highlight-fg \"" + currentColourConfig.Background + "\"\n")
                zathurarc.write("set inputbar-bg \"" + currentColourConfig.Page + "\"\n")
                zathurarc.write("set inputbar-fg \"" + currentColourConfig.Text + "\"\n")
                zathurarc.write("set statusbar-bg \"" + currentColourConfig.Background + "\"\n")
                zathurarc.write("set statusbar-fg \"" + currentColourConfig.Text + "\"\n")
                zathurarc.write("set highlight-color \"" + currentColourConfig.Highlight + "\"\n")
                zathurarc.write("set highlight-active-color \"" + currentColourConfig.Highlight_active + "\"\n")
                zathurarc.write("set default-bg \"" + currentColourConfig.Background + "\"\n")
                zathurarc.write("set default-fg \"" + currentColourConfig.Text + "\"\n")
                zathurarc.write("set recolor-lightcolor \"" + currentColourConfig.Page + "\"\n")
                zathurarc.write("set recolor-darkcolor \"" + currentColourConfig.Text + "\"\n")
                zathurarc.write("set index-bg \"" + currentColourConfig.Page + "\"\n")
                zathurarc.write("set index-fg \"" + currentColourConfig.Text + "\"\n")
                zathurarc.write("set index-active-bg \"" + currentColourConfig.Highlight + "\"\n")
                zathurarc.write("set index-active-fg \"" + currentColourConfig.Background + "\"\n")
                zathurarc.write("set recolor " + "true" + "\n")
                print("zathura configuration written to zathurarc")
                zathurarc.close()
            except FileNotFoundError:
                print("Zathurarc not found. Should be stored as ~/.config/zathura/zathurarc")
        except json.JSONDecodeError:
            print("""
Invalid JSON provided. Use the following format:
{
  "page": "#FFFFFF",
  "text": "#FFFFFF",
  "background": "#FFFFFF",
  "highlight": "#FFFFFF",
  "highlight_active": "#FFFFFF",
  "error": "#FFFFFF"
}
            """)
    except FileNotFoundError:
        print("Filepath cannot be resolved")


themes = ["catppuccin", "embark", "lilla",  "metropolis", "onedark", "solarized_light", "gruvbox", "nord","solarized_dark"]

def main():
    parser = argparse.ArgumentParser(description="Set theme or default config for Zathura.")
    parser.add_argument("-t", "--theme", type=str, help="Path to theme file (JSON).")
    parser.add_argument("--defaultconfig", "-dc", type=str, nargs=1, metavar="CONFIG_FILE",
                        help="Path to default config file.")

    args = parser.parse_args()
    if args.defaultconfig:
        defaultconfigfile = args.defaultconfig[0]
        setDefaultConfig(defaultconfigfile)
    if args.theme:
        filepath = args.theme
        if filepath.endswith('.json'):
            filepath = os.path.abspath(sys.argv[1])
            setTheme(filepath)
        else:
            if filepath in themes:
                setTheme(filepath + ".json")
            else:
                print("usage: main.py [-h] [-t THEME] [--defaultconfig CONFIG_FILE]")
                print(f"ERROR: {filepath} is not a valid theme name. Choose on of the following themes, or define your own in a json file.")
                for theme in themes:
                    print("\t"+theme)


if __name__ == "__main__":
    main()


