# Easy PSMP

A set of scripts and utilities to work easier with CyberArk PSMP - mainly for SSH and SCP

## SSH/SCP script setup

### Installation

```bash
# Clone repository to home directory
git clone --depth 1 https://github.com/mdpdesign/easy-psmp.git ~/.easy-psmp

# Initialize vitual environment - make sure you have "virtualenv" available
# alternatively replace it with "python -m venv .venv"
pushd ~/.easy-psmp && virtualenv .venv && source ~/.easy-psmp/.venv/bin/activate \
    && pip install -r requirements.txt \
    && popd

# Ensure scripts are executable & create symbolic links for provided commands
chmod +x ~/.easy-psmp/essh.sh && sudo ln -s ~/.easy-psmp/essh.sh /usr/local/bin/essh
chmod +x ~/.easy-psmp/escp.sh && sudo ln -s ~/.easy-psmp/escp.sh /usr/local/bin/escp
```

### General setup

To use PSMP with SSH or SCP, for the convenience, host connection should be properly configured, for e.g.:

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
export EPSMP_PSW='YourSuper$ecretP@ssw0rd'
export EPSMP_TOTP_SECRET='OTP_32CHAR_SECRET'
```

> Note: ENV variables can be also specified in '.env' file inside installation directory, as the script will try to load it

Before executing `essh|escp|epsmp` script(s), make sure all required libraries are installed and available

```bash
pip install -r requirements.txt
```

Once this is configured properly we can use `essh|escp|epsmp` script(s) to login to host via SSH non-interactively - this means
no manual typing of required information into terminal

```bash
# Usage
essh -h
escp -h

# For SSH
essh host1
essh --debug -p 22 user@hostname

# For SCP
escp host1:/home/file .
escp --debug -P 2222 host1:/home/file .

# W/o setting up execution scripts
python epsmp.py -h
python epsmp.py ssh host1
python epsmp.py scp host1:/home/file .
```

## Additional configuration of SSH/SCP

It's possible to create `epsmpcfg.yaml` file in the same directory as the script, containing additional configuration for SSH and/or SCP,
it allows to configure custom `binary` and `arguments` that will be used as defaults for the respective command.
Check `epsmpcfg.yaml.example` file for details

## Debugging

It's possible to export ENV variable `EPSMP_DEBUG` and set it to any non-empty value or provide `--debug` flag, to debug script execution
and log information to local file: `epsmp-dbglog.log`

```bash
# Enable debug with ENV variable
export EPSMP_DEBUG=1
essh -l user -p 22 hostname # or
python epsmp.py ssh -l user -p 22 hostname

# Enable debug with command line flag
essh --debug -l user -p 22 hostname # or
python epsmp.py ssh --debug -l user -p 22 hostname
```

## TODO

- Possibly simplify installation steps with script
