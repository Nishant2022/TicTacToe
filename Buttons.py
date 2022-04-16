class Button():
    def __init__(self, surface, colors, hover, rect, font):
        self.surface = surface
        self.colors = colors
        self.hover_color = hover
        self.rect = rect
        self.is_hovering = False
        self.font = font
        self.value = ''
    
    def hover(self, val):
        x, y = val
        if self.rect[0] < x < self.rect[0] + self.rect[2]:
            if self.rect[1] < y < self.rect[1] + self.rect[3]:
                self.is_hovering = True
            else:
                self.is_hovering = False
        else:
            self.is_hovering = False        

    def draw(self, function, *args):
        function(self, *args)
        
    
    def update(self, function):
        function(self)
    
    def change_value(self, value):
        self.value = value

class ToggleButton(Button):
    def __init__(self, surface, color, hover, rect, font):
        super(ToggleButton, self).__init__(surface, color, hover, rect, font)
        self.clicked = False
        self.double_clicked = False
        self.unclicked = False
        self.coords = (0,0)
