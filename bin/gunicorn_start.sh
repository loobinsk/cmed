#!/bin/bash

NAME="vrachivmeste"                                  # Name of the application
DJANGODIR=/var/www/vrachivmeste.ru/cmedu            # Django project directory
SOCKFILE=/var/www/vrachivmeste.ru/run/gunicorn.sock  # we will communicte using this unix socket
USER=cmedu                                        # the user to run as
GROUP=cmedu                                     # the group to run as
NUM_WORKERS=11                                      # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=cmedu.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=cmedu.wsgi                     # WSGI module name
ENV_DIR=/var/www/vrachivmeste.ru/.env_new

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
source $ENV_DIR/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec $ENV_DIR/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=127.0.0.1:8030 \
  --timeout 72000  \
  --log-level=debug \
  --log-file=/var/www/vrachivmeste.ru/vrvm_log.log: