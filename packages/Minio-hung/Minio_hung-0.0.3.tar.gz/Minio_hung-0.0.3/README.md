
# Minio-hung: Print your .csv file from Minio
## Powered by Ly Duc Hung (FPT Infomation System)

# How to install?
```
pip install Minio-hung
```
## or

Windows
```
py -m pip install Minio-hung
```
Linux/Mac OS
```
python3 -m pip install Minio-hung
```

# What's in package?
```
thuviencuabomay
```

# How to use Minio-hung?

## You can use to one of codes below here:

ACCESS_KEY: Access key in your Services Account.

SECRET_KEY: Secret key in your Services Account.

BUCKET_NAME: Your Bucket name.

OBJECT_NAME: The Object name in your Bucket.

## Print list buckets in Minio
```
#1
import thuviencuabomay

thuviencuabomay.read_list(ACCESS_KEY, PRIVATE_KEY)



#2
from thuviencuabomay import read_list

read_list(ACCESS_KEY, PRIVATE_KEY)

```

## Print .csv file from Minio
```
#1
import thuviencuabomay

thuviencuabomay.read_csv(ACCESS_KEY, SECRET_KEY, BUCKET_NAME, OBJECT_NAME)



#2
from thuviencuabomay import read_csv

read_csv(ACCESS_KEY, SECRET_KEY, BUCKET_NAME, OBJECT_NAME)

```