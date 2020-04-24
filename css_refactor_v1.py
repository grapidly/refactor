# css_refactor.py

# goal: create an app that converts css class names into new classes and save file
# *note: when changing CSS style names, HTML and JS will need to be changed too, as any reference overlooked will break the code.


# Pseudo Code
# ========================

# for style in css_stylesheet:
#     style_type = style_tag_type(style)
#     style_name = style_name(style)
#     search_for_every(style_type, style_name) in ['*.html', '*.js,']:
#         new_style_name = new_name
#         apply(new_style_name, (style_type, style_name)
#         new_code.save()

# ========================
import re
import glob
import os
import time


# def tag_type(css):
#     tags = []
#     for index, ele in enumerate(css.split()):
#         if ele.startswith('.'):
#             style_tag_type = 'class'
#             tags.append([index, 'class:', ele])
#         # need a second filter to exclude hex colors #000021;
#         elif ele.startswith('#') and ele[1] != int:
#             style_tag_type = 'id'
#             tags.append([index, 'id:', ele])
#         else:
#             tags.append([index, 'Unknown:', ele])
#     return tags

def tag_type(data):
    css = ''
    css_file = open("script.css", "w")
    for ele in (data.split()):
        if ele.startswith('.'):

            # pseduo class attr, i.e. ::before, ::after, etc.
            if '::' in ele:
                ele = ele.split('::')
                ele = ele[0]+'--nfr::'+ele[1]+' '
                css += ele

            # state change, i.e. :hover, :focus, etc.
            elif ':' in ele:
                ele = ele.split(':')
                ele = ele[0]+'--nfr:'+ele[1]+' '
                css += ele

            # handle comma bug
            elif ',' in ele:
                ele = ele.replace(',', '')
                ele = ele+'--nfr,'+' '
                css += ele

            # this should be normal class string by itself
            else:
                ele = ele+'--nfr'+' '
                css += ele

        # filter to exclude hex color codes, i.e. #000021;
        elif ele.startswith('#') and ele[1] != int:
            css += ele+' '
        else:
            css += ele+' '

    # return css
    css_file.write(css)
    time.sleep(5)
    css_file.close()
    print('Completed.')


def tag_name(style):
    return style


class Refactor_CSS:
    def __init__(self):
        self.files = None

    def __repr__(self):
        return '<Refactor_CSS: Object>'

    def create(self):
        css = glob.glob('*test.css')
        html = glob.glob('*.html')
        js = glob.glob('*.js')
        self.files = css+html+js
        if len(self.files) == 0:
            return f'No files found in: {os.getcwd()}'
        else:
            return 'Files created.'

    def read(self):
        for path in self.files:
            with open(path, 'r') as fp:
                if '.css' in path:
                    css = fp.read()
                elif '.html' in path:
                    html = fp.read()
                elif '.js' in path:
                    js = fp.read()
        self.files = {'css': css, 'html': html, 'js': js}
        return self.files

    def prep(self):
        pass

    # Preprocessing to split into classes/ids for analysis needed here
    # then ...

    def update(self, css_file):
        for style in css_file:
            style_type = tag_type(style)
            style_name = tag_name(style)
            print(style_type, style_name)

    def destroy(self):
        pass


if __name__ == '__main__':
    rf = Refactor_CSS()
    rf.create()
    rf.read()
    css = rf.files['css']
    html = rf.files['html']
    js = rf.files['js']
    tag_type(css)
