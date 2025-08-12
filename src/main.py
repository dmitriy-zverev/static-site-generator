from textnode import TextNode, TextType
from htmlnode import HTMLNode
from functions import markdown_to_blocks, block_to_block_type


def main():
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

```
some code.py
```

>Great quote

### This is the same paragraph on a new line ###

- This is a list
- with items

1. item 1
2. item 3
3. item 3
4. item 3
"""
    blocks = markdown_to_blocks(md)
    
    for b in blocks:
        print(block_to_block_type(b))

if __name__ == "__main__":
    main()