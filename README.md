# Easy PSMP

A set of scripts and utilities to work easier with PSMP - mainly for SSH and SCP

## SSH/SCP script setup

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
export EPSMP_PSW='YourSuper$ecretP@ssw0rd'
export EPSMP_TOTP_SECRET='OTP_32CHAR_SECRET'
```

> Note: ENV variables can be also specified in '.env' file, as the script will try to load it

Before executing `epsmp` script, make sure all required libraries are installed and available

```bash
pip install -r requirements.txt
```

Once this is configured properly we can use `epsmp` script to login to host via SSH non-interactively - this means
no manual typing of required information into terminal

```bash
# For SSH
python epsmp.py ssh host1

# For SCP
python epsmp.py scp host1:/home/file .
```

## Additional configuration of SSH/SCP

It's possible to create `epsmpcfg.yaml` file containing additional configuration for SSH and/or SCP, it allows to configure custom
`binary` and `arguments` that will be used as defaults for the respective command. Check `epsmpcfg.yaml.example` file for details

> Note: It's always possible to override any configured arguments via the command line arguments passed to `epsmp.py` script

## Debugging

It's possible to export ENV variable `EPSMP_DEBUG=true`, to debug script execution and log information to file `epsmp-dbglog.log`

## TODO

- Make `epsmp.py` script available in PATH and to work like a simple binary: `essh host1` or `escp host1:/home/file .` etc.
