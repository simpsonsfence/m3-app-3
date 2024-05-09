from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.media
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from datetime import date
import time

class Form1(Form1Template):

  """Initiating variables globally so they can be accesed from multiple functions"""
  item_number = ""
  item_description = ""
  cost_after = ""
  freight = ""
  fin_cost = ""
  total_cost = ""
  markup = ""
  unit_price = ""
  extended_price = ""
  net_amount = ""
  hst = ""
  total_due = ""
  extended_price_float = 0
  net_amount_float = 0
  hst_float = 0
  total_due_float = 0
  markup_percentage_type = 0
  full_list = []
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    """Set the variable to look up items in the spreadsheet"""
    self.full_list = [(row["Item Number"], row) for row in app_files.lbdata24["LBdata"].rows]
    self.part_look_up.items = self.full_list
    self.invoice_number_item = self.part_look_up.selected_value
    self.rich_text_2.content = 'DATE ' + date.today().strftime("%B %d, %Y") + '\n' + 'NUMBER ' + self.invoice_number_item['Invoice Number']
    self.repeating_panel_1.items = [{}]
    for x in range(11):
      self.repeating_panel_1.items.append({})
    self.repeating_panel_2.items = [{}]  
    self.repeating_panel_2.items = self.repeating_panel_2.items
    self.repeating_panel_3.items = [{}]  
    self.repeating_panel_3.items = self.repeating_panel_3.items
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
    self.item_description = part_selected['Description']
    list_price = part_selected['List Price']
    weight = part_selected['Weight']
    discount = part_selected['Discounted']
    exchange = part_selected['Exchange']
    self.cost_after = part_selected['Cost after']
    self.freight = part_selected['freight']
    self.fin_cost = part_selected['Fin Cost']
    self.total_cost = part_selected['Total Cost']
    self.markup = part_selected['Markup']
    self.item_amount.text = 1
    self.unit_price = part_selected['SELLING PRICE']
    self.markup_percentage_type = int(part_selected['Markup Type'])
    if self.markup_percentage_type == 1:
      self.markup_percentage.text = 80
    else:
      self.markup_percentage.text = 46.5

    """Set the amounts into the displayed text to veiw"""
    self.item_description_text.text = self.item_description
    self.list_price_box.text = list_price
    self.weight.text = weight
    self.discount_box.text = discount
    self.exchange_box.text = exchange
    self.freight_box.text = self.freight
    self.fin_cost_box.text = self.fin_cost
    self.total_cost_box.text = self.total_cost
    self.markup_box.text = self.markup
    self.unit_price_box.text = self.unit_price
    self.extended_price_box.text = self.unit_price
    self.extended_price = float(self.unit_price.lstrip('$ ').rstrip(' ').replace(",", ""))

  def set_selling(self):
    """Float variables to total up costs"""
    total_cost_float = float(self.cost_after.lstrip('$ ').rstrip(' ').replace(",", ""))
    unit_price_float = float(self.cost_after.lstrip('$ ').rstrip(' ').replace(",", ""))

    """If freight is checked add it to the totals"""
    if self.freight_check.checked:
      unit_price_float += float(self.freight.lstrip('$ ').rstrip(' ').replace(",", ""))
      total_cost_float += float(self.freight.lstrip('$ ').rstrip(' ').replace(",", ""))

    """If fin cost is checked add it to the totals"""
    if self.fin_cost_check.checked:
      unit_price_float += float(self.fin_cost.lstrip('$ ').rstrip(' ').replace(",", ""))
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
      unit_price_float += markup_float

    """Setting the final price to display"""
    self.unit_price = "$ " + '{:,.2f}'.format(unit_price_float)
    self.unit_price_box.text = self.unit_price

    """Setting total price to display"""
    self.extended_price_float = unit_price_float*int(self.item_amount.text)
    
    
    self.extended_price = "$ " + '{:,.2f}'.format(self.extended_price_float)
    self.extended_price_box.text = self.extended_price
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
    self.set_selling()
    for x in range(12):
      self.repeating_panel_1.items.pop()
    try:
      self.repeating_panel_1.items.append({'item_number_spot': self.item_number, 'item_description_spot': self.item_description, 'unit_price_spot': self.unit_price, 'quantity_spot': self.item_amount.text, 'extended_price_spot': self.extended_price})
      
    except AttributeError:
      self.repeating_panel_1.items = [
        {'item_number_spot': self.item_number, 'item_description_spot': self.item_description, 'unit_price_spot': self.unit_price, 'quantity_spot': self.item_amount.text, 'extended_price_spot': self.extended_price}
      ]
    for x in range(12):
      self.repeating_panel_1.items.append({})
    self.repeating_panel_1.items = self.repeating_panel_1.items
    self.net_amount_float += self.extended_price_float
    self.net_amount_box.text =  ' $ ' + '{:,.2f}'.format(self.net_amount_float)
    self.hst_float = self.net_amount_float*0.13
    self.hst_box.text =  ' $ ' + '{:,.2f}'.format(self.hst_float)
    self.total_due_float = self.net_amount_float + self.hst_float
    self.total_due_box.text =  ' $ ' + '{:,.2f}'.format(self.total_due_float)
    
    pass

  def generate_invoice_click(self, **event_args):
    """This method is called when the button is clicked"""  
    self.form_panel.visible = False
    self.call_js('printPage')
    self.form_panel.visible = True
    self.invoice_number_item['Invoice Number'] = '' + str(int(self.invoice_number_item['Invoice Number'])+1)
    self.part_look_up.items = [(row["Item Number"], row) for row in app_files.lbdata24["LBdata"].rows]
    self.invoice_number_item = self.part_look_up.selected_value
    self.rich_text_2.content = 'DATE ' + date.today().strftime("%B %d, %Y") + '\n' + 'NUMBER ' + self.invoice_number_item['Invoice Number']
    pass

  def clear_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.repeating_panel_1.items = [{}]
    for x in range(11):
      self.repeating_panel_1.items.append({})
    self.net_amount_float = 0
    self.net_amount_box.text = ' $ ' + '{:,.2f}'.format(self.net_amount_float)
    self.hst_float = 0
    self.hst_box.text = ' $ ' + '{:,.2f}'.format(self.hst_float)
    self.total_due_float = 0
    self.total_due_box.text = ' $ ' + '{:,.2f}'.format(self.total_due_float)
    pass

  def search_list(self):
    searched_list = []
    searched_list.append(self.full_list[0])
    for x in self.full_list:
      if self.search_box.text in x[0] or self.search_box.text in x[0].lower():
        searched_list.append(x)

    self.part_look_up.items = searched_list
    
    pass
  
  def search_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.search_list()
    pass

  def search_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.search_list()
    pass

  def search_box_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    self.search_list()
    pass

  def remove_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    for x in range(12):
      self.repeating_panel_1.items.pop()
    self.net_amount_float -= float(self.repeating_panel_1.items[-1]['extended_price_spot'].lstrip('$ ').rstrip(' ').replace(",", ""))
    self.net_amount_box.text =  ' $ ' + '{:,.2f}'.format(self.net_amount_float)
    self.hst_float = self.net_amount_float*0.13
    self.hst_box.text =  ' $ ' + '{:,.2f}'.format(self.hst_float)
    self.total_due_float = self.net_amount_float + self.hst_float
    self.total_due_box.text =  ' $ ' + '{:,.2f}'.format(self.total_due_float)
    self.repeating_panel_1.items.pop()
    try:
      for x in range(12):
        self.repeating_panel_1.items.append({})
    except AttributeError:
      self.repeating_panel_1.items = [{}]
      for x in range(11):
        self.repeating_panel_1.items.append({})
    self.repeating_panel_1.items = self.repeating_panel_1.items
    pass

  def add_total_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      self.repeating_panel_1.items.append({'item_number_spot': 'Cont.', 'item_description_spot': 'Previous Total', 'unit_price_spot': '', 'quantity_spot': '', 'extended_price_spot': '$ ' + '{:,.2f}'.format(float(self.previous_net_amount.text))})
    
    except AttributeError:
      self.repeating_panel_1.items = [
        {'item_number_spot': 'Cont.', 'item_description_spot': 'Previous Total', 'unit_price_spot': '', 'quantity_spot': '', 'extended_price_spot': '$ ' + '{:,.2f}'.format(float(self.previous_net_amount.text.replace(",", "")))}
      ]

    self.repeating_panel_1.items = self.repeating_panel_1.items
    self.net_amount_float += float(self.previous_net_amount.text)
    self.net_amount_box.text =  ' $ ' + '{:,.2f}'.format(self.net_amount_float)
    self.hst_float = self.net_amount_float*0.13
    self.hst_box.text =  ' $ ' + '{:,.2f}'.format(self.hst_float)
    self.total_due_float = self.net_amount_float + self.hst_float
    self.total_due_box.text =  ' $ ' + '{:,.2f}'.format(self.total_due_float)
    pass