import requests
import json

username = "iamyatinsinghal"
apistring = f"https://api.github.com/users/{username}/repos"
key = ""
headers = {"Authorization": f"Bearer {key}"}
jsonresponse = requests.get(apistring, headers=headers).json()
# print(jsonresponse)
# code to create a new json file and save data of API 
# with open("t.json",'w') as f:
#     f.write(json.dumps(jsonresponse, indent = 3))


best_repos = list()
all_repos = list()
c = 1
for repos in jsonresponse:
    if repos["fork"] == False and repos["name"] != username:
        repo_name = repos["name"]
        if repos["description"] != None:
            best_repos.append(
                {
                    "name": repos["name"],
                    "description": repos["description"],
                }
            )
            c += 1
        else:
            all_repos.append({"name": repos["name"]})

if len(best_repos) < 6:
    for i in range(0, len(all_repos)):
        repo_dict = all_repos[i]
        repo_name = repo_dict["name"]
        repo_url = f"https://api.github.com/repos/{username}/{repo_name}/contributors"
        # print(repo_url)
        try:
            repojson = requests.get(repo_url, headers=headers).json()
            # print(repojson)
            # print(repojson[0]["contributions"])
            all_repos[i].update({"commits": repojson[0]["contributions"]})
        except:
            all_repos[i].update({"commits": 0})
    all_repos.sort(key=lambda r: r["commits"], reverse=True)
    all_repos = all_repos[:6]
    # print(all_repos)
    for j in range(len(best_repos), len(all_repos)):
        repo_name = all_repos[j]["name"]
        languages_used = list()
        languagejson = requests.get(
            f"https://api.github.com/repos/{username}/{repo_name}/languages",
            headers=headers,
        ).json()
        # print(languagejson)
        for key in languagejson:
            languages_used.append(key)

        desc = "This project is made using "
        if len(languages_used) == 0:
            desc += "None."
        else:
            desc += str(languages_used[0])
        if len(languages_used) == 1:
            desc += "."
        elif len(languages_used) > 1:
            for i in range(1, len(languages_used) - 1):
                desc = desc + ", " + str(languages_used[i])
            desc = desc +", " + str(languages_used[-1]) + "."
        # all_repos[j].update({"languages_used": languages_used})
        best_repos.append({
            "name": repo_name,
            "description": desc,
        })

    print(best_repos)
