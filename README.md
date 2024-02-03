# Easy PSMP

A set of scripts and utilities to work easier with CyberArk PSMP - mainly for SSH and SCP

## SSH/SCP script setup

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

> Note: ENV variables can be also specified in '.env' file, as the script will try to load it

Before executing `epsmp` script, make sure all required libraries are installed and available

```bash
pip install -r requirements.txt
```

Once this is configured properly we can use `epsmp` script to login to host via SSH non-interactively - this means
no manual typing of required information into terminal

```bash
# Usage
python epsmp.py -h

# For SSH
python epsmp.py ssh host1

# For SCP
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
python epsmp.py ssh -l user -p 22 hostname

# Enable debug with command line flag
python epsmp.py ssh --debug -l user -p 22 hostname
```

## TODO

- Make `epsmp.py` script available in PATH and to work like a simple binary: `essh host1` or `escp host1:/home/file .` etc.
