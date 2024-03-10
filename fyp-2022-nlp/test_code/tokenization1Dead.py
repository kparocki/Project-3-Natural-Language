import re
from tqdm import tqdm
from emoji import emoj as emoji_pat

# Compile patterns for speedup
skippable_pat = re.compile(r"\s+|http\S+")  # typically spaces and links to be removed
user_pat = re.compile(r"@user")  # @user pattern
smiley_pat = re.compile(r"([:;8=])[Oo\-'`]?([sSDpPoO|$*@\\/\[\]{}()])")
special_pat = re.compile(r"[~’‘”:<>%&!?\|$.,-/()\"\*@;=£\^…‼️—–“∗\[\]{}¯\\―]|\+| ' ")  # special characters
token_pat = re.compile(r"#*\w+[’‘']*\**\w*")  # General token patern including hashtags

matchLst = [user_pat,emoji_pat,smiley_pat,special_pat,token_pat]

def tokenize_line(line):
    lineTokens = []
    lineUnmatch = []
    while line:
        startLen = len(line)
        
        skippable_match = re.search(skippable_pat, line) # If there is a skippable pattern at the beginning of the line, skip it.
        if skippable_match and skippable_match.start() == 0:
            line = line[skippable_match.end() :] 
            continue

        for match in matchLst: # search through each pattern adding it to tokens if present. 
            match = re.search(match, line)
            if match and match.start() == 0:
                lineTokens.append(line[: match.end()])
                line = line[match.end() :]
                continue

        if line and len(line) == startLen: # if there is string left, but nothing is found this iteration, then move one left and search again.
            lineUnmatch.append(line[0])
            line = line[1:]
    
    #lineTokens = [token.lower() for token in lineTokens]

    return lineTokens, lineUnmatch


def tokenize_file(path, unmatch=False):
    tokens = []
    unmatchable = []
    with open(path, "r", encoding="utf-8") as in_file:
        for inputLine in tqdm(in_file.readlines()):
            inputLine = "😂😂😂 \"Queening\" ? BITCH, you tried it! 💀 more like bumming with hoe intentions "
            resTokens, resUnmatch = tokenize_line(inputLine)
            tokens.extend(resTokens)
            unmatchable.extend(resUnmatch)
            break

    if unmatch:
        return tokens, unmatchable
    return tokens


if __name__ == "__main__":
    path = "data/hate/test_text.txt"

    tokens, unmatchable = tokenize_file(path, unmatch=True)

    print(tokens)
    #print(unmatchable)
    print(len(unmatchable))