import os
import re
from lm_eval.base import rf, PerplexityTask
from lm_eval.utils import sh

from best_download import download_file


def wikitext_detokenizer(string):
    # contractions
    string = string.replace("s '", "s'")
    string = re.sub(r"/' [0-9]/", r"/'[0-9]/", string)
    # number separators
    string = string.replace(" @-@ ", "-")
    string = string.replace(" @,@ ", ",")
    string = string.replace(" @.@ ", ".")
    # punctuation
    string = string.replace(" : ", ": ")
    string = string.replace(" ; ", "; ")
    string = string.replace(" . ", ". ")
    string = string.replace(" ! ", "! ")
    string = string.replace(" ? ", "? ")
    string = string.replace(" , ", ", ")
    # double brackets
    string = re.sub(r"\(\s*([^\)]*?)\s*\)", r"(\1)", string)
    string = re.sub(r"\[\s*([^\]]*?)\s*\]", r"[\1]", string)
    string = re.sub(r"{\s*([^}]*?)\s*}", r"{\1}", string)
    string = re.sub(r"\"\s*([^\"]*?)\s*\"", r'"\1"', string)
    string = re.sub(r"'\s*([^']*?)\s*'", r"'\1'", string)
    # miscellaneous
    string = string.replace("= = = =", "====")
    string = string.replace("= = =", "===")
    string = string.replace("= =", "==")
    string = string.replace(" " + chr(176) + " ", chr(176))
    string = string.replace(" \n", "\n")
    string = string.replace("\n ", "\n")
    string = string.replace(" N ", " 1 ")
    string = string.replace(" 's", "'s")

    return string


class RadBioText(PerplexityTask):
    VERSION = 1

    def download(self):
        if not os.path.exists('data/radbio/test'):
            os.makedirs("data/radbio/test", exist_ok=True)
            with open("data/radbio/test/test.validation.raw", 'w') as f:
                txt = """So let me explain, I modified the lowercase_word function. Let’s look at the changes.\n
Our function now accepts a parameter called number, As you can see, it is already initialized with a value, 5. The reason is that, if you choose not to provide a number, it uses the default value in the parameter.\n
In calling the function, it will be like this word = lowercase_word(number) with your desired number being in the brackets.\n
The length of the generated word will be equal to the length of the number you provided. The rest of the code is pretty self-explanatory."""
                for i in range(10):
                    f.write(txt)
                    f.write('\n')
            with open("data/radbio/test/test.test.raw", 'w') as f:
                txt = """So let me explain, I modified the lowercase_word function. Let\
’s look at the changes.
Our function now accepts a parameter called number, As you can see, it is already initi\\n
alized with a value, 5. The reason is that, if you choose not to provide a number, it u\
ses the default value in the parameter.
In calling the function, it will be like this word = lowercase_word(number) with your d\\n
esired number being in the brackets.
The length of the generated word will be equal to the length of the number you provided\
. The rest of the code is pretty self-explanatory."""
                for i in range(10):
                    f.write(txt)
                    f.write('\n')

                
            

    def has_validation_docs(self):
        return True

    def has_train_docs(self):
        return False

    def has_test_docs(self):
        return True
    
    def docs_for_split(self, split):
        ret = []
        for line in open(f"radbiotexthack.txt").read().split('\n'):
            rline = line.strip()
            if len(line) > 30:
                yield line

    def validation_docs(self):
        return self.docs_for_split('valid')

    def train_docs(self):
        return self.docs_for_split('train')

    def test_docs(self):
        return self.docs_for_split('test')

    def doc_to_target(self, doc):
        return wikitext_detokenizer(doc)
    
    def count_words(self, doc):
        # count number of words in *original doc before detokenization*
        return len(re.split(r"\s+", doc))
