# coding=utf8
import re


class Refactor:

    def __init__(self):
        self.suffix = input(
            'ENTER SUFFIX TO APPEND TO HTML/CSS/JS CLASS NAMES: ')
        self.styles = {}
        self.css = None
        self.html = None
        self.js = None
        self.matchlist = None

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

    def __apply_regex_sub(self, old_value, class_section):
        pattern = re.compile(r"\s?class=\".*"+(old_value)+".*\""
                             )
        pattern_raw = r"\s?class=\".*"+(old_value)+".*\""
        m = re.search(pattern, class_section)
        if m != None:
            group = m.group(0)
            sub = re.sub(
                pattern_raw, self.styles[old_value], class_section, count=1, flags=re.DEBUG)
            class_section += sub
        else:
            class_section = class_section

        return class_section

    def __find_old_value(self, line):
        for old_value in self.styles.keys():
            if old_value in line:
                print('OLD_VAL:', old_value)
                print(line)
                line = self.__apply_regex_sub(
                    old_value, line)
                print("NEW LINE:", line)
            else:
                line = line
        return line

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

        print(f"FILES REFACTORED WITH SUFFIX: '{self.suffix}.'")

    def refactor(self):
        new_html = ''
        html = self.html.splitlines(True)
        pattern = re.compile(r"""class=\".*\"""")
        for line in html:
            m = re.search(pattern, line)
            if m != None:
                m_start, m_end = m.span()
                b_start = line[0:m_start]
                b_end = line[m_end:]
                class_section = line[m_start:m_end]
                class_section = self.__find_old_value(class_section)
                line = b_start + class_section + ' ' + b_end
                new_html += line+' '
            else:
                new_html += line+' '

        self.write(new_html)

    def pp(self):
        print(*self.styles.items(), sep='\n')

    # =============================== SANDBOX ===============================

    def re_html(self, html):
        html = self.html
        styles = self.styles
        matchlist = self.matchlist
        pattern = 'class="\.*(.*).*\"'
        pattern_2 = 'class=\"(.[a-zA-Z-_ \d]+)\"'
        matches = re.finditer(pattern_2, html, flags=re.M)
        matches_tups = [(match.group(), match.span()) for match in matches]

        for index, match in enumerate(matches_tups):
            line = match[0]
            print(index, line)
            line_index = match[1]
            line_start, line_end = line_index
            new_line = ''
            re_match = re.split(pattern_2, match[0])
            print("1", re_match)
            class_names = re_match[1].split()
            print("2", class_names)
            section = html[line_start:line_end]

            for index2, class_name in enumerate(class_names):
                for index3, style in enumerate(styles.keys()):
                    if style == class_name:
                        line = re.sub(''+(class_name)+'',
                                      styles.get(style, line), line, count=1)
                    else:
                        continue
            replace = line
            html = html.replace(section, replace)

        self.write(html)


if __name__ == "__main__":
    rf = Refactor()
    rf.create_styles()
    # rf.refactor()
    # rf.sandbox()
    html = rf.html
    rf.re_html(html)
    matches = rf.matchlist
