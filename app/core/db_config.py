from configparser import ConfigParser

def load_config(filename="database.ini", section="postgres"):
    parser = ConfigParser()
    parser.read(filename)
    config ={}

    if parser.has_section(section):
        param = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
        return param
    else:
        raise Exception(f"The section {section} does not exist in the file {filename}")

if __name__ == "__main__":
    config = load_config()
    print(config)