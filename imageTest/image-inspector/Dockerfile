FROM python:2.7

MAINTAINER Darren Jackson, <darren.a.jackson>

# install docker-py
RUN pip install docker-py

# copy in the docker image inspector script
COPY resources/image-inspector.py /usr/local/bin/image-inspector.py
RUN chmod u+x /usr/local/bin/image-inspector.py

# pass image name and config file at run time
ENTRYPOINT ["/usr/local/bin/image-inspector.py"]
CMD ["--help"]
