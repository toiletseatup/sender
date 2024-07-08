def extract_domain(email):
    """Extract the domain from an email address."""
    return email.split('@')[1]

def format_reply_to(name):
    """Format the ReplyTo field as 'firstname.middle.lastname', ensuring no extra periods are added and all lowercase."""
    parts = name.split(' ')
    lowercase_parts = [part.lower() for part in parts]
    reply_to = '.'.join(lowercase_parts)
    
    # Ensure there are no extra periods
    reply_to = reply_to.replace('..', '.')
    return reply_to

def process_file(input_file, output_file, skipped_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile, \
         open(skipped_file, 'w', encoding='utf-8') as skipfile:
        
        # Write the header to the output file
        outfile.write("email | name | company | full_domain | reply_to | ceo\n")
        
        for line in infile:
            # Strip any leading/trailing whitespace
            line = line.strip()
            
            # Check if the line contains the expected delimiter ' | '
            if ' | ' in line:
                try:
                    # Split the line into email, name, and company
                    email, name, company = line.split(' | ')
                    
                    # Extract the full domain
                    full_domain = extract_domain(email)
                    
                    # Format the ReplyTo field
                    reply_to = format_reply_to(name)
                    
                    # Create the CEO email address
                    ceo_email = f"{reply_to}@{full_domain}"
                    
                    # Write the new line to the output file in the desired format
                    outfile.write(f"{email} | {name} | {company} | {full_domain} | {reply_to} | {ceo_email}\n")
                except Exception as e:
                    # Write the problematic line to the skipped file
                    skipfile.write(f"{line}\n")
            else:
                # Write lines that do not match the expected format to the skipped file
                skipfile.write(f"{line}\n")

# Define the input, output, and skipped file paths
input_file = 'input.txt'
output_file = 'ReplytoOutput.txt'
skipped_file = 'ReplyToskipped.txt'

# Process the file
process_file(input_file, output_file, skipped_file)
