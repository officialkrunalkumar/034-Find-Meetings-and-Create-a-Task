import os
from datetime import datetime, timezone, timedelta
import requests

def main(event):
  token = os.getenv("RevOps")
  
  team_id = event.get("inputFields").get("hubspot_team_id")
  
  today = datetime.now(timezone.utc)
  seven_days_earlier = today - timedelta(days=7)
  today_str = today.strftime('%Y-%m-%dT%H:%M:%SZ')
  seven_days_ago_str = seven_days_earlier.strftime('%Y-%m-%dT%H:%M:%SZ')
  
  url = 'https://api.hubapi.com/crm/v3/objects/meetings/search'
  
  controller_id = 8316195
  
  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
  }
  
  filter_groups = [
    {
      "filters" : [
        {
          "propertyName": "hubspot_team_id",
          "operator": "EQ",
          "value": controller_id
        },
        {
          "propertyName": "hs_meeting_start_time",
          "operator": "GTE",
          "value": seven_days_ago_str
        },
        {
          "propertyName": "hs_meeting_start_time",
          "operator": "LTE",
          "value": today_str
        },
        {
          "propertyName": "hs_activity_type",
          "operator": "NOT_HAS_PROPERTY"
        }
      ]
    },
    {
      "filters" : [
        {
          "propertyName": "hubspot_team_id",
          "operator": "EQ",
          "value": controller_id
        },
        {
          "propertyName": "hs_meeting_start_time",
          "operator": "GTE",
          "value": seven_days_ago_str
        },
        {
          "propertyName": "hs_meeting_start_time",
          "operator": "LTE",
          "value": today_str
        },
        {
          "propertyName": "hs_meeting_outcome",
          "operator": "NOT_HAS_PROPERTY"
        }
      ]
    }
  ]
  
  has_more = True
  after = None
  all_results = []
  
  properties = ["hubspot_owner_id", "hs_meeting_title"]
  
  while has_more:
    
    data = {
      "filterGroups": filter_groups,
      "limit": 100,
      "properties": properties
    }
    
    if after:
      data["after"] = after
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
      response_data = response.json()
      all_results.extend(response_data.get("results", []))
      has_more = response_data.get("paging", {}).get("next", False)
      after = response_data.get("paging", {}).get("next", {}).get("after")
    else:
      print(f"Error: {response.status_code} - {response.text}")
      break
  
  #print(all_results[0])
  ownerIds = []
  
  for record in all_results:
    owner_id = record['properties']['hubspot_owner_id']
    ownerIds.append(owner_id)
    
  #print(f"Total records fetched: {len(all_results)}")
  #print(ownerIds)
  
  return {
    "outputFields": {
      "ownerIds": ownerIds
    }
  }