import csv
from dotenv import load_dotenv
import os
import mailchimp_marketing as MailchimpMarketing
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm # progress bar
from mailchimp_marketing.api_client import ApiClientError

load_dotenv()

api_key = os.getenv("MAILCHIMP_API_KEY")
server_prefix = os.getenv("MAILCHIMP_SERVER_PREFIX")
list_id = os.getenv("MAILCHIMP_LIST_ID")
csv_filename = os.getenv("LOCAL_PC_LOCATION")

client_mailchimp = MailchimpMarketing.Client()
client_mailchimp.set_config({
    "api_key": api_key,
    "server": server_prefix
})

def get_contacts_data(csv_filename):
    """Read contacts and their tags from a CSV file."""
    contacts_data = []
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            tags = [tag.strip() for tag in row['Tags'].split(',') if tag]
            contact = {
                "email_address": row['Email'],
                "status_if_new": "subscribed",
                "merge_fields": {
                    "FNAME": row['FirstName'],
                    "LNAME": row['LastName']
                },
                "tags": tags
            }
            contacts_data.append(contact)
    return contacts_data

def update_contact_basic_info(list_id, contact):
    """Update a single contact's basic information in Mailchimp."""
    try:
        response = client_mailchimp.lists.set_list_member(list_id, contact['email_address'], {
            "email_address": contact['email_address'],
            "status_if_new": contact['status_if_new'],
            "merge_fields": contact['merge_fields']
        })
        return {"email_address": contact['email_address'], "tags": contact['tags']}
    except ApiClientError as error:
        print(f"An error occurred while updating {contact['email_address']}:", error.text)
        return None

def get_current_tags(list_id, email_address):
    """Fetch the current tags for a contact in Mailchimp."""
    try:
        response = client_mailchimp.lists.get_list_member_tags(list_id, email_address)
        return [tag['name'] for tag in response['tags']]
    except ApiClientError as error:
        print(f"An error occurred while fetching tags for {email_address}:", error.text)
        return []

def update_contact_tags(list_id, contact):
    """Update a single contact's tags in Mailchimp to match those specified in the CSV."""
    current_tags = get_current_tags(list_id, contact['email_address'])
    csv_tags = contact['tags']

    # Determine tags to add (present in CSV but not in Mailchimp)
    tags_to_add = [{'name': tag, 'status': 'active'} for tag in csv_tags if tag not in current_tags]
    
    # Determine tags to remove (present in Mailchimp but not in CSV)
    tags_to_remove = [{'name': tag, 'status': 'inactive'} for tag in current_tags if tag not in csv_tags]

    if tags_to_add or tags_to_remove:
        try:
            client_mailchimp.lists.update_list_member_tags(list_id, contact['email_address'], {
                "tags": tags_to_add + tags_to_remove
            })
        except ApiClientError as error:
            print(f"An error occurred while updating tags for {contact['email_address']}:", error.text)

def main():
    contacts_data = get_contacts_data(csv_filename)

    print("Updating basic contact info...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(update_contact_basic_info, list_id, contact): contact for contact in contacts_data}
        contacts_to_update_tags = []
        for future in tqdm(as_completed(futures), total=len(contacts_data), desc="Basic Info"):
            result = future.result()
            if result:
                contacts_to_update_tags.append(result)

    print("\nUpdating contact tags...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        tag_futures = [executor.submit(update_contact_tags, list_id, contact) for contact in contacts_to_update_tags]
        for _ in tqdm(as_completed(tag_futures), total=len(contacts_to_update_tags), desc="Tags"):
            pass

if __name__ == "__main__":
    main()
