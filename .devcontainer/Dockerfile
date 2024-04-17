# python version
ARG VARIANT="3.11-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}
        
# always auto setup remote for new git branches
RUN git config --global --add --bool push.autoSetupRemote true