import re
from glob import glob

from tqdm import tqdm

from emoji import emoj as emoji_pat


def tokenize_match(match):
    global line

    if match and match.start() == 0:
        # If there is one at the beginning of the line, tokenise it.
        tokens.append(line[: match.end()])
        line = line[match.end() :]
        return True

    return False


# Compile patterns for speedup
skippable_pat = re.compile(r"\s+|http\S+")  # typically spaces and links to be removed
user_pat = re.compile(r"@user")  # @user pattern
smiley_pat = re.compile(r"([:;8=])[Oo\-'`]?([sSDpPoO|$*@\\/\[\]{}()])")
special_pat = re.compile(
    r"[~’‘”:<>%&!?\|$.,-/()\"\*@;=£\^…‼️—–“∗\[\]{}¯\\―]|\+| ' "
)  # special characters
token_pat = re.compile(r"#*\w+[’‘']*\**\w*")  # General token patern including hashtags


def tokenize_line():
    global line
    # As long as there's any material left...
    while line:
        # Try finding a skippable token delimiter first.
        skippable_match = re.search(skippable_pat, line)
        if skippable_match and skippable_match.start() == 0:
            # If there is one at the beginning of the line, just skip it.
            line = line[skippable_match.end() :]
            continue

        # Find "@user" and tokenize
        user_match = re.search(user_pat, line)
        if tokenize_match(user_match):
            continue

        # Find emoji
        emoji_match = re.search(emoji_pat, line)
        if tokenize_match(emoji_match):
            continue

        # Find smiley and tokenize
        smiley_match = re.search(smiley_pat, line)
        if tokenize_match(smiley_match):
            continue

        # Find special characters
        special_match = re.search(special_pat, line)
        if tokenize_match(special_match):
            continue

        # Tokenize words
        token_match = re.search(token_pat, line)
        if tokenize_match(token_match):
            pass
        else:
            # Else there is unmatchable material here.
            # It ends where a skippable or token match starts, or at the end of the line.
            patterns = [
                skippable_match,
                user_match,
                # emoji_match,
                smiley_match,
                # hashtag_match,
                special_match,
                token_match,
            ]
            matched = [match.start() for match in patterns if match]

            unmatchable_end = min(len(line), min(matched))
            # Add it to unmatchable and discard from line.
            unmatchable.append(line[:unmatchable_end])
            line = line[unmatchable_end:]


def tokenize_file(path, unmatch=False):
    global tokens
    global unmatchable
    tokens = []
    unmatchable = []
    with open(path, "r", encoding="utf-8") as in_file:
        for _line in tqdm(in_file.readlines()):
            global line
            line = _line
            #line = "What a lovely day to drive #not #boo #fog #work 😳😳😳 "
            tokenize_line()
            #break
    if unmatch:
        return tokens, unmatchable
    return tokens


if __name__ == "__main__":
    path = "data/sentiment/test_text.txt"

    _, unmatchable = tokenize_file(path, unmatch=True)

    print(_)
    print(unmatchable)
    print(len(unmatchable))
    quit()
    filtered_tokens = []
    for i, token in enumerate(_):
        if token == ".":
            continue
        filtered_tokens.append(token)

    print(len(_))
    print(len(filtered_tokens))
