import base64, os

from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document



# Settings

# Fill in these constants

#

# Obtain an OAuth access token from https://developers.docusign.com/oauth-token-generator

access_token = "eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwAAzBZ5glrXSAgAAAw6h8Va10gCAPhn2lOuzL9AnfuEzG3fpvYVAAEAAAAYAAEAAAAFAAAADQAkAAAAZjBmMjdmMGUtODU3ZC00YTcxLWE0ZGEtMzJjZWNhZTNhOTc4EgABAAAACwAAAGludGVyYWN0aXZlMACANX54glrXSDcAUKvOQFlUHEiaEBDQXR19jA.uQGOjQ6Sw91qQgTnOzEENAye6iUMmmmnkJ_xlPSpoEzgpVE_OpSln8S7t5Kk4l_RvluEZZ5pHI-7kl-r0PzVBUUherlmgJGWAueyb0Kb_9K9s7dXp5veYI8xb9B_hjkZQtwU6SzHDWJoaOvYzRgxQJVxu-mpZGs3Db1pWjYe4BnqSLx5vhgLnuHIP34Fmr0O8WCMVYvTggLZHie1mbaHv2WpDn7J_EQc3eDIcarvm6XnkDgNpom9bE6GLfjh7ncuI3ZfA_INAhztn-HrjOXUIxzpFhg6Kb32CABl0ysCWAMX6NDm4XGkDcKFFsZOr0CtWNH-iwU22UvjdJRVYvp5DA"
# Obtain your accountId from demo.docusign.com -- the account id is shown in the drop down on the

# upper right corner of the screen by your picture or the default picture. 

account_id = "e95437ae-f5c1-4d14-a1d5-ed1f249156ac"
# Recipient Information:

signer_name = "Sharon Lee"
signer_email = "sharonleeyen@gmail.com"
# The document you wish to send. Path is relative to the root directory of this repo.

file_name_path = 'trade.pdf';

base_path = 'https://demo.docusign.net/restapi'



# Constants

APP_PATH = os.path.dirname(os.path.abspath(__file__))

def send_document_for_signing():

  """

  Sends the document <file_name> to be signed by <signer_name> via <signer_email>

  """



  # Create the component objects for the envelope definition...

  with open(os.path.join(APP_PATH, file_name_path), "rb") as file:

    content_bytes = file.read()

  base64_file_content = base64.b64encode(content_bytes).decode('ascii')



  document = Document( # create the DocuSign document object 

    document_base64 = base64_file_content, 

    name = 'Trading Verfication', # can be different from actual file name

    file_extension = 'pdf', # many different document types are accepted

    document_id = 1 # a label used to reference the doc

  )




  # Create the signer recipient model 

  signer = Signer( # The signer

    email = signer_email, name = signer_name, recipient_id = "1", routing_order = "1")



  # Create a sign_here tab (field on the document)

  sign_here = SignHere( # DocuSign SignHere field/tab

    document_id = '1', page_number = '1', recipient_id = '1', tab_label = 'SignHereTab',

    x_position = '195', y_position = '147')



  # Add the tabs model (including the sign_here tab) to the signer

  signer.tabs = Tabs(sign_here_tabs = [sign_here]) # The Tabs object wants arrays of the different field/tab types




  # Next, create the top level envelope definition and populate it.

  envelope_definition = EnvelopeDefinition(

    email_subject = "Please sign this document sent from the Python SDK",

    documents = [document], # The order in the docs array determines the order in the envelope

    recipients = Recipients(signers = [signer]), # The Recipients object wants arrays for each recipient type

    status = "sent" # requests that the envelope be created and sent.

  )
  # Ready to go: send the envelope request

  api_client = ApiClient()

  api_client.host = base_path

  api_client.set_default_header("Authorization", "Bearer " + access_token)



  envelope_api = EnvelopesApi(api_client)

  results = envelope_api.create_envelope(account_id, envelope_definition=envelope_definition)

  return results
  
