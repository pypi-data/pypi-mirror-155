from minio import Minio
import os
import io
import base64
from io import BytesIO
import hashlib

class PyMinio:
    def __init__(self, host, port, access_key, secret_key, secure=False):
        self.client = Minio(
            "{}:{}".format(host, port),
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )

    def set_bucket(self, bucket):
        self.bucket = bucket

    def _trim_bucket(self, object_name:str, *, trim:bool) -> str:
        if object_name[0]=='/':
            object_name = object_name[1:]
            
        # 去掉前面的桶的名字
        if trim==True:
            arr = object_name.split('/')[1:]
            object_name = os.path.join(*arr)

        return object_name

    def download(self, object_name:str, local_name:str, *, trim:bool=False) -> bool:
        object_name = self._trim_bucket(object_name, trim=trim)

        if self.exists(object_name):
            self.client.fget_object(self.bucket, object_name, local_name)
            return True
        else:
            return False

    def upload(self, file_path:str, object_name:str) -> bool:
        if self.client.bucket_exists(self.bucket) == False:
            self.client.make_bucket(self.bucket)  # 生成一个bucket，类似文件夹

        self.client.fput_object(
            bucket_name=self.bucket,
            object_name=object_name,
            file_path=file_path
        )
        return True

    def write(self, object_name, content:bytes):
        self.client.put_object(self.bucket, object_name, io.BytesIO(content), len(content))

    def exists(self, object_name:str, *, trim:bool=False) -> bool:
        object_name = self._trim_bucket(object_name, trim=trim)

        try:
            response = self.client.get_object(self.bucket, object_name)
            response.close()
            response.release_conn()
            return True
        except Exception as e:
            return False

    # 删除对象
    def remove_file(self, object_name:str, *, trim:bool=False) -> bool:
        object_name = self._trim_bucket(object_name, trim=trim)
        try:
            self.client.remove_object(self.bucket, object_name)
            #print("Sussess")
            return True
        except Exception as err:
            #print(err)
            return False

    def get_client(self) -> Minio:
        return self.client

    def upload_image(self, image_base64:str, *, object_name=None, filetype=None, bucket=None):
        partition = image_base64.find(",")
        if partition > 0:
            image_base64 = image_base64[partition:]
        else:
            image_base64 = image_base64
        image_data = base64.b64decode(image_base64)

        if object_name!=None and object_name[0]=='/':
            object_name = object_name[1:]

        if bucket==None:
            bucket = self.bucket

        if self.client.bucket_exists(bucket) == False:
            self.client.make_bucket(bucket)  # 生成一个bucket，类似文件夹

        #
        if object_name==None:
            if filetype==None:
                import imghdr

                # 通过二进制内容获取图片格式
                filetype = imghdr.what(None, image_data)
                if filetype==None:
                    filetype = "unknown"

            hash_md5 = hashlib.md5()
            hash_md5.update(image_data)
            image_name = hash_md5.hexdigest()
            object_name = "{}/{}.{}".format(image_name[:2], image_name[2:], filetype)

        result = self.client.put_object(bucket, object_name, BytesIO(image_data), len(image_data))

        if result!=None:
            return "{}/{}".format(bucket, object_name)
        else:
            return None
        
