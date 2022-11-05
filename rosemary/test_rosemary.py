from rosemary import Item, update

def test_item_name_isnt_changed():
    item = Item('Bread', days_left = 3, quality = 5)
    update(item)
    return item.name == 'Bread'

def test_item_quality_lower_border():
    item = Item('Bread', days_left = 3, quality = 0)
    update(item)
    return 0 <= item.quality <= 50

def test_item_decreases_days_left():
    item = Item('Bread', days_left = 3, quality = 5)
    update(item)
    return item.days_left == 2

def test_item_decreases_quality():
    item = Item('Bread', days_left = 3, quality = 5)
    update(item)
    return item.quality == 4

def test_item_decreases_quality_speed2_1():
    item = Item('Bread', days_left = 0, quality = 5)
    update(item)
    return item.quality == 3

def test_item_decreases_quality_speed2_2():
    item = Item('Bread', days_left = -5, quality = 5)
    update(item)
    return item.quality == 3



def test_diamond_name_isnt_changed():
    item = Item('Diamond', days_left = 3, quality = 100)
    update(item)
    return item.name == 'Diamond'

def test_diamond_days_left():
    item = Item('Diamond', days_left = 3, quality = 100)
    update(item)
    return item.days_left == 3

def test_diamond_quality_1():
    item = Item('Diamond', days_left = 3, quality = 100)
    update(item)
    return item.quality == 100

def test_diamond_quality_2():
    item = Item('Diamond', days_left = 3, quality = 20)
    update(item)
    return item.quality == 100



def test_cheese_name_isnt_changed():
    item = Item('Aged Brie', days_left = 3, quality = 100)
    update(item)
    return item.name == 'Aged Brie'

def test_cheese_quality_upper_border():
    item = Item('Aged Brie', days_left = 3, quality = 50)
    update(item)
    return 0 <= item.quality <= 50

def test_cheese_quality_1():
    item = Item('Aged Brie', days_left = -50, quality = 1)
    update(item)
    return item.quality == 2

def test_cheese_quality_2():
    item = Item('Aged Brie', days_left = 50, quality = 1)
    update(item)
    return item.quality == 2



def test_tickets_name_isnt_changed():
    item = Item('Tickets', days_left = 3, quality = 100)
    update(item)
    return item.name == 'Tickets'

def test_tickets_quality_upper_border():
    item = Item('Tickets', days_left = 3, quality = 50)
    update(item)
    return 0 <= item.quality <= 50

def test_item_quality_lower_border():
    item = Item('Tickets', days_left = 0, quality = 0)
    update(item)
    return 0 <= item.quality <= 50

def test_tickets_decreases_days_left():
    item = Item('Tickets', days_left = 3, quality = 5)
    update(item)
    return item.days_left == 2

def test_tickets_quality_plus_one_1():
    item = Item('Tickets', days_left = 12, quality = 1)
    update(item)
    return item.quality == 2

def test_tickets_quality_plus_one_2():
    item = Item('Tickets', days_left = 50, quality = 1)
    update(item)
    return item.quality == 2

def test_tickets_quality_plus_two_1():
    item = Item('Tickets', days_left = 11, quality = 1)
    update(item)
    return item.quality == 3

def test_tickets_quality_plus_two_2():
    item = Item('Tickets', days_left = 7, quality = 1)
    update(item)
    return item.quality == 3

def test_tickets_quality_plus_three_1():
    item = Item('Tickets', days_left = 6, quality = 1)
    update(item)
    return item.quality == 4
  
def test_tickets_quality_plus_three_2():
    item = Item('Tickets', days_left = 2, quality = 1)
    update(item)
    return item.quality == 4

def test_tickets_quality_zero():
    item = Item('Tickets', days_left = 1, quality = 20)
    update(item)
    return item.quality == 0
