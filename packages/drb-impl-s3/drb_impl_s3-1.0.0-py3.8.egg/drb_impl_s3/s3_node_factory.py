from drb import DrbNode
from drb.factory import DrbFactory
from drb_impl_http import DrbHttpNode
from requests.auth import HTTPBasicAuth

from drb_impl_s3 import DrbS3Service, Auth


class S3NodeFactory(DrbFactory):

    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, DrbS3Service):
            return node
        if isinstance(node, DrbHttpNode):
            if isinstance(node.auth, HTTPBasicAuth):
                auth = Auth(service_name=node.path.original_path,
                            aws_access_key_id=node.auth.username,
                            aws_secret_access_key=node.auth.password)
            else:
                auth = Auth(service_name=node.path.original_path)
            return DrbS3Service(auth=auth)
        raise NotImplementedError("Call impl method")
