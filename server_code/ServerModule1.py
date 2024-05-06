import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
from anvil.pdf import PDFRenderer
import anvil.server

@anvil.server.callable
def create_pdf():
  # Create a pdf from 'Form2', and pass in 'name' and 'img' as its constructors
  pdf = PDFRenderer(filename='Little Beaver Invoice', quality='original').render_form("Form1")
  return pdf
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
