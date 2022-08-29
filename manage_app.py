import httpx
import os
from secrets import token_bytes
from base64 import b64encode
import json

def get_current_env_vars(serviceId):
    retreive_current_envs = httpx.get(url="https://api.render.com/v1/services/{service_id}/env-vars".format(service_id=serviceId), headers={"Authorization": f"Bearer {os.environ['RENDER_API_KEY']}"})
    return retreive_current_envs.json()

def get_service_id_and_slug(appName):
    retreive_service_id = httpx.get(url="https://api.render.com/v1/services", headers={"Authorization": f"Bearer {os.environ['RENDER_API_KEY']}"})
    for service in retreive_service_id.json():
        if service["service"]["name"] == appName:
           return {"service_id": service["service"]["id"], "slug": service["service"]["slug"]}

def update_or_add_envars(serviceId, envVars):
    update_env_vars = httpx.put(url="https://api.render.com/v1/services/{service_id}/env-vars".format(service_id=serviceId), headers={"Authorization": f"Bearer {os.environ['RENDER_API_KEY']}"}, json=envVars)
    return update_env_vars.json()

def build_env_vars(appName, serviceSlug):
    staticEnVars = []
    boolsVars = ["I_REALLY_WANT_VOLATILE_STORAGE","ENABLE_DUO"]
    stringsVars = ["ADMIN_TOKEN", "DUO_SKEY", "DUO_IKEY", "DUO_HOST", "DATABASE_URL", "DOMAIN", "SMTP_HOST", "SMTP_FROM", "SMTP_PORT", "SMTP_SECURITY", "SMTP_USERNAME", "SMTP_PASSWORD"]

    for varToAddBools in boolsVars:
        if varToAddBools == "ENABLE_DUO" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": "_ENABLE_DUO", "value": os.environ[varToAddBools]})
        elif varToAddBools == "I_REALLY_WANT_VOLATILE_STORAGE":
            staticEnVars.append({"key": varToAddBools, "value": "true"})
        else:
            continue

    for varToAddBools in stringsVars:
        if varToAddBools == "ADMIN_TOKEN":
            staticEnVars.append({"key": varToAddBools, "value": b64encode(token_bytes(32)).decode()})
        elif varToAddBools == "DUO_SKEY" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": varToAddBools, "value": os.environ[varToAddBools]})
        elif varToAddBools == "DUO_IKEY" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": varToAddBools, "value":  os.environ[varToAddBools]})
        elif varToAddBools == "DUO_HOST" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": varToAddBools, "value": os.environ[varToAddBools]})
        elif varToAddBools == "DATABASE_URL" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": varToAddBools, "value": os.environ[varToAddBools]})
        elif varToAddBools == "DOMAIN":
            staticEnVars.append({"key": varToAddBools, "value": "https://{app_name}-{service_slug}.onrender.com".format(app_name=appName, service_slug=serviceSlug)})
        elif varToAddBools == "SMTP_HOST" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": varToAddBools, "value": os.environ[varToAddBools]})
        elif varToAddBools == "SMTP_FROM" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": varToAddBools, "value": os.environ[varToAddBools]})
        elif varToAddBools == "SMTP_PORT" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": varToAddBools, "value": os.environ[varToAddBools]})
        elif varToAddBools == "SMTP_SECURITY" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": varToAddBools, "value": os.environ[varToAddBools]})
        elif varToAddBools == "SMTP_USERNAME" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": varToAddBools, "value": os.environ[varToAddBools]})
        elif varToAddBools == "SMTP_PASSWORD" and os.environ[varToAddBools] != "":
            staticEnVars.append({"key": varToAddBools, "value": os.environ[varToAddBools]})
        else:
            continue

    return staticEnVars

def kickoff_build(serviceId):
    build = httpx.post(url="https://api.render.com/v1/services/{service_id}/deploys".format(service_id=serviceId), headers={"Authorization": f"Bearer {os.environ['RENDER_API_KEY']}"}, json={"clearCache": "clear"})
    return build.json()

appName = os.environ["APP_NAME"]
serviceDetails = get_service_id_and_slug(appName)
update_or_add_envars(serviceDetails['service_id'], build_env_vars(appName, serviceDetails['slug']))
kickoff_build(serviceDetails['service_id'])