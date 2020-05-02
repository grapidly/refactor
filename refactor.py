# coding=utf8
import re

# TODO:
# ============================================================================
#       BUG -- 'follow_frame-bottom' class in styles dict but NOT appending suffix.
#       BUG -- TBD
#       BUG -- TBD


class Refactor:

    def __init__(self):
        self.suffix = input(
            'ENTER SUFFIX TO APPEND TO HTML/CSS/JS CLASS NAMES: ')
        self.styles = {}
        self.css = None
        self.html = None
        self.js = None
        self.matchlist = []

    def __repr__(self):
        try:
            return '<Refactor object; css=({0}), html=({1}), styles=({2})>'.format(len(self.css), len(self.html), len(self.styles))

        except TypeError as error:
            return '{0}: <Refactor object; css=({0}), html=({1}), styles=({2})>'.format(error, 0, 0, 0)

      # =============================== UTIL METHODS ===============================

    def __load_data(self):
        with open('test.css', 'r') as fp:
            self.css = fp.read()
        with open('test.html', 'r') as fp:
            self.html = fp.read()
        with open('test.js', 'r') as fp:
            self.js = fp.read()
        return self.css, self.html, self.js

    def __load_regex(self):
        css, html, js = self.__load_data()
        css_re = r"""\.\D[^]['?#\s\r\n,{};:/\/\().]+"""
        html_re = r"""class=\".*\""""
        js_re = r""".*"""
        css_matches = re.finditer(
            css_re, css, re.MULTILINE | re.VERBOSE)
        html_matches = re.finditer(
            html_re, html, re.MULTILINE | re.VERBOSE)
        js_matches = re.finditer(
            js_re, js, re.MULTILINE | re.VERBOSE)
        return css_matches, html_matches, js_matches

    def __create_dict(self, matchNum, match):
        old_value = match.group()
        if len(old_value) < 5:
            pass
        elif old_value in ['.woff', '.jpg', '.woff2']:
            pass
        else:
            old_value = old_value.replace('.', '')
            new_value = old_value+self.suffix
            self.styles[old_value] = new_value

    # =============================== USER METHODS ===============================

    def create_styles(self):
        css_matches, html_matches, js_matches = self.__load_regex()
        for matchNum, match in enumerate(css_matches, start=1):
            self.__create_dict(matchNum, match)

    def write(self, data=None):
        if data == None:
            data = self.__replace_html(self.styles, self.html)
        else:
            data = data
        with open('refactor.html', 'w') as fp:
            fp.write(data)

        print(f"FILES REFACTORED WITH SUFFIX: '{self.suffix}'")

    def pp(self):
        print(*self.styles.items(), sep='\n')

    # =============================== SANDBOX ===============================

    def get_style_value(self, value):
        if self.suffix not in value:
            value = self.styles.get(value)
            return value
        else:
            print(f"ERROR. SUFFIX IN CLASS: {value}")

    def re_html(self, html):
        html = self.html
        styles = self.styles
        pattern = 'class=\"(.[a-zA-Z-_ \d]+)\"'
        matches = re.finditer(pattern, html, flags=re.M)
        tups_of_matches = [(match.group(), match.span()) for match in matches]
        # temp debug code to run py -i
        self.matchlist.append(tups_of_matches)

        for index, match in enumerate(tups_of_matches):
            line = match[0]
            line_index = match[1]
            line_start, line_end = line_index
            re_match = re.split(pattern, match[0])
            class_names = re_match[1].split()
            section = html[line_start:line_end]
            temp_line = line

            for index2, class_name in enumerate(class_names):
                for index3, style in enumerate(styles.keys()):
                    if style == class_name and self.suffix not in class_name:
                        temp_line = re.sub('[^\-]'+class_name,
                                           " "+self.get_style_value(style), temp_line, count=1)
                    else:
                        continue

                final_line = temp_line
                if final_line.startswith("class=\""):
                    pass
                else:
                    final_line = final_line.replace("class=", "class=\"")

            html = re.sub('('+line+')+', final_line, html)

        self.write(html)


if __name__ == "__main__":
    rf = Refactor()
    rf.create_styles()
    html = rf.html
    rf.re_html(html)
