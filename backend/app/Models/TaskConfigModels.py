class Element:
    def __init__(self, element_type=None, search_type=None, search_value=None, action=None, action_value=None, **kwargs):
        self.element_type = element_type
        self.search_type = search_type
        self.search_value = search_value
        self.action = action
        self.action_value = action_value
