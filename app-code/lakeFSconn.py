import lakefs_client
from lakefs_client import models
from lakefs_client.client import LakeFSClient

def lakeFs_client():
# lakeFS credentials and endpoint
    configuration = lakefs_client.Configuration()
    configuration.username = 'AKIAJJLVIWNDY2ZT27ZQ'
    configuration.password = 'ftb34icGIJu03/wlnBM82m4rAD9b0N+LVCmlm+dz'
    configuration.host = 'https://relaxing-parakeet.eastus.lakefsazcloud.io'
    configuration.verify_ssl = False


    client = LakeFSClient(configuration)
    return client

