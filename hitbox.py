class HitBox:
    def __init__(self, left, top, width, height):
        self.height = height
        self.width = width
        self.abs_left = 0
        self.abs_top = 0
        self.margin_left = left
        self.margin_top = top
        self.left = self.abs_left + self.margin_left
        self.top = self.abs_top + self.margin_top

    def move(self, x, y):
        self.abs_left = x
        self.abs_top = y
        self.left = self.abs_left + self.margin_left
        self.top = self.abs_top + self.margin_top

    def get_rect(self):
        return tuple((self.left, self.top, self.width, self.height))

    def collision(self, other):
        if ((other.left <= self.left <= other.left + other.width) or
            (other.left <= self.left + self.width <= other.left + other.width)) and\
                ((other.top <= self.top <= other.top + other.height) or
                 (other.top <= self.top + self.height <= other.top + other.width)):
            return True
        return False
