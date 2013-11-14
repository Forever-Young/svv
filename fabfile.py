from fabric.api import *

env.hosts = ['svv']
env.use_ssh_config = True

def deploy():
    with cd('/home/svv/svv'):
        print("Updating sources")
        print("Checking for uncommitted changes")
        with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
            result = run('hg shelve').return_code
        if result == 0:
            print("Shelved uncommitted changes")
        else:
            print("No uncommitted changes")
        run('hg pull')
        run('hg update')

        with prefix('source /home/svv/env/bin/activate'):
            run('pip install -r docs/requirements.txt --no-deps')
            run('./manage.py syncdb --noinput')
            run('./manage.py migrate --noinput')
            run('./manage.py collectstatic -c -l --noinput')

    print("Restarting workers")
    run('sudo /home/svv/restart-wsgi.sh')
    run('sudo /home/svv/restart-celery.sh')
