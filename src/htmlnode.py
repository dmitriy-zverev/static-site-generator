class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = []
        if children:
            self.children += children
        self.props = props

    def to_html(self):
        if self.tag:
            return f"<{self.tag}>{self.with_children()}</{self.tag}>"
        return f"{self.with_children()}"
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        result_str = ""

        for prop in self.props:
            result_str += " " + f"{prop}=\"{self.props[prop]}\""
        return result_str
    
    def with_children(self):
        if self.children == []:
            return

        value_with_children = self.value
        
        for child in self.children:
            if child.tag:
                value_with_children += f"<{child.tag}{child.props_to_html()}>{child.value}</{child.tag}>"
            else:
                value_with_children += f"{child.value}"
    
        return value_with_children

    def __repr__(self):
        return f"HTMLNode(<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}> Children: {self.children})"