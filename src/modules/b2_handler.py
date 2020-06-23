"""Upload File - Utility
Upload a file to B2 storage

The B2 handler can be configured with the following environmental variables, or the class
initialized with dict with the same keys into class initialization.
    B2_KEY_ID       - The ID of the B2 key
    B2_KEY_SECRET   - The B2 Key secret
    B2_APP_BUCKET   - The B2 Bucket name
    B2_APP_NAME     - The B2 Application name to use

"""
import logging
import os

import arrow
from b2sdk.v1 import B2Api, InMemoryAccountInfo
import b2sdk

tmp_dir = os.environ.get('DROP_ZONE_TMP_DIR')


class B2Handler:

    def __init__(self, auth: dict={}):
        """Create a new instance of B2Handler. The handler defaults to using environment vars for
           all B2 settings, however different settings can be passed in through the init of the
           class.
        """
        self.allow_name_collisions = False
        if auth:
            self.key_id = auth['B2_KEY_ID']
            self.key_secret = auth['B2_KEY_SECRET']
            self.bucket_name = auth['B2_APP_BUCKET']
            self.app_name = auth['B2_APP_NAME']
        else:
            self.key_id = os.environ.get('B2_KEY_ID')
            self.key_secret = os.environ.get('B2_KEY_SECRET')
            self.bucket_name = os.environ.get('B2_APP_BUCKET')
            self.app_name = os.environ.get('B2_APP_NAME')
        self.auth()

    def auth(self):
        """Authenticate to the B2 service. """
        info = InMemoryAccountInfo()  # store credentials, tokens and cache in memory
        b2_api = B2Api(info)
        b2_api.authorize_account('production', self.key_id, self.key_secret)
        # try:
        #     b2_api.authorize_account('production', self.key_id, self.key_secret)
        # except b2sdk.exception.InvalidAuthToken:
        #     logging.error('Could not auth with B2')
        #     return False
        self.b2_api = b2_api
        return True

    def list(self, path: str=""):
        """List files within a B2 bucket, with an optional path. """
        bucket = self.b2_api.get_bucket_by_name(self.bucket_name)
        res = bucket.ls(path)
        return res

    def upload(self, local_fp: str, remote_fp: str=None, meta: dict={}) -> bool:
        """Upload a local file to a B2 bucket. """
        remote_file_info = self.remote_file_name(local_fp)
        remote_file_name = remote_file_info['remote_file_name']
        remote_fp = '%s/%s' % (self.app_name, remote_file_name)
        file_info = meta
        file_info.update(remote_file_info['meta'])

        bucket = self.b2_api.get_bucket_by_name(self.bucket_name)
        logging.info('Uploading file: %s -> %s' % (local_fp, remote_fp))

        resp = bucket.upload_local_file(
            local_file=local_fp,
            file_name=remote_fp,
            file_infos=file_info)
        logging.info('Writing b2://%s/%s' % (self.bucket_name, remote_fp))
        if resp:
            logging.info('')
            print(resp)
            return True

        return False

    def download(self, remote_fp):
        """ """
        print('IN B2 DOWNLOAD')
        print('Downloading: %s' % remote_fp)
        bucket = self.b2_api.get_bucket_by_name(self.bucket_name)
        try:
            bucket.download_file_by_name(remote_fp, os.path.join(tmp_dir, 'test'))
        except b2sdk.exception.FileNotPresent:
            print('File 404 on Download: %s' % remote_fp)
            return False

        return True

    def remote_file_name(self, local_file_name: str) -> str:
        """Filter the local file name into the eventual remote file name. """
        remote_file_name = local_file_name

        # Simplify the name to just the file's name, removing the full local path.
        if '/' in remote_file_name:
            remote_file_name = local_file_name[local_file_name.rfind('/') + 1:]

        if not self.allow_name_collisions:
            remote_file_data = self.check_name_availability(remote_file_name)

        return remote_file_data

    def check_name_availability(self, remote_file_name) -> dict:
        """Checks if the desired remote name is free, if not appends a UTC timestamp to the file,
           along with meta data showing a `collision_avoidance`.
        """
        desired_path = '%s/%s' % (self.app_name, remote_file_name)
        current_files = self.list(self.app_name)
        meta = {}

        for f, name in current_files:
            if '.bzEmpty' in f.file_name:
                continue
            if f.file_name == desired_path:
                remote_file_name = self._create_non_overwrite_name(remote_file_name)
                meta = {
                    'collision_avoidance': 'true'
                }
                break

        ret = {
            'remote_file_name': remote_file_name,
            'meta': meta
        }

        return ret

    def _create_non_overwrite_name(self, remote_file_name: str) -> str:
        """In the event Add the current UTC time to the file to avoid a name collision. """
        print('FOUND NAME COLLISION')
        now = arrow.utcnow()
        append_time_str = "%s_%s_%s_%s_%s_%s" % (
            now.year,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.microsecond)
        if '.' in remote_file_name:
            rfm = remote_file_name
            remote_file_name = "%s_%s%s" % (
                rfm[:rfm.rfind('.')],
                append_time_str,
                rfm[rfm.rfind('.'):])
        else:
            remote_file_name += append_time_str
        return remote_file_name


if __name__ == "__main__":
    file_path = '/tmp/RBDevil_-_peppers.png'

    b2 = B2Handler()
    b2.upload(file_path)

# End File: drop-zone/drop_zone/modules/b2_handler.py
