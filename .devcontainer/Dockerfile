
ARG VARIANT="jammy"
FROM ubuntu:${VARIANT}

# ENV LANG="C.UTF-8"
ENV LC_ALL="en_US.UTF-8"

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        git \
        zsh \
        ssh \
        less \
        vim \
        bind9-dnsutils \
        gnupg2 \
        dirmngr \
        coreutils \
        unzip \
        locales \
        # Pyenv build deps
        build-essential \
        libssl-dev \
        zlib1g-dev \
        libbz2-dev \
        libreadline-dev \
        libsqlite3-dev \
        curl \
        libncursesw5-dev \
        xz-utils \
        tk-dev \
        libxml2-dev \
        libxmlsec1-dev \
        libffi-dev \
        liblzma-dev \
    && locale-gen en_US.UTF-8 && update-locale LANG=en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ARG USER=vscode
ARG UID=1000
ARG GID=$UID
ARG USER_HOME=/home/vscode

RUN groupadd -g ${GID} ${USER} \
    && useradd -d ${USER_HOME} -u ${UID} -g ${GID} -l -m -s /usr/bin/zsh ${USER}

RUN chgrp -R 0 ${USER_HOME} && \
    chmod -R g=u ${USER_HOME}

# Allow to run docker cli - DooD, Please mount docker.sock and binary in devcontainer.json
RUN if ! grep -qE '^docker:' /etc/group; then \
        echo "(*) Creating missing docker group with GID 999..."; \
        groupadd --gid 999 --system docker; \
        usermod -aG docker ${USER}; \
    fi

# Install tools
ARG TOOLS_TMP=/tmp/tools
ARG LSD_VER=1.0.0
RUN mkdir -m a=rwx -p ${TOOLS_TMP} && cd ${TOOLS_TMP} \
    && curl -sSL https://github.com/lsd-rs/lsd/releases/download/v${LSD_VER}/lsd_${LSD_VER}_amd64.deb -o lsd.deb \
    && dpkg -i lsd.deb \
    && rm -rf ${TOOLS_TMP}

USER ${UID}

# Update PATH variable for tools that will be installed
RUN echo "export PATH=\$PATH:${USER_HOME}/.local/bin:${USER_HOME}/.pyenv/bin" >> ${USER_HOME}/.zshenv

# Install fzf, antigen etc.
RUN git clone https://github.com/zsh-users/antigen.git ${USER_HOME}/antigen \
    && git clone --depth 1 https://github.com/junegunn/fzf.git ${USER_HOME}/.fzf \
    && ${USER_HOME}/.fzf/install --all

# Install Pyenv and Python
ARG PYTHON_VER=3.12.1
RUN git clone https://github.com/pyenv/pyenv.git ${USER_HOME}/.pyenv

ENV PYENV_ROOT=${USER_HOME}/.pyenv
ENV PATH="${PYENV_ROOT}/shims:${PYENV_ROOT}/bin:$PATH"

RUN pyenv install ${PYTHON_VER} \
    && pyenv global ${PYTHON_VER} \
    && pyenv versions \
    && python -V

# Install Python packages & tools
RUN pip install --upgrade pip pre-commit

COPY --chown=${UID}:${GID} --chmod=644 .zshrc ${USER_HOME}/.zshrc
COPY --chown=${UID}:${GID} --chmod=644 .p10k.zsh ${USER_HOME}/.p10k.zsh

WORKDIR ${USER_HOME}

SHELL ["/usr/bin/zsh", "-c"]

RUN source ${USER_HOME}/.zshrc