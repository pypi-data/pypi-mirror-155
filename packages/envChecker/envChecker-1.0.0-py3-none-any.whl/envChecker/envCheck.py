import os
import re
import dotenv

success = True

def check() -> bool:
    if not os.path.exists("./.env.example"):
        print("Unable to detect .env.example.")
        return False
    with open(".env.example", "r") as example:
        matching = {}
        explanations = {}
        req_envs = []
        var_optional = False
        for line in example.readlines():
            if "=" in line and var_optional is not True:
                req_envs.append(line.split("=")[0])
            elif "#OPTIONAL" in line:
                var_optional = True
    missing = []
    dotenv.load_dotenv()
    for env in req_envs:
        value = os.getenv(env)
        if value is None:
            missing.append(env)
            continue
    if len(missing):
        for i in range(len(missing)):
            try:
                missing[i] = missing[i] + ": " + explanations[missing[i]]
            except KeyError:
                pass
        print(f"You are missing the following variables in .env: {missing}")
        success = False
    else:
        success = True

    return success