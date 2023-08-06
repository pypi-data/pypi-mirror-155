# package-shipper

```py
from shipper.create_docker_compose import create_docker_compose
from shipper.create_reversed_proxy import create_reversed_proxy
from shipper.create_run_script import create_run_script
from shipper.docker_build import docker_build
from shipper.print_config_template import print_config_template
from shipper.generate_web_config import generate_web_config
from shipper.get_folder_list import get_folder_list
from shipper.place_env import place_env
from shipper.docker_publish import docker_publish
from shipper.update_project import update_project
from shipper.update_to_git import update_to_git

configs = [
    {"name": "seeset-config-breakgroup-client", "port": "7901:80", "url": "/seeset/config/break-group"},
    {"name": "seeset-config-holiday-config", "port": "7902:80", "url": "/seeset/config/holiday"},
    {"name": "seeset-config-losscause-client", "port": "7903:80", "url": "/seeset/config/loss-cause"},
    {"name": "seeset-config-machine-client", "port": "7904:80", "url": "/seeset/config/machine"},
    {"name": "seeset-config-machine-type-client", "port": "7905:80", "url": "/seeset/config/machine-type"},
    {"name": "seeset-config-people-client", "port": "7906:80", "url": "/seeset/config/people"},
    {"name": "seeset-config-rootcause-client", "port": "7907:80", "url": "/seeset/config/root-cause"},
    {"name": "seeset-config-schedule-client", "port": "7908:80", "url": "/seeset/config/schedule"},
    {"name": "seeset-config-workday-client", "port": "7909:80", "url": "/seeset/config/workday"},
]


def main():
    try:
        print_config_template('chart')
        folder_list = get_folder_list(configs)
        create_docker_compose(folder_list, configs)
        create_run_script(folder_list, configs)
        create_reversed_proxy(folder_list, configs)
        generate_web_config(folder_list, configs)
        update_project(folder_list)
        place_env(folder_list)
        docker_build(folder_list)
        docker_publish(folder_list)
        update_to_git(folder_list)
    except Exception as error:
        print(error)


if __name__ == '__main__':
    main()


```