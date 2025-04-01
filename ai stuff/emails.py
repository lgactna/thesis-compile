import re
import os
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import uuid
import base64

def extract_emails(input_file):
    """Extract emails from the input file and return a list of email data."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match emails formatted with triple backticks
    email_pattern = r'```\s*\nTO:\s*([^\n]+)\s*\nFROM:\s*([^\n]+)\s*\n\s*\n(.*?)```'
    emails = re.findall(email_pattern, content, re.DOTALL)
    
    email_data = []
    for to_addr, from_addr, body in emails:
        email_data.append({
            'to': to_addr.strip(),
            'from': from_addr.strip(),
            'body': body.strip()
        })
    
    return email_data

def create_eml_file(emails, output_dir):
    """Create a single .eml file representing the email chain."""
    if not emails:
        print("No emails found to process.")
        return
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate message IDs for each email
    message_ids = [f"<{uuid.uuid4()}@domain.com>" for _ in range(len(emails))]
    
    # Generate timestamps for each email (going from past to present)
    base_date = datetime.now() - timedelta(days=len(emails))
    timestamps = [base_date + timedelta(days=i) for i in range(len(emails))]
    
    # Create the main multipart message
    main_msg = MIMEMultipart('mixed')
    main_msg['Subject'] = "Semiconductor Manufacturing Product Discussion"
    main_msg['From'] = emails[-1]['from']
    main_msg['To'] = emails[-1]['to']
    main_msg['Date'] = email.utils.formatdate(float(timestamps[-1].timestamp()), localtime=True)
    main_msg['Message-ID'] = message_ids[-1]
    
    # Add References header (all previous message IDs)
    if len(emails) > 1:
        main_msg['References'] = " ".join(message_ids[:-1])
        main_msg['In-Reply-To'] = message_ids[-2]  # The message being replied to
    
    # Create the main message part (latest email)
    main_part = MIMEMultipart('alternative')
    
    # First add the latest email content
    text_content = emails[-1]['body']
    
    # Now build the thread by adding previous emails as quoted parts
    full_thread = text_content
    
    # Add previous emails as quoted text, from newest to oldest
    for i in range(len(emails)-2, -1, -1):
        date_str = email.utils.formatdate(float(timestamps[i].timestamp()), localtime=True)
        quoted_header = f"\n\nOn {date_str}, {emails[i]['from']} wrote:\n"
        quoted_body = "\n".join([f"> {line}" for line in emails[i]['body'].split('\n')])
        full_thread += quoted_header + quoted_body
    
    # Add the full thread to the message
    text_part = MIMEText(full_thread, 'plain')
    main_part.attach(text_part)
    main_msg.attach(main_part)
    
    # Create an HTML version with proper formatting
    # html_content = f"<html><body><p>{full_thread.replace(chr(92), '<br/>')}</p></body></html>"
    # html_part = MIMEText(html_content, 'html')
    # main_part.attach(html_part)
    
    # Write the .eml file
    sender_id = emails[-1]['from'].split('@')[0]
    filename = f"{output_dir}/email_chain_{sender_id}.eml"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(main_msg.as_string())
    
    print(f"Email chain saved to {filename}")
    
    # Additionally, create individual .eml files for each email in the chain
    for i, email_data in enumerate(emails):
        msg = MIMEMultipart()
        msg['Subject'] = "Semiconductor Manufacturing Product Discussion"
        msg['From'] = email_data['from']
        msg['To'] = email_data['to']
        msg['Date'] = email.utils.formatdate(float(timestamps[i].timestamp()), localtime=True)
        msg['Message-ID'] = message_ids[i]
        
        # Add references to previous emails
        if i > 0:
            msg['References'] = " ".join(message_ids[:i])
            msg['In-Reply-To'] = message_ids[i-1]
            
        # Add email body
        msg.attach(MIMEText(email_data['body'], 'plain'))
        
        # Create individual email file
        sender = email_data['from'].split('@')[0]
        ind_filename = f"{output_dir}/email_{i+1}_{sender}.eml"
        
        with open(ind_filename, 'w', encoding='utf-8') as f:
            f.write(msg.as_string())
        
        print(f"Individual email saved to {ind_filename}")

def main():
    input_file = os.path.join(os.path.dirname(__file__), 'emails.txt')
    output_dir = os.path.join(os.path.dirname(__file__), 'extracted_emails')
    
    emails = extract_emails(input_file)
    if emails:
        print(f"Found {len(emails)} emails in the input file.")
        create_eml_file(emails, output_dir)
    else:
        print("No emails found in the specified format.")

if __name__ == "__main__":
    main()