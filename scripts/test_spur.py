import spur

 # = spur.SshShell(hostname="localhost", username="bob", password="password1")

shell = spur.SshShell(
    hostname="54.173.21.14",
    username="ubuntu",
    
)
## private_key_file="path/to/private.key"

with shell:
    result = shell.run(["echo", "-n", "hello"])
print(result.output) # prints hello