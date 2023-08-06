#
# A simple Dockerfile to quickly build a docker image for testing. It is not at all secure, so never upload a docker
# image built this way to an image repo! Use the Dockerfiles in the HEA Main project to create distribution-worthy
# images.
#
# This Dockerfile accepts one arguments:
#     SOURCE: path to a tarball (tar.gz or tgz file; required).
#
# Run as follows:
#     docker build --build-arg SOURCE="dist/<tarball>" -t registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-folders:latest .
#
# To create a tarball, run the following:
#     python setup.py clean --all sdist bdist_wheel
#
# Run the image from the HEA Main project with the following command (see the top of the docker-compose-dev.yml file
# for instructions):
#     docker-compose -f ./docker-compose-dev.yml up
#

FROM hea-python-base:latest

ARG SOURCE

RUN apt-get update && \
    apt-get install --no-install-recommends -y git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app
COPY $SOURCE .
RUN mkdir sdist
RUN tar xvzf $(ls *.tgz *.tar.gz) --directory sdist --strip-components 1
WORKDIR /home/app/sdist
RUN pip install -r requirements_dev.txt
RUN pytest
WORKDIR /home/app
COPY docker-entrypoint.sh .
RUN dos2unix ./docker-entrypoint.sh
ENTRYPOINT [ "sh", "docker-entrypoint.sh" ]
EXPOSE 8080
