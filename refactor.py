# coding=utf8
import re

# =============================== BUGS ===============================
#       BUG -- 'follow_frame-bottom' class in styles dict but NOT appending suffix.


class Refactor:

    def __init__(self):
        self.suffix = input(
            'ENTER SUFFIX TO APPEND TO HTML/CSS/JS CLASS NAMES: ')
        self.styles = {}
        self.css = None
        self.html = None
        self.js = None

    def __repr__(self):
        try:
            return '<Refactor object; css=({0}), html=({1}), styles=({2})>'.format(len(self.css), len(self.html), len(self.styles))

        except TypeError as error:
            return '{0}: <Refactor object; css=({0}), html=({1}), styles=({2})>'.format(error, 0, 0, 0)

      # =============================== UTIL METHODS ===============================

    def __load_website_files(self):
        with open('test.css', 'r') as fp:
            self.css = fp.read()
        with open('test.html', 'r') as fp:
            self.html = fp.read()
        with open('test.js', 'r') as fp:
            self.js = fp.read()
        return self.css, self.html, self.js

    def __load_re_matches(self):
        css, html, js = self.__load_website_files()
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

    def __create_styles_dict(self, matchNum, match):
        EXCLUSION_LIST = ['.woff', '.jpg', '.woff2', '.js', '.ug', '.active']
        old_value = match.group()
        if len(old_value) < 5:
            pass
        elif old_value in EXCLUSION_LIST:
            pass
        else:
            old_value = old_value.replace('.', '')
            new_value = old_value+self.suffix
            self.styles[old_value] = new_value

    def __init_html(self):
        html = self.html
        styles = self.styles
        pattern = 'class=\"(.[a-zA-Z-_ \d]+)\"'
        matches = re.finditer(pattern, html, flags=re.M)
        tups_of_matches = [(match.group(), match.span()) for match in matches]

        return tups_of_matches, pattern, html

    def __get_new_style_value(self, value):
        if self.suffix not in value:
            value = self.styles.get(value)
            return value
        else:
            print(f"ERROR. SUFFIX IN CLASS: {value}")

    def __unpack_matches(self, matches, pattern, file_string):
        for index, match in enumerate(matches):
            line = match[0]
            line_index = match[1]
            line_start, line_end = line_index
            re_match = re.split(pattern, match[0])
            class_names = re_match[1].split()
            section = file_string[line_start:line_end]
            temp_line = line
            final_line = ''

            for index2, class_name in enumerate(class_names):
                for index3, style in enumerate(self.styles.keys()):
                    if style == class_name and self.suffix not in class_name:
                        temp_line = re.sub('[^\-]'+class_name,
                                           " "+self.__get_new_style_value(style), temp_line, count=1)
                    else:
                        continue

                final_line = temp_line

                if final_line.startswith("class=\""):
                    pass
                else:
                    final_line = final_line.replace("class=", "class=\"")

            file_string = re.sub('('+line+')+', final_line, file_string)

        return file_string

    # =============================== USER METHODS ===============================

    def load_styles(self):
        css_matches, html_matches, js_matches = self.__load_re_matches()
        for matchNum, match in enumerate(css_matches, start=1):
            self.__create_styles_dict(matchNum, match)

    def pp_styles(self):
        print(*self.styles.items(), sep='\n')

    def write(self, data=None):
        if data == None:
            data = self.__replace_html(self.styles, self.html)
        else:
            data = data
        with open('refactor.html', 'w') as fp:
            fp.write(data)

        print(f"FILES REFACTORED WITH SUFFIX: '{self.suffix}'")

    # =============================== SANDBOX ===============================

    def re_html(self, html):
        matches, pattern, html = self.__init_html()
        refactored_html = self.__unpack_matches(matches, pattern, html)
        self.write(refactored_html)

    # def re_css(self, css):
    #     css = self.css
    #     pattern = r"""\.\D[^]['?#\s\r\n,{};:/\/\().]+"""
    #     for line in css.splitlines():
    #         print(line)


if __name__ == "__main__":
    rf = Refactor()
    rf.load_styles()
    html = rf.html
    rf.re_html(html)
    styles = rf.styles
    css = rf.css
