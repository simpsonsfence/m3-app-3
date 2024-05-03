from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files

class Form1(Form1Template):

  """Initiating variables globally so they can be accesed from multiple functions"""
  item_number = ""
  descript = ""
  cost_after = ""
  freight = ""
  fin_cost = ""
  total_cost = ""
  markup = ""
  selling = ""
  total = ""
  total_float = 0
  markup_percentage_type = 0
  item_numbers = list(())
  item_descriptions = list(())
  item_sellings = list(())
  item_amounts = list(())
  item_totals = list(())
  total_price = 0
  
  
  
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
    self.item_number = part_selected['Item Number']
    self.descript = part_selected['Description']
    list_price = part_selected['List Price']
    weight = part_selected['Weight']
    discount = part_selected['Discounted']
    exchange = part_selected['Exchange']
    self.cost_after = part_selected['Cost after']
    self.freight = part_selected['freight']
    self.fin_cost = part_selected['Fin Cost']
    self.total_cost = part_selected['Total Cost']
    self.markup = part_selected['Markup']
    if self.markup_percentage_type == 1:
      self.markup_percentage.text = 80
    else:
      self.markup_percentage.text = 46.5
    self.item_amount.text = 1
    self.selling = part_selected['SELLING PRICE']
    self.markup_percentage_type = part_selected['Markup Type'] 

    """Set the amounts into the displayed text to veiw"""
    self.descript_text.text = self.descript
    self.list_price_box.text = list_price
    self.weight.text = weight
    self.discount_box.text = discount
    self.exchange_box.text = exchange
    self.freight_box.text = self.freight
    self.fin_cost_box.text = self.fin_cost
    self.total_cost_box.text = self.total_cost
    self.markup_box.text = self.markup
    self.selling_box.text = self.selling
    self.total_box.text = self.selling

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
    markup_float = total_cost_float * float(self.markup_percentage.text)/100


    """Setting the markup value to display"""
    self.markup = "$ " + '{:,.2f}'.format(markup_float)
    self.markup_box.text = self.markup

    """If markup is enabled add to total"""
    if self.markup_check.checked:
      selling_float += markup_float

    """Setting the final price to display"""
    self.selling = "$ " + '{:,.2f}'.format(selling_float)
    self.selling_box.text = self.selling

    """Setting total price to display"""
    self.total_float = selling_float*int(self.item_amount.text)
    self.total = "$ " + '{:,.2f}'.format(self.total_float)
    self.total_box.text = self.total
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

  def markup_percentage_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass
    
  def item_amount_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass

  def markup_percentage_change(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass
    
  def item_amount_change(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass

  def markup_percentage_lost_focus(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass
    
  def item_amount_lost_focus(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.set_selling()
    pass
  
  def add_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item_numbers.append(self.item_number)
    self.item_descriptions.append(self.descript)
    self.item_sellings.append(self.selling)
    self.item_amounts.append(self.item_amount.text)
    self.item_totals.append(self.total)

    self.total_price += self.total_float
    
    pass

  def generate_invoice_click(self, **event_args):
    """This method is called when the button is clicked"""
    print(self.item_numbers)
    print(self.item_descriptions)
    print(self.item_sellings)
    print(self.item_amounts)
    print(self.item_totals)
    print(self.total_price)
    pass

  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item_numbers = list(())
    self.item_descriptions = list(())
    self.item_sellings = list(())
    self.item_amounts = list(())
    self.item_totals = list(())
    self.total_price = 0
    pass



     

    
  


                       


    
    
      

    
    
