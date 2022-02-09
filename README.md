# GitLab repository for CO2201 Group Projects

## Prerequisites

- Python 3 (known to work with python 3.9.7)
- python `venv` module (installed separately on Debian derivatives)
- python `pip` module (installed separately on Debian derivatives)

## Notes

The following promopt denotes a comand expected to work on both
Windows and Linux:

```commandline
$>
```

## Installation

### Clone out the git repository

```commandline
$> git clone https://campus.cs.le.ac.uk/gitlab/co2201-2022/group-15.git
```

### Create a virtual environment

```commandline
$> python3 -m venv /path/to/virtualenvs/group15
```
### Activate the virtual environment

On Windows:
```commandline
X:\> /path/to/virtualenvs/group15/Scripts/activate.bat
```

On Linux:
```commandline
$ . /path/to/virtualenvs/group15/bin/activate
```

### Update pip and related packages

```commandline
$> python3 -m pip install -U pip setuptools wheel
```

### Install the dependencies

```commandline
$> python3 -m pip install -r requirements.txt
```

## How to run the web application

```commandline
$> python3 ./manage.py runserver
```

## Database

### Setup the database

```commandline
$> python3 ./manage.py migrate
```

### Changing/Expanding the database schema [1]

- First, create the model into `gameindustry/models.py`
- Execute `python3 manage.py makemigrations gameindustry`


[1] https://docs.djangoproject.com/en/4.0/intro/tutorial02/
