import json
import requests

# making request to get data 
url = "https://linkedin-profiles-and-company-data.p.rapidapi.com/profile-details"

username = "yatin-singhal-838594201"

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

# code to create a new json file and save data of API 
# with open("t.json",'w') as f:
#     f.write(json.dumps(json_obj, indent = 3))



# Creating new dict to save data in more understandable form 
data_dic = {}


data_dic["Name"] = json_obj["first_name"] + " " + json_obj["last_name"]
data_dic["Summary"] = json_obj["summary"]

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


# print data_dic for testing
print(json.dumps(data_dic, indent = 3))