class UploadResult:

    def __init__(self, bucket_name, object_name):
        self.bucket_name = bucket_name
        self.object_name = object_name

    def to_response(self):
        return {"bucket_name": self.bucket_name, "object_name": self.object_name}

    def __eq__(self, o: object) -> bool:
        if isinstance(o, UploadResult):
            return (self.bucket_name, self.object_name) == (
                o.bucket_name,
                o.object_name,
            )
        return False
