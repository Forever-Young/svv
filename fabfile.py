from fabric.api import *

env.hosts = ['svv']
env.use_ssh_config = True

def deploy():
    with cd('/home/svv/svv'):
        print("Stashing uncommitted changes, if any")
        run("git stash")
        print("Updating sources")
        run('git pull')

        with prefix('source /home/svv/env/bin/activate'):
            run('pip install -r docs/requirements.txt --no-deps')
            run('./manage.py migrate --noinput')
            run('./manage.py collectstatic -c -l --noinput')

    print("Restarting workers")
    run('sudo /home/svv/restart-wsgi.sh')
    run('sudo /home/svv/restart-celery.sh')
