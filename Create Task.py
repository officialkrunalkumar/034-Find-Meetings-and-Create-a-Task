import os, requests, ast, time

def main(event):
  
  token = os.getenv("RevOps")
  
  url = 'https://api.hubapi.com/crm/v3/objects/tasks'
  
  headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
  }
  
  ownerIds = event.get("inputFields").get("ownerIds")
  
  ownerList = ast.literal_eval(ownerIds)
  
  #ownerList = ["68733528"]
  
  for owner in ownerList:
    task_data = {
      "properties": {
        "hs_task_body": "Please add the meeting title and/or meeting outcome for the meeting you have done.",
        "hs_task_status": "NOT_STARTED",
        "hs_task_priority": "HIGH",
        "hubspot_owner_id": owner,
        "hs_task_subject": "Add missing data",
        "hs_timestamp": str(int(time.time() * 1000))
      }
    }
    
    response = requests.post(url, headers=headers, json=task_data)
    if response.status_code == 201:
      print("Task created successfully!")
    else:
      print(f"Error: {response.status_code}, {response.text}")
  
  return {
    "outputFields": {
      
    }
  }