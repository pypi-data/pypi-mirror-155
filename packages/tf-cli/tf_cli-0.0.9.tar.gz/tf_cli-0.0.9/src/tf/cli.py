#!/bin/python3

import click

from .api_methods import logger
from .cli_utils import CLI_Utils

# To create args for each option, replace is_flag with 
# type=(<data_type1>, <data_type2>, ...) function in each option  
@click.command()
@click.option("-b", "--build", is_flag=True, help="Test and fmt .tf code.")
@click.option("-c", "--commit", is_flag=True, help="Make commits to local repo.")
@click.option("-p", "--push", is_flag=True, help="Push tf data to server.")
@click.option("--clean", is_flag=True, help="Clean unnecessary tf files.")
def main(build, commit, push, clean) -> int:
    try:
        CLI = CLI_Utils()
    except Exception as err:
        logger.error(err)
    else:
        if build:
            CLI.build()
        
        elif commit:
            CLI.commit()
        
        elif push:
            CLI.push()
        
        elif clean:
            CLI.clean()
    return 0


if __name__ == '__main__':
    main()
