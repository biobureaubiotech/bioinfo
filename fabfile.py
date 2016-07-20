from fabric.api import run, local

def reset_db():
    local('uname -s')
def backup_users():
    local('python manage.py dumpdata account users --indent 2 > fixtures/users.json')
def restore_users():
    local('python manage.py loaddata fixtures/users.json')

def reset():
    local('./manage.py sqlflush | ./manage.py dbshell')