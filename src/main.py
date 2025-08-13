from functions import markdown_to_html_node


def main():
    md = """
# Header 1

- item 1
- item 2

## Header 2

Paragraph
and _more_ text

```
Code
here and _there_
**booold**
```

[link](https://notscammy.com)

![img alt](https://notscammy.com/image.jpg)

### Header 3

> Great quote
"""
    blocks = markdown_to_html_node(md)
    
    print(f"{blocks.to_html()}")

if __name__ == "__main__":
    main()
