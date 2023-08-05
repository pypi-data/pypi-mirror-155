from minio import Minio
import pandas as pd
def read_csv(ACCESS_KEY,PRIVATE_KEY,BUCKET_NAME,OBJECT_NAME):
    client = Minio(
        "lakedpaapi-fis-mbf-dplat.apps.xplat.fis.com.vn",
        access_key=ACCESS_KEY,
        secret_key=PRIVATE_KEY,
        secure = False
        )

# client.list_buckets()
# name_bucket = input('Enter your bucket name: ')
# name_object = input('Enter your object name: ')
    obj = client.get_object(BUCKET_NAME,OBJECT_NAME)

    de = pd.read_csv(obj, on_bad_lines='skip')

    print(de)

def read_list(ACCESS_KEY, PRIVATE_KEY):
    client = Minio(
        "lakedpaapi-fis-mbf-dplat.apps.xplat.fis.com.vn",
        access_key=ACCESS_KEY,
        secret_key=PRIVATE_KEY,
        secure = False
        )

    a = client.list_buckets()    
    print(a)