import io

import boto3
from botocore.client import BaseClient


class Auth:
    """
    This class give us all the requirement to connect to a swift service.

    Parameters:
        service_name: The name of a service, e.g. 's3' or 'ec2'.
            region_name: The name of the region associated with the client.
            A client is associated with a single region.

        api_version: The API version to use.  By default, this implementation
            use the latest API version. You only need to specify this parameter
            if you want to use a previous API version of the client.

        use_ssl: Whether to use SSL.  By default, SSL is used.
            Note that not all services support non-ssl connections.

        verify: Whether to verify SSL certificates. By default,
            SSL certificates are verified.  You can provide the following
            values:
            * False - do not validate SSL certificates.  SSL will still be
            used (unless use_ssl is False), but SSL certificates
            will not be verified.
            * path/to/cert/bundle.pem - A filename of the CA cert bundle to
            uses.

        endpoint_url: The complete URL to use for the constructed
            client. If this value is provided, then ``use_ssl`` is ignored.

        aws_access_key_id: The access key to use when creating
            the client.

        aws_secret_access_key: The secret key to use when creating
            the client.

        aws_session_token: The session token to use when creating
            the client.

        config: Advanced client configuration options. If region_name
            is specified in the client config, its value will take precedence
            over environment variables and configuration values, but not over
            a region_name value passed explicitly to the method.  If
            user_agent_extra is specified in the client config, it overrides
            the default user_agent_extra provided by the resource API.
      """

    def __init__(self,
                 **kwargs):
        self.service_name = "s3"
        self.region_name = kwargs.get("", None)
        self.api_version = kwargs.get("api_version", None)
        self.use_ssl = kwargs.get("use_ssl", True)
        self.verify = kwargs.get("verify", None)
        self.endpoint_url = kwargs.get("endpoint_url", None)
        self.aws_access_key_id = kwargs.get("aws_access_key_id", None)
        self.aws_secret_access_key = kwargs.get("aws_secret_access_key", None)
        self.aws_session_token = kwargs.get("aws_session_token", None)
        self.config = kwargs.get("config", None)

    def get_session(self):
        session = boto3.session.Session()

        return session.client(
            service_name=self.service_name,
            region_name=self.region_name,
            api_version=self.api_version,
            use_ssl=self.use_ssl,
            verify=self.verify,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token,
            config=self.config
        )


class Connection:
    """
    This class use the singleton pattern to provide too
    much connection to the s3 server.

    Parameters:
        auth: An Auth object to provide all the information required
              to establish the connection with the server.
    """

    conn = None

    def __new__(cls, auth: Auth) -> BaseClient:
        if cls.conn is None:
            cls.conn = boto3.resource(
                service_name=auth.service_name,
                region_name=auth.region_name,
                api_version=auth.api_version,
                use_ssl=auth.use_ssl,
                verify=auth.verify,
                endpoint_url=auth.endpoint_url,
                aws_access_key_id=auth.aws_access_key_id,
                aws_secret_access_key=auth.aws_secret_access_key,
                aws_session_token=auth.aws_session_token,
                config=auth.config
            )
        return cls.conn


class Requests:
    def __init__(self, auth: Auth):
        self.conn = Connection(auth)
        self.auth = auth

    def list_buckets(self):
        return self.conn.buckets.all()

    def list_objects(self, name):
        return self.conn.Bucket(name).objects.all()

    def get_temp_url(self, bucket, name):
        s3_api = self.auth.get_session()
        return s3_api.generate_presigned_url(
            'get_object', Params={
                'Bucket': bucket,
                'Key': name
            },
            ExpiresIn=3600
        )

    def get_obj(self, bucket, name):
        return self.conn.Object(
            bucket_name=bucket,
            key=name
        )


def check_args(*args):
    return len(args) > 0 and isinstance(
        args[0],
        int
    ) and args[0] > 0


class Download(io.BytesIO):
    def __init__(self, s3_object, chunk_size: int):
        self.s3_object = s3_object
        self._chunk_size = chunk_size
        self._req = None
        self._iter = None
        self._buff = bytearray(0)

    @property
    def size(self):
        return self.s3_object.content_length

    def __init_request(self):
        if self._req is None:
            self._req = self.s3_object.get()

    def __init_generator(self):
        self.__init_request()
        if self._iter is None:
            self._iter = iter(
                lambda: self._req['Body'].read(self._chunk_size), b'')

    def getvalue(self) -> bytes:
        self.__init_request()
        return self._req['Body'].read()

    def read(self, *args, **kwargs):
        self.__init_request()
        if not check_args(*args):
            return self.getvalue()
        self.__init_generator()
        try:
            self._buff.extend(bytearray(next(self._iter)))
            res = self._buff[0:args[0]]
            del (self._buff[0:args[0]])
            return bytes(res)
        except StopIteration:
            if len(self._buff) > 0:
                if args[0] < len(self._buff):
                    res = self._buff[0:args[0]]
                    del (self._buff[0:args[0]])
                    return bytes(res)
                else:
                    return bytes(self._buff)
            else:
                return bytes(0)

    def readable(self):
        return True

    def seekable(self) -> bool:
        return False
