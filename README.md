# Easy PSMP

A set of scripts and utilities to work easier with PSMP - mainly for SSH and SCP

## SSH script setup

To use PSMP with SSH, for the convinience, host connection should be properly configured, for e.g.:

```text
# cat ~/.ssh/config

Host host1
    User userid@userid-udm#THEDOMAIN.COM@hostname1
    Hostname psmp.prod.thedomain.com

Host host2
    User userid@userid-udm#THEDOMAIN.COM@hostname2
    Hostname psmp.prod.thedomain.com

Host host3
    User userid@userid-udm#THEDOMAIN.COM@hostname3
    Hostname psmp.prod.thedomain.com

# #########################################

Host *
    StrictHostKeyChecking no
    UserKnownHostsFile=/dev/null
```

Next, two ENV variables must be available/exported in current shell session:

```bash
export ESSH_PSW='YourSuper$ecretP@ssw0rd'
export ESSH TOTP_SECRET='OTP_32CHAR_SECRET'
```

> Note: ENV variables can be also specified in '.env' file, as the script will try to load it

Before executing 'essh.py` script, make sure all required libraries are installed and available

```bash
pip install -r requirements.txt
```

Once this is configured properly we can use 'essh.py script to login to host via SSH non-interactively - this means
no manual typing of required information into terminal

```bash
python essh.py host1
```

## TODO

- Make `essh.py` script available in PATH and to work like a simple binary: `essh host1` etc.
- Make `SCP` version of the script
