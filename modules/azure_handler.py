from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

def connect_to_azure(pat, org_url):
    credentials = BasicAuthentication('', pat)
    connection = Connection(base_url=org_url, creds=credentials)
    return connection

def list_azure_repos(connection):
    git_client = connection.clients.get_git_client()
    repos = git_client.get_repositories()
    return [repo.name for repo in repos]
