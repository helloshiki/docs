FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y openssh-server busybox
RUN useradd -m guest -s /bin/false && mkdir /home/guest/.ssh
ADD /docker-entrypoint.sh /
CMD ["/docker-entrypoint.sh"]
