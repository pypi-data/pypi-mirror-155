import subprocess
import logging
import os

logger = logging.getLogger(name=__name__)


class GitUtils:
    @staticmethod
    def git_clone(local_path: str, git_url: str, tag=None, username: str = None, password: str = None):
        if not os.path.isdir(local_path):
            os.makedirs(local_path, exist_ok=True)
        try:
            if username is not None and password is not None:
                if git_url.startswith('https://'):
                    git_url = git_url.replace('https://', 'https://{}:{}@'.format(username, password))
                elif git_url.startswith('http://'):
                    git_url = git_url.replace('http://', 'http://{}:{}@'.format(username, password))
                else:
                    git_url = 'https://{}:{}@{}'.format(username, password, git_url)

            branch_cmd = ['--branch', tag] if tag is not None else []
            cmd = ['git', 'clone'] + branch_cmd + [git_url, local_path]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = [std.decode() for std in p.communicate()]
            exit_code = p.returncode
            response = not exit_code
            if exit_code:
                log_message = 'Error executing:  {ps1} $ {cmd}\n{err}'.format(
                    ps1=local_path, cmd=' '.join(cmd), err=err
                )
                if password is not None:
                    log_message = log_message.replace(password, '********')
                logging.error(log_message)
        except Exception:
            response = False
            logging.warning('Error cloning git to: {}'.format(local_path))
        return response
