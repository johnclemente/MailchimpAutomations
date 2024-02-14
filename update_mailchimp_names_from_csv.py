#python update_mailchimp_names_from_csv.py
import csv
import os
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

api_key = os.getenv("MAILCHIMP_API_KEY")
server_prefix = os.getenv("MAILCHIMP_SERVER_PREFIX")
list_id = os.getenv("MAILCHIMP_LIST_ID")
csv_filename = os.getenv("LOCAL_PC_LOCATION")

client_mailchimp = MailchimpMarketing.Client()
client_mailchimp.set_config({
    "api_key": api_key,
    "server": server_prefix
})

def chunked_contacts_data(contacts, chunk_size=500):
    """Yield successive chunk_size chunks from contacts."""
    for i in range(0, len(contacts), chunk_size):
        yield contacts[i:i + chunk_size]

def add_or_update_contacts_in_mailchimp_list(list_id, contacts):
    for contacts_chunk in chunked_contacts_data(contacts):
        try:
            response = client_mailchimp.lists.batch_list_members(list_id, {
                "members": contacts_chunk,
                "update_existing": True
            })
            print("Batch operation successful. Response:", response)
        except ApiClientError as error:
            print("An error occurred:", error.text)

def get_contacts_data(csv_filename):
    contacts_data = []
    with open(csv_filename, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            contact = {
                "email_address": row['Email'],
                "status_if_new": "subscribed",
                "merge_fields": {
                    "FNAME": row['FirstName'],
                    "LNAME": row['LastName']
                }
            }
            contacts_data.append(contact)
    return contacts_data

def main():
    contacts_data = get_contacts_data(csv_filename)
    add_or_update_contacts_in_mailchimp_list(list_id, contacts_data)

if __name__ == "__main__":
    main()
