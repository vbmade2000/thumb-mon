# TODO:
# This Dockerfile is not completed yet. Following are next steps
# Copy thumber source code to appropriate directory
# Start thumber

FROM centos
LABEL maintainer="vbmade2000@gmail.com"

# TODO: Investigate more about Python3 because Python comes already with
# CentoS8. It is being installed here because it was difficult to setup
# already installed Python3 as a default one using alternative --set python
# command.
RUN dnf install -y python3 python3-dbus

# This instruction is just for experiment. 
COPY ./dist/rpmbuild/RPMS/noarch /tmp/thumber-1.0-0.noarch.rpm 
