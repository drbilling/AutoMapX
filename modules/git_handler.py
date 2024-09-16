import git

def clone_repo(repo_url, local_dir):
    repo = git.Repo.clone_from(repo_url, local_dir)
    return repo

def list_files(repo):
    return [file.path for file in repo.tree().traverse()]
