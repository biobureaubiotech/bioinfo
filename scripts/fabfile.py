from fabric.api import env, run, local, cd, settings, hide

# env.hosts = ['localhost']#, 'host2@example.com'

# env.use_ssh_config = True
# env.hosts = ['mendel']
# env.user = 'raony'
# env.key_filename = '/home/raony/dev/biobureau/keys/bioinfo_biobureau.pem'

#fab sethost:54.173.21.14 reload
#http://www.linuxjournal.com/content/fabric-system-administrators-best-friend?page=0,1

def sethost(foo):
  env.hosts = [foo]
  env.user = 'ubuntu'
  return env

def initiate_instance():
    print('env.hosts:', env.hosts)
    # run("ls -l")
    # run("pwd")
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
    ):
        command = 'sudo apt-get update;sudo apt-get -y upgrade'
        output = run(command)
        for line in output.splitlines():
            print(line)


def reload():
    """ Reload Apache """
    # env = setenv("foo")
    # print(env.hosts)
    print('env.hosts:', env.hosts)
    # output = run("ls -l")
    # output += run("sudo apt update")
    # output += run("sudo apt -f upgrade")
    # output = run("screen -x")
    # output = run('screen -d -m "yes"')
    # output = run('screen -d -m yes; sleep 1')
    # print(output)
    # output = run("screen -S -d 'ls -lah; exec bash'")#-d -m 
    # output = run("""screen -dmS test-screen bash -c "top; exec bash" """)
    #ssh root@remoteserver 'screen -S backup -d -m /root/backup.sh'
    #ssh root@remoteserver screen -d -m ./script
    # print(output)

##!/bin/bash
# source ENV/bin/activate
# python run.py    