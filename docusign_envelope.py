import base64, os

from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document



# Settings

# Fill in these constants

#

# Obtain an OAuth access token from https://developers.docusign.com/oauth-token-generator

access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjY4MTg1ZmYxLTRlNTEtNGNlOS1hZjFjLTY4OTgxMjIwMzMxNyJ9.eyJUb2tlblR5cGUiOjUsIklzc3VlSW5zdGFudCI6MTU3MjE3NTYzOSwiZXhwIjoxNTcyMjA0NDM5LCJVc2VySWQiOiI1M2RhNjdmOC1jY2FlLTQwYmYtOWRmYi04NGNjNmRkZmE2ZjYiLCJzaXRlaWQiOjEsInNjcCI6WyJzaWduYXR1cmUiLCJjbGljay5tYW5hZ2UiLCJvcmdhbml6YXRpb25fcmVhZCIsImdyb3VwX3JlYWQiLCJwZXJtaXNzaW9uX3JlYWQiLCJ1c2VyX3JlYWQiLCJ1c2VyX3dyaXRlIiwiYWNjb3VudF9yZWFkIiwiZG9tYWluX3JlYWQiLCJpZGVudGl0eV9wcm92aWRlcl9yZWFkIiwiZHRyLnJvb21zLnJlYWQiLCJkdHIucm9vbXMud3JpdGUiLCJkdHIuZG9jdW1lbnRzLnJlYWQiLCJkdHIuZG9jdW1lbnRzLndyaXRlIiwiZHRyLnByb2ZpbGUucmVhZCIsImR0ci5wcm9maWxlLndyaXRlIiwiZHRyLmNvbXBhbnkucmVhZCIsImR0ci5jb21wYW55LndyaXRlIl0sImF1ZCI6ImYwZjI3ZjBlLTg1N2QtNGE3MS1hNGRhLTMyY2VjYWUzYTk3OCIsImlzcyI6Imh0dHBzOi8vYWNjb3VudC1kLmRvY3VzaWduLmNvbS8iLCJzdWIiOiI1M2RhNjdmOC1jY2FlLTQwYmYtOWRmYi04NGNjNmRkZmE2ZjYiLCJhbXIiOlsiaW50ZXJhY3RpdmUiXSwiYXV0aF90aW1lIjoxNTcyMTc1NjM3LCJwd2lkIjoiNDBjZWFiNTAtNTQ1OS00ODFjLTlhMTAtMTBkMDVkMWQ3ZDhjIn0.bbk6obFFhyLZ9yl9LmdL5hypqal8ECoiz477L7zhz74Lh6IK-CJsc3LKnffCOA0HoGFQt09JaXvWVL2N9T-IhflyitzNvHitJd9IQF2ZPjrwtChISX1JdT1EM6Le6nTDuJlsZtyTI7FEebAB7Evs2SCJr2sx3QB8TVtrxM7zj-oq7BeL8lLFGTXpOCkZLyMCb1o0hGIY0TRMZJAidUig2sh4EZ01WsR7fPlYQSKzZmd06xxVaX3VeQCTazTnKyb2SDnDqi4duCqEKdjUKQ6A_H5iFGPyxhAcgQZMCUI02A6umdiF2uKeH_7cZ8VZLFBL_NaP0V8WKNR19PHjA6j1BQ"
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

    x_position = '90', y_position = '540')



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
  
