# Script: update_csv_from_mailchimp.py
# Fetch audience data from mailchimp and update local csv

import csv
from dotenv import load_dotenv
import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

load_dotenv()

# AUTH
api_key = os.getenv("MAILCHIMP_API_KEY")
server_prefix = os.getenv("MAILCHIMP_SERVER_PREFIX") # specify server location
list_id = os.getenv("MAILCHIMP_LIST_ID") # specify audience ID here
csv_filename = os.getenv("LOCAL_PC_LOCATION") # file you are using to sync

client_mailchimp = MailchimpMarketing.Client()
client_mailchimp.set_config({
    "api_key": api_key,
    "server": server_prefix
})

def fetch_mailchimp_list_members(list_id, count=200):
    members_data = []
    try:
        response = client_mailchimp.lists.get_list_members_info(list_id, count=count)
        members = response['members']
        for member in members:
            # Extract tag names from the tags list
            tags = [tag['name'] for tag in member['tags']]
            # Join tags into a single string, comma seperated
            tags_str = ', '.join(tags)
            members_data.append({
                "Email": member['email_address'],
                "FirstName": member['merge_fields'].get('FNAME', ''),
                "LastName": member['merge_fields'].get('LNAME', ''),
                "Tags": tags_str  # Add the tags as a string
            })
        return members_data
    except ApiClientError as error:
        print("An error occurred:", error.text)
        return None

def update_csv(csv_filename, members_data):
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Email', 'FirstName', 'LastName','Tags']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for member in members_data:
            writer.writerow(member)

def main():
    members_data = fetch_mailchimp_list_members(list_id)
    if members_data:
        update_csv(csv_filename, members_data)
        print(f"CSV file '{csv_filename}' has been updated with Mailchimp list members.")
    else:
        print("Failed to fetch members data.")

if __name__ == "__main__":
    main()
