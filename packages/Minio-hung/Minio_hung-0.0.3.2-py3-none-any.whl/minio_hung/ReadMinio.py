from minio import Minio
import pandas as pd
from io import BytesIO
def readcsv(ACCESS_KEY,PRIVATE_KEY,BUCKET_NAME,OBJECT_NAME):
    client = Minio(
        "lakedpaapi-fis-mbf-dplat.apps.xplat.fis.com.vn",
        access_key=ACCESS_KEY,
        secret_key=PRIVATE_KEY,
        secure = False
        )

    obj = client.get_object(BUCKET_NAME,OBJECT_NAME)

    de = pd.read_csv(obj)

    print(de)

def writecsv(ACCESS_KEY,PRIVATE_KEY,BUCKET_NAME_IN,OBJECT_NAME_IN,BUCKET_NAME_OUT,OBJECT_NAME_OUT):
    client = Minio(
        "lakedpaapi-fis-mbf-dplat.apps.xplat.fis.com.vn",
        access_key=ACCESS_KEY,
        secret_key=PRIVATE_KEY,
        secure = False
        )

    obj = client.get_object(BUCKET_NAME_IN, OBJECT_NAME_IN)

    df = pd.read_csv(obj)

    csv = df.to_csv().encode('utf-8')

    client.put_object(
    BUCKET_NAME_OUT,
    OBJECT_NAME_OUT,
    data=BytesIO(csv),
    length=len(csv),
    content_type='example.csv'
)   

def read_list(ACCESS_KEY, PRIVATE_KEY):
    client = Minio(
        "lakedpaapi-fis-mbf-dplat.apps.xplat.fis.com.vn",
        access_key=ACCESS_KEY,
        secret_key=PRIVATE_KEY,
        secure = False
        )

    a = client.list_buckets()    
    print(a)


