# ITHS Data Engineering course
A data engineering project where students get to create a blog summarizing pipeline

**Important**: If you have a Windows computer, you should execute these commands in your linux subsystem.
## Get started
### Install Python
Install the Python 3.10 to your system.

Once installed, run `python3.10 --version` in your terminal to ensure that it installed properly.

### Install Make
Many computers come pre-installed with make. Check if it's installed by running `make --version` in your terminal.

If make is not installed, install it.

Have a look at the [Makefile](Makefile). Think of this file as a collection of shortcuts. They can save you time, help you remember complicated commands and allows your teammates to easily run the same command as you.

The Makefile is pretty empty now, but you can add more commands there throughout the project.

You can execute a command by running `make my_command_name` in your terminal.
### Install Python Packages
Most of the requirements are installed with the following command
```bash
cd path/to/git-repo
make install_dependencies
source venv/bin/activate
```

## Tips
**Important**: All your python code should go inside of the src/newsfeed folder. This makes it so that you can "build" your own python package easily and not have problems with the PYTHONPATH i.e. not being able to import code from other files.


## Pull Request Practice


