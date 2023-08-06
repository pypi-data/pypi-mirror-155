from subprocess import check_output


def get_last_change_hash(path):
    rev = check_output(["git", "rev-list", "-1", "HEAD", path])
    return rev.decode()[:7]
