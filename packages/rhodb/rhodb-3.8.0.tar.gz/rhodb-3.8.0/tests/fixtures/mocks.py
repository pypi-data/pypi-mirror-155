from copy import copy

class MockS3Client(object):

    _objects = {}

    def list_objects(self, Bucket, Delimiter=None, Prefix=None):
        if not Prefix:
            return {'Contents': self._objects[Bucket]}

        objs = []
        for key, obj in self._objects[Bucket].iteritems():
            if key.startsWith(Prefix):
                objs.append(obj)
        return {'Contents': objs}

    def put_object(self, Bucket, Key, Body, Metadata=None):
        if Bucket not in self._objects:
            self._objects[Bucket] = {}

        self._objects[Bucket][Key] = {
            'body': Body,
            'metadata': Metadata
        }

    def upload_file(self, Filename, Bucket, Key, ExtraArgs=None, Callback=None,
                    Config=None):
        # Filename is a StringIO instance. Easier for testing than actually
        # creating a file.
        self.put_object(Bucket, Key, Body=Filename.getvalue())

    def get_object(self, Bucket, Key):
        return self._objects[Bucket][Key]

    def delete_object(self, Bucket, Key):
        obj = self.get_object(Bucket, Key)
        del self._objects[Bucket][Key]
        return obj

    def delete_objects(self, Bucket, Delete):
        objs = []
        for key in Delete['Objects']:
            objs.append(self.delete_object(Bucket, key))

        return objs

    def head_object(self, Bucket, Key):
        return self.get_object(Bucket, Key)['metadata']

    def copy_object(self, Bucket, Key, CopySource, Metadata=None,
                    MetadataDirective='COPY'):
        bucket, key = CopySource.split('/')
        obj = self.get_object(bucket, key)
        new_obj = copy(obj)
        if Metadata:
            new_obj['metadata'] = Metadata

        self.put_object(Bucket, Key, Body=new_obj['body'],
                        Metadata=new_obj['metadata'])
        return {}


class MockBotoSession(object):
    def __init__(self, *args, **kwargs):
        pass

    def client(self, service_name):
        return MockS3Client()
