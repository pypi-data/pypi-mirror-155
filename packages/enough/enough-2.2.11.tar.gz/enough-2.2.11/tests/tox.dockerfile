RUN pip3 install python-openstackclient python-heatclient python-glanceclient # this is not necessary to run tests but to cleanup leftovers when tests fail
RUN pip install tox
# BEGIN dependencies playbooks/infrastructure/test-pipelining.yml
RUN apt-get install -y python
# END dependencies playbooks/infrastructure/test-pipelining.yml
# BEGIN dependencies of test/ssh
RUN apt-get install -y jq
RUN pip install tox yq
RUN apt-get install -y python3-apt python3-libvirt python3-lxml # required because python3 is used not python2
# END dependencies of test/ssh

# Cache Python environment creations
COPY requirements.txt requirements-dev.txt tox.ini /opt/
RUN mkdir /opt/docs
COPY docs/requirements.txt /opt/docs/
# BEGIN HACK TO REMOVE WHEN tox installs setuptools >= 61.2.0
# see https://lab.enough.community/main/infrastructure/-/merge_requests/525#note_4791
RUN pip install tox-setuptools-version
# END HACK TO REMOVE WHEN tox installs setuptools >= 61.2.0
RUN tox --notest -e py3_cache,flake8,docs

# BEGIN dependencies enabling .test resolution in the test container
RUN apt-get install -y bind9
COPY tests/named.conf.local /etc/bind
COPY tests/named.conf.options /etc/bind
COPY tests/entrypoint.sh /opt
# COPY --chmod requires BuildKit and docker 20.10
RUN chmod 0777 /opt/entrypoint.sh
ENTRYPOINT ["/opt/entrypoint.sh"]
# END dependencies enabling .test resolution in the test container
