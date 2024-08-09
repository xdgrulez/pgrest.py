import os
from requests import post
from piny import YamlLoader

class pg:
    def __init__(self, config_str):
        self.config_dict = get_config_dict(config_str)

    def sql(self, sql_str):
        url_str = self.config_dict["url"]
        headers_dict = {"Content-Type": "application/json"}
        payload_dict = {"sql": sql_str}
        auth_str_tuple = (self.config_dict["username"], self.config_dict["password"])
        response = post(f"{url_str}/sql", headers=headers_dict, json=payload_dict, auth=auth_str_tuple)
        if response.ok:
            row_str_list = response.text.split("\n")
            return row_str_list
        else:
            print(response.text)
        

def get_config_dict(config_str):
    home_str = os.environ.get("PGRESTPY_HOME")
    if not home_str:
        home_str = "."
    #
    config_dict = None
    config_path_str_list = [f"{home_str}/config", f"{home_str}"]
    for config_path_str in config_path_str_list:
        if os.path.exists(f"{config_path_str}/{config_str}.yaml"):
            config_dict = YamlLoader(f"{config_path_str}/{config_str}.yaml").load()
        elif os.path.exists(f"{config_path_str}/{config_str}.yml"):
            config_dict = YamlLoader(f"{config_path_str}/{config_str}.yml").load()
    if config_dict is None:
        raise Exception(f"No configuration file \"{config_str}.yaml\" or \"{config_str}.yml\" found in \"{config_path_str_list}\" (hint: you can use KAFI_HOME environment variable to set the kafi home directory).")
    #
    return config_dict
