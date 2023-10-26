import requests
from lakeFSconn import *
import sys

url = "https://api.tomorrow.io/v4/timelines"

# replace the location using the corresponding lat,long
#location = "47.75,-120.74"  # washington
location = "36.11,-115.17"  # las vegas
environment = 'dev' # Using environment as a variable FFU, see at end of this guide
rawRepo = environment + "-raw"
rawRepoStorageNamespace = 'https://demo343.blob.core.windows.net/dataops/' + environment + '-raw'
mainBranch = 'main'
featureBranch = sys.argv[-1]
print(featureBranch)



# replace apikey with your own API key
querystring = {"location": location, "fields": ["temperature", "humidity", "windSpeed", "windDirection", "windGust", "precipitationType", "solarGHI", "visibility", "weatherCode"],
               "units": "metric", "timesteps": "1d", "apikey": "o3BuPNTgB1yN3ApGJipYyE7PIvPL6LWk"}

response = requests.request("GET", url, params=querystring)

client = lakeFs_client()

# Using Python Client, see full example on the sample repo
try:
    client.repositories.create_repository(
        repository_creation=models.RepositoryCreation(
            name=rawRepo,
            storage_namespace=rawRepoStorageNamespace,
            default_branch=mainBranch))
except:
    pass


# replace the name based on your own preferences
with open('data.txt', 'w', encoding='utf8') as f:
    f.write(response.text)

client.branches_api.create_branch(repository=rawRepo, branch_creation=models.BranchCreation(name=featureBranch, source=mainBranch))
 

with open('data.txt', 'rb') as f:
    client.objects_api.upload_object(repository=rawRepo, branch=featureBranch, path='raw/data.txt', content=f)


client.commits_api.commit(
    repository=rawRepo,
    branch=featureBranch,
    commit_creation=models.CommitCreation(message='Added a weather File', metadata={'using': 'python_api'}))

    
