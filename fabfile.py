from fabric.operations import run
from fabric.decorators import hosts
from fabric.context_managers import cd, prefix

@hosts('uvar@uvar.si')
def deploy():
    with cd('~/uvar.si'):
        run('git pull')
    with prefix('workon uvar'):
        run('django-admin.py syncdb')
        run('django-admin.py collectstatic --noinput')
    run('supervisorctl restart uvar.si')

