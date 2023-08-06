import yaml

from playbooks.hostea.roles.hostea.files import hosteasetup

testinfra_hosts = ['ansible://gitea-host']


def get_domain(inventory):
    vars_dir = f'{inventory}/group_vars/all'
    return yaml.safe_load(open(vars_dir + '/domain.yml'))['domain']


def test_hosteasetup_gitea(request, pytestconfig, host, tmpdir):
    certs = request.session.infrastructure.certs()
    domain = get_domain(pytestconfig.getoption("--ansible-inventory"))

    #
    # Login Gitea
    #
    gitea = hosteasetup.Gitea(f'gitea.{domain}')
    gitea.certs(certs)
    username = "root"
    password = "etquofEtseudett"
    gitea.authenticate(username=username, password=password)
    u = gitea.users.get("root")
    assert u.username == "root"
    #
    # Create project
    #
    gitea.projects.delete(username, "testproject")
    assert gitea.projects.get(username, "testproject") is None
    p = gitea.projects.create(username, "testproject")
    assert p.project == "testproject"
