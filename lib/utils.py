import streamlit.components.v1 as components


def add_to_color(color, amount):
    """
    Add a certain amount to a color in the range [0, 255]
    """
    def _clip_color(color):
        """
        Clip a color in the range [0, 255]
        """
        if color > 255:
            color = 255
        elif color < 0:
            color = 0
        return int(color)

    # r_comp = _clip_color(color & 0xFF0000 + amount & 0xFF0000)
    r_comp = _clip_color(float((color >> 16) & 0x0000FF) + float((amount >> 16) & 0x0000FF)) 
    g_comp = _clip_color(float((color >> 8) & 0x0000FF) + float((amount >> 8) & 0x0000FF))
    b_comp = _clip_color(float(color & 0x0000FF) + float(amount & 0x0000FF)) 
    # g_comp = _clip_color(color & 0x00FF00 + amount & 0x00FF00)
    # b_comp = _clip_color(color & 0x0000FF + amount & 0x0000FF)  
    print(r_comp, g_comp, b_comp) 
    print(r_comp << 16, g_comp << 8, b_comp)
    print((r_comp << 16) + (g_comp << 8) + b_comp)
    return (r_comp << 16) + (g_comp << 8) + b_comp


def color_to_hex(color):
    color = hex(color)[2:]
    color = color.upper()
    color = '#' + color
    return color


def ChangeButtonColour(widget_label, font_color, background_color='transparent'):
    if isinstance(background_color, int):
        border_color = add_to_color(background_color, 0x000000)
        border_color = color_to_hex(border_color)
        background_color = color_to_hex(background_color)
    else:
        border_color = ''
    print(border_color, background_color, font_color)

    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    console.log("Element:");
                    console.log(elements[i]);
                    console.log("Element End");
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}';
                    elements[i].style.border = '5px solid {border_color}';
                    console.log("After change:");
                    console.log(elements[i]);
                    console.log("If End")
                }}
            }}
        </script>
        """
    components.html(f"{htmlstr}", height=0, width=0)