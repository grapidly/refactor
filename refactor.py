# coding=utf8
import re


class Refactor:
    def __init__(self):
        self.suffix = input(
            'ENTER SUFFIX TO APPEND TO HTML/CSS/JS CLASS NAMES:')
        self.styles = {}
        self.css = None
        self.html = None

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
        return self.css, self.html

    def __load_regex(self):
        css, html = self.__load_data()
        css_re = r"""
            \.\D[^]['?#\s\r\n,{};:/\/\().]+
            """
        html_re = r"""
            class=\"([a-z_-]*\s?[a-z_-]*\s*[a-z_-]*\s*[a-z_-]*\s*[a-z_-]*\s*[a-z_-]*\s*[a-z_-]*\s*)\"
            """
        css_matches = re.finditer(
            css_re, css, re.MULTILINE | re.VERBOSE)
        html_matches = re.finditer(
            html_re, html, re.MULTILINE | re.VERBOSE)
        return css_matches, html_matches

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

    def __replace_html(self, dict, html):
        regex = re.compile("|".join(map(re.escape, dict.keys())))
        return regex.sub(lambda match: dict[match.group(0)], html)

    # =============================== USER METHODS ===============================

    def create_styles(self):
        css_matches, html_matches = self.__load_regex()

        for matchNum, match in enumerate(css_matches, start=1):
            self.__create_dict(matchNum, match)
            print("Match {matchNum} was found at {start}-{end}: {match}".format(
                matchNum=matchNum, start=match.start(), end=match.end(), match=match.group()))

            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                                start=match.start(groupNum), end=match.end(groupNum), group=match.group(groupNum)))

    def pp(self):
        print(*self.styles.items(), sep='\n')

    def write(self, data=None):
        if data == None:
            data = self.__replace_html(self.styles, self.html)
            with open('refactor.html', 'w') as fp:
                fp.write(data)
        else:
            data = data
            with open('refactor.html', 'w') as fp:
                fp.write(data)

    # TODO: Need a clean code to simply append the suffix to all CSS/HTML/JS classes
    def refactor(self):
        pass


if __name__ == "__main__":
    rf = Refactor()
    rf.create_styles()
    rf.write()
