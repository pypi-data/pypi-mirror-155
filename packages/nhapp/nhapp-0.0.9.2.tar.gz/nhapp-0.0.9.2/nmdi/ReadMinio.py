from importlib.resources import read_text
from minio import Minio
import pandas as pd
from io import BytesIO
def readcsv(ACCESS_KEY,PRIVATE_KEY,BUCKET_NAME,OBJECT_NAME):
    client = Minio(
        "apilakedpa.apps.xplat.fis.com.vn",
        access_key=ACCESS_KEY,
        secret_key=PRIVATE_KEY,
        secure = True
        )

    obj = client.get_object(BUCKET_NAME,OBJECT_NAME)

    de = pd.read_csv(obj)

    print(de)

def writecsv(ACCESS_KEY,PRIVATE_KEY,BUCKET_NAME_IN,OBJECT_NAME_IN,BUCKET_NAME_OUT,OBJECT_NAME_OUT):
    client = Minio(
        "apilakedpa.apps.xplat.fis.com.vn",
        access_key=ACCESS_KEY,
        secret_key=PRIVATE_KEY,
        secure = True
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

def readtext(ACCESS_KEY,PRIVATE_KEY,BUCKET_NAME,OBJECT_NAME):
    client = Minio(
        "apilakedpa.apps.xplat.fis.com.vn",
        access_key=ACCESS_KEY,
        secret_key=PRIVATE_KEY,
        secure = True
        )

    obj = client.get_object(BUCKET_NAME,OBJECT_NAME)

    df = pd.read_csv(obj)

    print(df)

def writetext(ACCESS_KEY,PRIVATE_KEY,BUCKET_NAME_IN,OBJECT_NAME_IN,BUCKET_NAME_OUT,OBJECT_NAME_OUT):
    client = Minio(
        "apilakedpa.apps.xplat.fis.com.vn",
        access_key=ACCESS_KEY,
        secret_key=PRIVATE_KEY,
        secure = True
        )

    obj = client.get_object(BUCKET_NAME_IN, OBJECT_NAME_IN)

    df = pd.read_csv(obj)

    csv = df.to_csv().encode('utf-8')

    client.put_object(
    BUCKET_NAME_OUT,
    OBJECT_NAME_OUT,
    data=BytesIO(csv),
    length=len(csv),
    content_type='example.txt'
    )

def read_list(ACCESS_KEY, PRIVATE_KEY):
    client = Minio(
        "apilakedpa.apps.xplat.fis.com.vn",
        access_key=ACCESS_KEY,
        secret_key=PRIVATE_KEY,
        secure = True
        )

    a = client.list_buckets()    
    print(a)


