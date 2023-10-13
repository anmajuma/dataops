import pandas as pd
import json
from lakeFSconn import *
import sys

client = lakeFs_client()

environment = 'dev' # Using environment as a variable FFU, see at end of this guide
rawRepo = environment + "-raw"
featureBranch = sys.argv[-1]
fpath = 'raw/data.txt'
print(featureBranch)

with (
        client.objects.get_object(repository=rawRepo, ref=featureBranch, path=fpath) as f,
        open('data.txt', "wb") as o
    ):
    o.write(f.read())


with open('data.txt', 'r', encoding='utf8') as f:
    jsdata = json.load(f)


intervals = jsdata['data']['timelines'][0]['intervals']
df = pd.DataFrame([x['values'] for x in intervals])

weather_code_map = {0: 'Unknown',
1000: 'Clear',
1001: 'Cloudy',
1100: 'Mostly Clear',
1101: 'Partly Cloudy',
1102: 'Mostly Cloudy',
2000: 'Fog',
2100: 'Light Fog',
3000: 'Light Wind',
3001: 'Wind',
3002: 'Strong Wind',
4000: 'Drizzle',
4001: 'Rain',
4200: 'Light Rain',
4201: 'Heavy Rain',
5000: 'Snow',
5001: 'Flurries',
5100: 'Light Snow',
5101: 'Heavy Snow',
6000: 'Freezing Drizzle',
6001: 'Freezing Rain',
6200: 'Light Freezing Rain',
6201: 'Heavy Freezing Rain',
7000: 'Ice Pellets',
7101: 'Heavy Ice Pellets',
7102: 'Light Ice Pellets',
8000: 'Thunderstorm'}

df['weatherCode'] = [weather_code_map[x] for x in df['weatherCode']]
df.to_csv("weather_cleased.csv",index=False)

environment = 'dev' # Using environment as a variable FFU, see at end of this guide
cleasnsedRepo = environment + "-cleansed"
cleasnsedStorageNamespace = 'https://demo343.blob.core.windows.net/dataops/' + environment + '-cleansed'
mainBranch = 'main'
featureBranch = sys.argv[-1]
print(featureBranch)

# Using Python Client, see full example on the sample repo
try:
    client.repositories.create_repository(
        repository_creation=models.RepositoryCreation(
            name=cleasnsedRepo,
            storage_namespace=cleasnsedStorageNamespace,
            default_branch=mainBranch))
except:
    pass

client.branches_api.create_branch(repository=cleasnsedRepo, branch_creation=models.BranchCreation(name=featureBranch, source=mainBranch))

with open('weather_cleased.csv', 'rb') as f:
    client.objects_api.upload_object(repository=cleasnsedRepo, branch=featureBranch, path='cleansed/weather_cleased.csv', content=f)

client.commits_api.commit(
    repository=cleasnsedRepo,
    branch=featureBranch,
    commit_creation=models.CommitCreation(message='Added a cleased weather data', metadata={'using': 'python_api'}))
