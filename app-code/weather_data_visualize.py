from lakeFSconn import *
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import sys

client = lakeFs_client()

environment = 'dev' # Using environment as a variable FFU, see at end of this guide
cleasnsedRepo = environment + "-cleansed"
featureBranch = sys.argv[-1]
fpath = 'cleansed/weather_cleased.csv'
print(featureBranch)

with (
        client.objects.get_object(repository=cleasnsedRepo, ref=featureBranch, path=fpath) as f,
        open('weather_cleased.csv', "wb") as o
    ):
    o.write(f.read())

df = pd.read_csv("weather_cleased.csv")

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(df.index, df['temperature'], color ='maroon', width = 0.4)
plt.xlabel("Day")
plt.ylabel("Temperature")
plt.savefig("TempPlotByDay", facecolor='g', bbox_inches="tight",
            pad_inches=0.3, transparent=True)
plt.close()

with open('TempPlotByDay.png', 'rb') as f:
    client.objects_api.upload_object(repository=cleasnsedRepo, branch=featureBranch, path='plot/TempPlotByDay.png', content=f)

client.commits_api.commit(
    repository=cleasnsedRepo,
    branch=featureBranch,
    commit_creation=models.CommitCreation(message='Added a weather data plot', metadata={'using': 'python_api'}))
