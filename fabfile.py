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
    with cd('bioinfo_biobureau'):
        run('git pull')

def worker():
    env.hosts = ['bioworker']
def web():
    env.hosts = ['biobureau']    

#usage
#fab worker deploy_worker 
#fab web deploy_web 