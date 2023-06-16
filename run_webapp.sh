#!/bin/bash
SH=$(cd `dirname $BASH_SOURCE` && pwd)
AH=$(cd "$SH" && pwd)

echo $SH
echo $AH

#region load envvar APP_PORT only, from .env file
if [ -z $APP_PORT ]; then
    dotenv_path="$AH/.env" ; [ ! -f $dotenv_path ] && (echo "ERROR Envfile is required at $dotenv_path; plesae clone one eg from $dotenv_path-local"; kill $$)
        # source $dotenv_path  #NOTE we cannot use simple source here, it will override/pollute current envvar eg ENV_NAME, APP_PORT may be passed by gcp cloudrun ie set some envvar before running the Dockerfile
        eval $(
            source $dotenv_path;  # source inside eval() will effect inner thread here ie outter thread stay untouched ref. https://unix.stackexchange.com/a/266630/17671
            echo APP_PORT=$APP_PORT;
        )
            [ -z $APP_PORT ] && (echo "Envvar APP_PORT is required; please define one in $dotenv_path"; kill $$)
fi
#endregion

if [[ -f "$HOME/.pyenv/shims/pipenv" ]]; then
  pipenv="$HOME/.pyenv/shims/pipenv"
elif [[ -f "$HOME/.local/bin/pipenv" ]]; then
  pipenv="$HOME/.local/bin/pipenv"
elif [[ -f "/opt/homebrew/bin/pipenv" ]]; then
  pipenv="/opt/homebrew/bin/pipenv"
elif [[ -f "/usr/local/bin/pipenv" ]]; then
  pipenv="/usr/local/bin/pipenv"
else
  echo "pipenv application not found"
fi

cd $AH
    PYTHONPATH=`pwd` $pipenv run                uvicorn src.main:app  --host=0.0.0.0 --port=$APP_PORT                                       2>&1 | tee "$SH/$(basename $BASH_SOURCE).log"

_=cat<<EOT
    PIPENV_DONT_LOAD_ENV=0   stop autoloading .env ref. https://pipenv-fork.readthedocs.io/en/latest/advanced.html#automatic-loading-of-env
                             this allows external envvar, eg from cloudrun, passed to this script and NOT OVERIDDEN
EOT