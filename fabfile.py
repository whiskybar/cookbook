from fabric.operations import run
from fabric.context_managers import cd, prefix, env

env.hosts = ['uvar@uvar.si']


def deploy(quick=False):
    with cd('~/uvar.si'):
        run('git pull')
    with prefix('workon uvar'):
        if not quick:
            run('django-admin.py syncdb')
        run('django-admin.py collectstatic --noinput')
    run('supervisorctl restart uvar.si')


def quickdeploy():
    deploy(quick=True)
