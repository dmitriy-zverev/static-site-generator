class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = []
        if children:
            self.children += children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        result_str = ""

        for prop in self.props:
            result_str += " " + f"{prop}=\"{self.props[prop]}\""
        return result_str
    
    def __repr__(self):
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>\nChildren: {self.children}"