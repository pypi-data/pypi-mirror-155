import threading
import logging
import hashlib
import time
import os
import dtlpy as dl

logger = logging.getLogger(name='AgentRunner.Syncer')


class ArtifactsSyncer(threading.Thread):
    def __init__(self, local_directory, project, package_name, execution_id, interval=5 * 60):
        """

        :param local_directory: local directory to sync
        :param project: project to sync
        :param package_name: package to sync
        :param execution_id: execution id to sync
        :param interval: time between syncs (in sec)
        """
        super(ArtifactsSyncer).__init__()
        self.interval = interval
        self.local_directory = local_directory
        assert isinstance(project, dl.entities.Project)
        self.project = project

        self.execution_id = execution_id
        self.package_name = package_name

    @staticmethod
    def md5(fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def download(self):
        logger.info('[Start] Syncing to local directory')
        artifacts = self.project.artifacts.download(localpath=self.local_directory,
                                                    package_name=self.package_name,
                                                    execution_id=self.execution_id,
                                                    overwrite=True)
        logger.info('[Done] Syncing to local directory. Num artifacts downloaded: {}'.format(len(artifacts)))
        return True

    def run(self):
        while True:
            # get local files list
            local_filepaths = list()
            for path, subdirs, files in os.walk(self.local_directory):
                for name in files:
                    filepath = os.path.join(path, name)
                    local_filepaths.append(filepath)

            # get remote items
            remote_path = self.project.artifacts.get_remote_path(package_name=self.package_name,
                                                                 execution_id=self.execution_id)
            artifacts = self.project.artifacts.list(package_name=self.package_name,
                                                    execution_id=self.execution_id)
            remote_filepaths = {os.path.relpath(artifact.filename, remote_path): artifact for artifact in artifacts}

            for filepath in local_filepaths:
                abs_filepath = os.path.relpath(filepath, self.local_directory)
                local_md5 = self.md5(filepath)
                if abs_filepath in remote_filepaths:
                    # file exists remotely
                    try:
                        remote_md5 = remote_filepaths[abs_filepath].metadata['system']['md5']
                        if local_md5 == remote_md5:
                            need_to_upload = False
                        else:
                            need_to_upload = True
                    except KeyError:
                        need_to_upload = True
                else:
                    # file doesnt exists
                    need_to_upload = True

                if need_to_upload:
                    logger.info('[Start] Syncing file: {}'.format(filepath))
                    artifact = self.project.artifacts.upload(filepath=filepath,
                                                             package_name=self.package_name,
                                                             execution_id=self.execution_id,
                                                             overwrite=True)
                    if 'system' not in artifact.metadata:
                        artifact.metadata['system'] = dict()
                    artifact.metadata['system']['md5'] = local_md5
                    artifact.update(system_metadata=True)
                    logger.info('[Done] Syncing file: {}'.format(filepath))
            time.sleep(self.interval)
