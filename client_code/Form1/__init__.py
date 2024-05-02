from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

class Form1(Form1Template):

  """Initiating variables globally so they can be accesed from multiple functions"""
  cost_after = ""
  freight = ""
  fin_cost = ""
  total_cost = ""
  markup = ""
  selling = ""
  markup_percentage_type = 0
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    """Set the variable to look up items in the spreadsheet"""
    self.part_look_up.items = [(row["Item Number"], row) for row in app_files.lbdata24["LBdata"].rows]
    # Any code you write here will run before the form opens.

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""

    """Reset check boxes to checked whenever product is changed"""
    self.freight_check.checked = True
    self.fin_cost_check.checked = True
    self.markup_check.checked = True

    """Getting the product info from the spreadsheet"""
    part_selected = self.part_look_up.selected_value
    descript = part_selected['Description']
    list_price = part_selected['List Price']
    weight = part_selected['Weight']
    discount = part_selected['Discounted']
    exchange = part_selected['Exchange']
    self.cost_after = part_selected['Cost after']
    self.freight = part_selected['freight']
    self.fin_cost = part_selected['Fin Cost']
    self.total_cost = part_selected['Total Cost']
    self.markup = part_selected['Markup']
    self.selling = part_selected['SELLING PRICE']
    self.markup_percentage_type = part_selected['Markup Type'] 

    """Set the amounts into the displayed text to veiw"""
    self.descript_text.text = descript
    self.list_price_box.text = list_price
    self.weight.text = weight
    self.discount_box.text = discount
    self.exchange_box.text = exchange
    self.freight_box.text = self.freight
    self.fin_cost_box.text = self.fin_cost
    self.total_cost_box.text = self.total_cost
    self.markup_box.text = self.markup
    self.selling_box.text = self.selling

  def set_selling(self):
    """Float variables to total up costs"""
    total_cost_float = float(self.cost_after.lstrip('$ ').rstrip(' ').replace(",", ""))
    selling_float = float(self.cost_after.lstrip('$ ').rstrip(' ').replace(",", ""))

    """If freight is checked add it to the totals"""
    if self.freight_check.checked:
      selling_float += float(self.freight.lstrip('$ ').rstrip(' ').replace(",", ""))
      total_cost_float += float(self.freight.lstrip('$ ').rstrip(' ').replace(",", ""))

    """If fin cost is checked add it to the totals"""
    if self.fin_cost_check.checked:
      selling_float += float(self.fin_cost.lstrip('$ ').rstrip(' ').replace(",", ""))
      total_cost_float += float(self.fin_cost.lstrip('$ ').rstrip(' ').replace(",", ""))

    """Setting the total cost to display"""
    self.total_cost = "$ " + '{:,.2f}'.format(total_cost_float)
    self.total_cost_box.text = self.total_cost

    """Calculating the markup based on the products markup percentage"""
    if self.markup_percentage_type == 0:
      markup_float = total_cost_float * 0.8
    else:
      markup_float = total_cost_float * 0.465

    """Setting the markup value to display"""
    self.markup = "$ " + '{:,.2f}'.format(markup_float)
    self.markup_box.text = self.markup

    """If markup is enabled add to total"""
    if self.markup_check.checked:
      selling_float += markup_float

    """Setting the final price to display"""
    self.selling = "$ " + '{:,.2f}'.format(selling_float)
    self.selling_box.text = self.selling
    pass
      
  def freight_check_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    """Run the function to recalculate the selling price"""
    self.set_selling()
    pass

  def fin_cost_check_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.set_selling()

  def markup_check_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.set_selling()
    pass



     

    
  


                       


    
    
      

    
    
