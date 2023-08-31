import json
import requests
# import os
from home.models import users_data

def api_call(git,linked,request):
    data_dic = {}
    data_dic["success"] = 1
    # for linkedin data

    # making request to get data 
    url = "https://linkedin-profiles-and-company-data.p.rapidapi.com/profile-details"

    username = linked

    payload = {
        "profile_id": username,
        "profile_type": "personal",
        "contact_info": False,
        "recommendations": False,
        "related_profiles": False
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "8be347dd0bmshcf0913c6d6c424fp1af42fjsncd6106c89176",
        "X-RapidAPI-Host": "linkedin-profiles-and-company-data.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # convert json to python dict 
    json_obj = json.loads(response.content)
    # print(type(json_obj))
    # print(json.dumps(json_obj, indent = 3))

    
    # Creating new dict to save data in more understandable form 
    

    try:
        data_dic["Name"] = json_obj["first_name"] + " " + json_obj["last_name"]
        data_dic["Summary"] = json_obj["summary"]

        # divide skills into language, frameworks, other 
        # divide skills into language, frameworks, other 
        lang = ["c","c++","java","python","javascript","kotlin","html","css","html5","css3","php","r",'python (programming Language)','cascading style sheets (css)','c (programming language)','html5','sql','ruby',"swift"]
        liby_and_fram =  ['bootstrap','django','react.js','flutter','angularjs','.net framework','angular','flask','node.js','angular.js','vue.js','tailwind css','jQuery','spring framework','hibernate','spring boot','spring mvc',"jquery"]
        other =  ["microsoft powerPoint","microsoft office","adobe photoshop","microsoft word","microsoft excel",
        "adobe illustrator","adobe indesign","machine learning","data analysis","data science","big data","software developement","graphic developement","digital marketing","event management","project management","microsoft azure","problem solving","video editing","communication"]


        temp = {'language' : [], 'library_and_framework' : [] , 'other' : []}
        for i in json_obj["skills"]:
            if i.lower() in lang:
                temp["language"].append(i)
            elif i.lower() in liby_and_fram:
                temp["library_and_framework"].append(i)
            elif i.lower() in other:
                temp["other"].append(i)
        temp["language"].sort()
        temp["library_and_framework"].sort()
        temp["other"].sort()
        data_dic['skills'] = temp

        # Extract Education 

        edu_dic = []
        for i in json_obj["education"]:
            temp_edu = {}
            degree_name = i["degree_name"]
            field_of_study = i["field_of_study"]

            if (degree_name) and ( field_of_study):
                temp_edu["Degree"] = degree_name + ", " + field_of_study
            elif (not degree_name) and field_of_study:
                temp_edu["Degree"] = field_of_study
            elif (not field_of_study) and degree_name:
                temp_edu["Degree"] = degree_name
            else:
                temp_edu["Degree"] = ""

            school_name = str(i["school"]["name"])
            if not school_name:
                school_name = ""
            
            start_year = str(i["date"]["start"]["year"])
            end_year = str(i["date"]["end"]["year"])
            # print(start_year)
            if start_year!="None" and end_year!="None" and school_name != "":
                temp_edu["College"] = school_name + " (" + start_year + " - " + end_year + ")"
            elif school_name !="":
                temp_edu["College"] = school_name
            else:
                temp_edu["College"] =  ""

            edu_dic.append(temp_edu)

        data_dic["Education"] = edu_dic

        # Experience
        exp_dic = []
        for i in json_obj["position_groups"]:
            temp_exp = {}
            temp_exp["title"] = i["profile_positions"][0]["title"]
            start = f'''{i["profile_positions"][0]["date"]["start"]["month"]}/{i["profile_positions"][0]["date"]["start"]["year"]}'''
            end = "Present"
            end_year = i["profile_positions"][0]["date"]["end"]["year"]
            end_month = i["profile_positions"][0]["date"]["end"]["month"]
            if end_year and end_month:
                end = f'''{i["profile_positions"][0]["date"]["end"]["month"]}/{i["profile_positions"][0]["date"]["end"]["year"]}'''
            temp_exp["company"] = i["company"]["name"]
            temp_exp["start"] = start
            temp_exp["end"] = end
            exp_dic.append(temp_exp)
            
        data_dic["Experience"] = exp_dic
        data_dic["Acquirements"] = []
        data_dic["position_of_responsibility"] = []
        #print(data_dic)

        # print data_dic for testing
        # print(json.dumps(data_dic, indent = 3))
    except:
        # print("Data can not be retrived")
        data_dic["success"] = 0

    # fetch github data 
    # username="Akshay2002Singh"
    git_key = ""
    with open("gat_key.txt","r") as f:
        git_key = f.read()
        git_key = git_key.strip()
        print(git_key)

    username = git
    apistring=f"https://api.github.com/users/{username}/repos"
    headers={"Authorization":f"Bearer {git_key}"}
    try:
        jsonresponse=requests.get(apistring,headers=headers).json()
        print("hello")
        best_repos = list() 
        all_repos = list()
        c = 1
        for repos in jsonresponse:
            repo_name = repos["name"]
            repo_url = f"https://api.github.com/repos/{username}/{repo_name}/contributors"
            if repo_name==username:
                pass
            try:
                repojson = requests.get(repo_url, headers=headers).json()
                commits=repojson[0]["contributions"]
            except:
                commits=0
            # print(repo_url)

            if repos["fork"] == False and repos["name"] != username:
                repo_name = repos["name"]
                if repos["description"] != None:
                    best_repos.append(
                        {
                            "name": repos["name"],
                            "description": repos["description"],
                            "commits":commits
                        }
                    )
                    c += 1
                all_repos.append({"name": repos["name"],"commits":commits})


        all_repos.sort(key=lambda r: r["commits"], reverse=True)
        best_repos.sort(key=lambda r: r["commits"], reverse=True)

        if len(best_repos) < 6:
            for i in range(0, len(all_repos)):

            # print(all_repos)
                for j in range(len(best_repos), len(all_repos)):
                    repo_name = all_repos[j]["name"]
                    repo_commits=all_repos[j]["commits"]
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
                        "commits":repo_commits
                    })
                # print(best_repos)
                # print(all_repos)
        
        data_dic["Projects"] = best_repos[:6]
    except:
        data_dic["success"] = 0
    # print(json.dumps(data_dic, indent = 3))
    # return data_dic
    temp = users_data.objects.get(f_key=request.user)
    temp.data = json.dumps(data_dic) 
    temp.fetch_done = 1
    temp.save()
# api_call("Akshay2002Singh","akshay-singh-elite","asdfads")
