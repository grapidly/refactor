# coding=utf8
import re

# =============================== BUGS ===============================
#       BUG -- 'follow_frame-bottom' class in styles dict but NOT appending suffix.
#       BUG -- '.one_col_text--header h3' by there --> '.two_col_text__OOO--column-one__OOO,' appending to middle of class.


class Refactor:

    def __init__(self):
        self.suffix = input(
            'ENTER SUFFIX TO APPEND TO HTML/CSS/JS CLASS NAMES: ')
        self.styles = {}
        self.css = None
        self.html = None
        self.js = None
        self.EXCLUSION_LIST = ['.woff', '.jpg',
                               '.woff2', '.js-', '.ug-', '.active']

    def __repr__(self):
        try:
            return '<Refactor object; css=({0}), html=({1}), styles=({2})>'.format(len(self.css), len(self.html), len(self.styles))

        except TypeError as error:
            return '{0}: <Refactor object; css=({0}), html=({1}), styles=({2})>'.format(error, 0, 0, 0)

      # =============================== UTIL METHODS ===============================

    def __load_files(self):
        with open('test.css', 'r') as fp:
            self.css = fp.read()
        with open('test.html', 'r') as fp:
            self.html = fp.read()
        with open('test.js', 'r') as fp:
            self.js = fp.read()
        return self.css, self.html, self.js

    def __load_re_matches(self):
        css, html, js = self.__load_files()
        css_re = r"""\.\D[^]['?#\s\r\n,{};:/\/\().]+"""
        css_re2 = r"""\.(?!png|svg|com|url|w3|ttf|org|gif|jpg|jpeg|onlinewebfonts|eot|woff)([a-z-_]+[^-.,)(\/])"""
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
        old_value = match.group()
        if len(old_value) < 5:
            pass
        elif old_value in self.EXCLUSION_LIST:
            pass
        else:
            # old_value = old_value.replace('.', '')
            new_value = old_value+self.suffix
            self.styles[old_value] = new_value

    def __init_html(self):
        html = self.html
        pattern = 'class=\"(.[a-zA-Z-_ \d]+)\"'
        matches = re.finditer(pattern, html, flags=re.M)
        matches = [(match.group(), match.span()) for match in matches]

        return matches, pattern, html

    def __init_css(self):
        css = self.css
        pattern = r"""\.\D[^]['?#\s\r\n,{};:/\/\().]+"""
        matches = re.finditer(pattern, css, flags=re.M)
        matches = [(match.group(), match.span()) for match in matches]

        return matches, css

    def __get_new_style(self, value):
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
                                           " "+self.__get_new_style(style), temp_line, count=1)
                    else:
                        continue

                final_line = temp_line

                if final_line.startswith("class=\""):
                    pass
                else:
                    final_line = final_line.replace("class=", "class=\"")

            file_string = re.sub('('+line+')+', final_line, file_string)

        return file_string

    def __unpack_css(self, matches, file_string):
        # regex pattern playground -->  https://regex101.com/r/fvGD8T/3

        pattern = r"""\.(?!png|svg|com|url|w3|ttf|org|gif|jpg|jpeg|onlinewebfonts|eot|woff)([a-z-_]+[^-.,)(\/])"""
        for index, line in enumerate(file_string.splitlines()):
            new_line = line
            matches = re.finditer(
                pattern, line, flags=re.MULTILINE)
            if matches:
                for match in matches:
                    start, end = match.span()
                    match = match.group()
                    if match in self.styles:
                        new_line = re.sub(
                            match, self.styles[match], line, count=1, flags=re.MULTILINE)
                        file_string = re.sub(
                            line, new_line, file_string, count=1, flags=re.MULTILINE)
                    else:
                        continue

            else:
                continue

        return file_string

    # =============================== USER METHODS ===============================

    def load_styles(self):
        css_matches, html_matches, js_matches = self.__load_re_matches()
        for matchNum, match in enumerate(css_matches, start=1):
            self.__create_styles_dict(matchNum, match)

    def pp_styles(self):
        print(*self.styles.items(), sep='\n')

    def write(self, data=None, filename=None):
        if filename is None:
            filename = input('ENTER FILENAME: ')

        with open(filename, 'w') as fp:
            fp.write(data)

        print(f"FILES REFACTORED WITH SUFFIX: '{self.suffix}' TO '{filename}'")

    # =============================== SANDBOX ===============================

    def re_html(self):
        matches, pattern, html = self.__init_html()
        refactored_html = self.__unpack_matches(matches, pattern, html)
        self.write(refactored_html, 'RF.html')

    def re_css(self):
        matches, css = self.__init_css()
        refactored_css = self.__unpack_css(matches, css)
        print(refactored_css)
        self.write(refactored_css, 'RF.css')


if __name__ == "__main__":
    rf = Refactor()
    rf.load_styles()
    # rf.re_html()
    rf.re_css()
    html = rf.html
    styles = rf.styles
    css = rf.css
