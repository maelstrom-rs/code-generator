from dotenv import load_dotenv
from github import Github
from jsonpath_ng import jsonpath, parse
import json
import os


load_dotenv()

token = os.getenv("GH_API_TOKEN")
repo_name = os.getenv("GH_REPO")

g = Github(token)
r = g.get_repo(repo_name)
print(r.name)


with open("specs/api-docs.json", 'r') as json_file:
    json_data = json.load(json_file)

p = parse('$.paths.*.*')

for match in p.find(json_data):
    opid = parse('operationId').find(match.value)[0].value
    desc = parse('description').find(match.value)
    if len(desc) > 0:
        desc = desc[0].value
    else:
        desc = ""
    tag = parse("tags[0]").find(match.value)[0].value
    summary = parse("summary").find(match.value)[0].value

    title = tag + ": " + opid
    body = summary + "\n\n" + desc

    print("%s\n%s" % (title, body) )
    r.create_issue(title=title, body=body)
    
