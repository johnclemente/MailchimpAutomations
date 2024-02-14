<h1>Tool Description</h1>

This suite of Python scripts provides an efficient way to synchronize contact information between a local CSV file and a Mailchimp account. It's designed to help users manage their Mailchimp contacts, including updating names and tags, from the convenience of their local machine. I personally have had a lot of difficulty bulk managing my audience using the current audience manager, so this tool is to help with that!

<h1>Setup</h1>

1. create an .env file in your project directory with the following fields:  
<code>MAILCHIMP_API_KEY=  
MAILCHIMP_SERVER_PREFIX=  
MAILCHIMP_LIST_ID=  
LOCAL_PC_LOCATION=C:/Users/yourpath/MailChimpContacts.csv</code>

2. python installed on PATH or in the same directory as local project repo

3. Prepare Your CSV File: Create a CSV file named MailChimpContacts.csv in the project directory. The CSV should have the following column headers:
<code>Email, FirstName, LastName, Tags</code>

<h1>Synchronize Contacts</h1>
Fetch the current contacts from Mailchimp and update the local CSV file by running:

<code>python update_csv_from_mailchimp.py</code>

After executing this command, you can make any desired modifications directly in the CSV file. The changes will be reflected in Mailchimp when you run the update scripts.

<h1>Script Descriptions</h1>
Below is a brief overview of each script included in this toolset:

<h3>update_mailchimp_names_from_csv.py</h3>
Updates the names of Mailchimp contacts based on the MailChimpContacts.csv file. Ideal for bulk name updates.

<h3>update_csv_from_mailchimp.py</h3>
Fetches the latest data from Mailchimp, including emails, names, and tags, and updates the local MailChimpContacts.csv accordingly. This ensures your local copy is in sync with Mailchimp.

<h3>update_mailchimp_from_csv.py</h3>
Reflects changes made in the MailChimpContacts.csv file in Mailchimp, updating contact names and adding tags. It is efficient but does not remove tags if they are deleted from the CSV.

<h3>Limitations</h3>

<h4>Performance</h4>

Updates are processed sequentially, which may result in longer execution times for large lists. The script employs parallel processing where feasible to enhance performance.

<h4>Error Handling</h4> 

Basic error handling is included, yet users should manually verify synchronization, especially when encountering specific errors from the Mailchimp API, such as rate limits or validation errors.
