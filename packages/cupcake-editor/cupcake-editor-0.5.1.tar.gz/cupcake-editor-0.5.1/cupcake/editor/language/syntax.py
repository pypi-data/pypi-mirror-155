from ...config.languages import CPP


class SyntaxLoader:
    def __init__(self):
        self.syntax = CPP()
        self.setup_tokens()

    def setup_tokens(self):
        self.keywords = self.syntax.keywords
        self.numbers = self.syntax.numbers
        self.strings = self.syntax.strings
        self.comments = self.syntax.comments

        self.regexize_tokens()

    def regexize_tokens(self):
        self.rgx_keywords = "|".join([f"\\y{i}\\y" for i in self.keywords])
        self.rgx_numbers = "|".join(self.numbers)
        self.rgx_strings = "|".join(self.strings)
        self.rgx_comments = "|".join(self.comments)
    
    def get_autocomplete_list(self):
        return [(i, "keyword") for i in self.keywords]
