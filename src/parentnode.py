from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("Error: ParentNode object must have a tag")

        if self.children == []:
            raise ValueError("Error: ParentNode object must have children")
        
        child_to_html = [child.to_html() for child in self.children]
        return f"<{self.tag}>{"".join(child_to_html)}</{self.tag}>"