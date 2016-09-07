from fabric.api import env, run, local, cd
# env.use_ssh_config = True
env.hosts = ['54.173.21.14']
env.user = 'raony'
# env.key_filename = '/home/raony/dev/biobureau/biob_plataforma/keys/bioinfo_biobureau.pem'
run("ls -lah")
