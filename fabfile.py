from fabric.api import run, local, env, cd

def reset_db():
    local('uname -s')
    
def backup_users():
    local('python manage.py dumpdata account users --indent 2 > fixtures/users.json')

def restore_users():
    local('python manage.py loaddata fixtures/users.json')

def reset():
    local('./manage.py reset_db')
    local('rm -rf projects/migrations')
    local('./manage.py makemigrations projects')
    local('./manage.py migrate')
    restore_users()

def deploy_web():
    with cd('bioinfo_biobureau'):
        run('git pull')

    run('sudo systemctl restart gunicorn')
def deploy_worker():
    local('git add .;git commit -am "deploy to worker"')
    local('git push')
    with cd('bioinfo_biobureau'):
        run('git pull')

def worker():
    env.hosts = ['bioworker']
def web():
    env.hosts = ['biobureau']    

def reset_db():
    
    # local('psql bioinfo_biobureau -c "DROP DATABASE bioinfo_biobureau"')
    local('dropdb bioinfo_biobureau')
    local('createdb bioinfo_biobureau')
    
    local('rm -rf projects/migrations')
    local('rm -rf analyses/migrations')

    # local('find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf')

    local('python manage.py makemigrations projects')
    local('python manage.py makemigrations analyses')

    local('python manage.py makemigrations')
    local('python manage.py migrate')
    local('python manage.py loaddata fixtures/users.json')
    local('python manage.py loaddata fixtures/projects.json')
    local('python manage.py loaddata fixtures/analyses.json')
    local('python manage.py runserver')

#usage
#fab worker deploy_worker 
#fab web deploy_web 