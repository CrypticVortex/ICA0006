import subprocess
import os
import sys

# Function to check if plink is installed
def is_plink_installed():
    """
    Check if PuTTY's plink is installed by trying to call it from the command line.
    """
    try:
        subprocess.run(["plink", "-V"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Function to download and install plink
def install_plink():
    """
    Download and install PuTTY's plink from the official download page.
    """
    plink_url = "https://the.earth.li/~sgtatham/putty/latest/w64/plink.exe"
    plink_path = os.path.join(os.environ["USERPROFILE"], "plink.exe")
    try:
        print("Downloading plink...")
        urllib.request.urlretrieve(plink_url, plink_path)
        os.chmod(plink_path, 0o755)
        print("plink installed successfully.")
    except Exception as e:
        print(f"Failed to download plink: {e}")
        sys.exit(1)

# Check if plink is installed, if not, install it
if not is_plink_installed():
    install_plink()
    
# List of your server IP addresses or hostnames
servers = ['server1_ip', 'server2_ip', 'server3_ip']

# Ask for credentials
user = "kasutaja"
password = "parool"

# Commands to install Ceph
commands = [
    'sudo apt update',
    'sudo apt install -y ceph-deploy',
    'ceph-deploy new {server1_ip} {server2_ip} {server3_ip}',
    'ceph-deploy install {server1_ip} {server2_ip} {server3_ip}',
    'ceph-deploy mon create-initial',
    'ceph-deploy admin {server1_ip} {server2_ip} {server3_ip}',
    'sudo chmod +r /etc/ceph/ceph.client.admin.keyring'
]

def run_command_on_server(server, command):
    """
    Run a given command on the specified server using SSH with the provided username and password.
    """
    ssh_command = f'plink -ssh {server} -l {user} -pw {password} -batch -hostkey "{host_key}" "{command}"'
    process = subprocess.Popen(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, error = process.communicate()
    if process.returncode == 0:
        print(f'Successfully ran command on {server}: {command}')
    else:
        print(f'Error running command on {server}: {command}\n{error.decode()}')
#Server host_key
host_key = "ssh-ed25519 255 SHA256:3tQ6zQ8KRtivhpyhH2jGd3h9+hSZdhfHax0WvZGd0Dw"

# Install Ceph on each server
for command in commands:
    for server in servers:
        run_command_on_server(server, command.format(server1_ip=servers[0], server2_ip=servers[1], server3_ip=servers[2]))
