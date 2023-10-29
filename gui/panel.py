import thorpy


class Panel(thorpy.Box):
    def __init__(self, children, size=(300, 300), color=(200, 200, 200)):
        # Initialize a ThorPy box element with the provided elements and size
        super(Panel, self).__init__(children=children, size_limit=size)

        self.set_bck_color(color)
