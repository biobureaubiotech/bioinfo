import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_system_host_keys()

# ssh.load_system_host_keys()
server = '54.173.21.14'
username = 'raony'
ssh.connect(server, username=username)
cmd_to_execute = 'ls -lah'
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
print(ssh_stdin, ssh_stdout, ssh_stderr)
print(ssh_stdout.readlines())
