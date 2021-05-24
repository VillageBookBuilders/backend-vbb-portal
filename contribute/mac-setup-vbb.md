
# Initial Setup for macOS

## First Time Installs

__install homebrew__  
[Homebrew](https://brew.sh/)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

__install git__  
[git](https://git-scm.com/download/mac)  
[git install mac](https://git-scm.com/download/mac)
```
brew install git
```

__install python__  
[Python Brew Formulae](https://docs.brew.sh/Homebrew-and-Python)  
```
brew install python
```

__install Postgresql__  
[Postgresql Brew Formulae](https://formulae.brew.sh/formula/postgresql)  
[Postgres Wiki](https://wiki.postgresql.org/wiki/Homebrew)
```
brew install postgresql
```
to start postgres server
```
brew services start postgresql
```
to stop postgres server
```
brew services stop postgresql
```

__install pyenv__  
[pyenv github](https://github.com/pyenv/pyenv)  
[pyenv Brew Formulae](https://formulae.brew.sh/formula/pyenv)
We'll use pyenv to install the version of python that vbb uses
```
brew install openssl readline sqlite3 xz zlib
brew install pyenv
```
add the following to your .bash_profile, .zshrc, or .zprofile file
```
export PYENV_ROOT="$HOME/.pyenv/shims"
export PATH="$PYENV_ROOT:$PATH"
export PIPENV_PYTHON="$PYENV_ROOT/python"
```

## VBB setup

### download backend-vbb-portal repo
go to your github folder
```
mkdir backend-vbb-portal
cd backend-vbb-portal
git init
git remote add origin git@github.com:VilllageBookBuilders/backend-vbb-portal.git
git fetch
git pull origin master
```

install python 3.8.5 locally using pyenv
```
pyenv local 3.8.5
```

confirm with:
```
python -V
```
if you are not seeing python 3.8.5 make sure you've added the exports to your bash / zshrc / zprofile file


### create a vbb table in the postgres default databse:
start postgres server
```
brew services start postgresql
```

create the vbb database
```
createdb vbb
```

create the virtual environment and run it
```
python -m venv env
source env/bin/activate
pip install -r requirements/local.txt
python manage.py migrate
python manage.py runserver
```

## create a superuser account
```
python manage.py createsuperuser
```

