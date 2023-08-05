# Terraform CLI: KISS Style

## Summary
This is the design and implementation of providing simple and reliable terraform (`tf`) commands for devs ops that build, commit and push `.tf` files. Terraform has hidden functionalities that devs may not be familar with. It shouldn't be the dev's responsibility to remember multiple commands every time they make a commit to terraform servers. That's why I decided to create a bash program orchestrated by python for devs to only remember a few commands.

```
Usage: tf [OPTIONS]

Options:
  -b, --build   Test and fmt .tf code.
  -c, --commit  Make commits to local repo.
  -p, --push    Push tf data to server.
  --clean       Clean unnecessary tf files.
  --help        Show this message and exit.
```  



## File Information
The main directory that requires attention is the __src/tf__ directory:

- __api_methods.py__ - This files provides the users to see incoming messages by creating a global logger variable.

- __cli_utils.py__ - Creates essential utilities for `cli.py` that performs the system commands of the program.

- __cli.py__ - Bootstrap function for `cli_utils.py`. This file mainly interacts with the user by running the command `tf` and providing them `[OPTIONS] -b -c -p` in a pretty interface. 


## How do I run the Program?

NOTE : This code has only been tested on the latest Ubuntu operating system. Run on macOS at your own risk, but this program is not operational in Windows.   

## Running on Virtual Env (venv)

NOTE: You must have python3 installed to run these
commands. Infomation about python can be found [here](https://www.python.org/about/).

Follow these instructions if you want to run the files using venv

```
./build.sh

# run venv 
source tf_env/bin/activate 

# use the program as intended
tf [OPTIONS]
```

### Cleaning Virtual Env (venv) & Dependencies
```
./clean.sh

# exit the virtual environment 
deactivate 
```

## Who do I talk to?

__Name__ - Rooklyn Kline<br>
__Email__ - rkline2@umbc.edu<br>