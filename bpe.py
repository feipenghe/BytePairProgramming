def increase_frequency(d, bigram):
    # print("increase frequency: ", bigram)

    if bigram not in d.keys():
        d[bigram] = 1
    else:
        d[bigram] += 1
def decrease_frequency(d, bigram):
    # print("decrease frequency: ", bigram)
    if bigram in d.keys():
        d[bigram] -= 1
        drop_bigram(d, bigram)

def drop_bigram(d, bigram):
    """ check and act dropping bigram"""
    if bigram in d.keys():
        if d[bigram] <= 0:
            d.pop(bigram)
            return True

def plot_n_save(xs, ys):
    """ takes two list of numbers"""
    from matplotlib import pyplot as plt
    import numpy as np
    xs = np.array(xs)
    ys = np.array(ys)
    plt.scatter(xs, ys)
    plt.xlabel("size of the type vocabulary")
    plt.ylabel("length of the training corpus")

    plt.savefig('q3.png')

if __name__ == "__main__":
    # def preprocess
    # """process text files into a list of "words"  """
    # each word is a list of tokens, tokens are added into dictionary and are counted in frequency dicitonary
    import sys
    vocab_len_limit = sys.maxsize
    process_line_limit = sys.maxsize
    # process_line_limit = sys.maxsize
    frequency_limit = 1
    d = dict()
    vocab = set()
    with open("./A5-data.txt", "r") as f:
        lines = f.readlines()
        text = ""
        count = 0
        for line in lines:
            line = line.replace("\n", "")  ## stripping
            text += "".join(line) + " "
            # print("text: ", text)
            count += 1
            if count == process_line_limit:
                break
        #     text = " ".join(line)
        #     print(text)
        #     text = "it unit unites."
        #     print(text)
        text = [char for char in text]

        # text is one sentence here
        word = []
        tokenized_text = []
        for i in range(len(text)):
            if text[i] == " ":
                token = "<s>"
                word.append(token)
                tokenized_text.append(word)
                word = []  # reintilize word
                vocab.add(token)
            # elif text[i] == ".":  # need more word boundary vocabulary
            #     token = text[i]
            #     word.append(token)
            #     tokenized_text.append(word)
            #     word = []  # reintilize word
            #     vocab.add(token)
            else:
                token = text[i]
                word.append(text[i])
                vocab.add(token)

        print(tokenized_text)

    # def count frequency
    # iterate tokenized_text and scan per bigram
    for tokenized_word in tokenized_text:
        for i in range(len(tokenized_word) - 1):
            word1 = tokenized_word[i]
            word2 = tokenized_word[i + 1]
            bigram = (word1, word2)
            increase_frequency(d, bigram)

    #         if bigram not in d.keys():
    #             d[bigram] = 0
    #         d[bigram] += 1

    # def
    # iterate tokenized_text and change affected frequency
    xs = []
    ys = []

    while True:
        if len(d) == 0:
            break
        highest_pair = max(d, key=d.get)
        if d[highest_pair] <= frequency_limit:
            break
        print("highest freq: ", d[highest_pair])
        d.pop(highest_pair)
        vocab.add(highest_pair)

        if len(vocab) >= vocab_len_limit:
            break


        match_count = 0
        # frequency recalculate
        for tokenized_word in tokenized_text:
            for i in range(len(tokenized_word) - 1):
                word1 = tokenized_word[i]
                word2 = tokenized_word[i + 1]
                bigram = (word1, word2)

                if bigram == highest_pair:
                    match_count += 1
                    # bigram not in dictionary anymore but it's in text

                    # if bigram in d.keys():
                    #     d[bigram] -= 1


                    if i - 1 >= 0:  # valid index for left token
                        left = tokenized_word[i - 1]
                        left_bigram = (left, word1 + word2)
                        # if left_bigram == ('n', 'in'):
                        #     print("bigram, ", bigram)
                        #     print("tokenized_word: ", tokenized_word)
                        #     exit()
                        increase_frequency(d, left_bigram)
                        original_left_bigram = (left, word1)
                        decrease_frequency(d, original_left_bigram)
                        vocab.add(word1 + word2)
                    if i + 2 < len(tokenized_word):
                        right = tokenized_word[i + 2]
                        right_bigram = (word1 + word2, right)

                        increase_frequency(d, right_bigram)
                        original_right_bigram = (word2, right)
                        decrease_frequency(d, original_right_bigram)
                        # print("vocab add: ", word1 + word2)
                        vocab.add(word1 + word2)
                    drop_bigram(d, bigram)
                    # if drop_bigram(d, bigram):  # possibly dropping bigram in dictionary
                    #     print("drop: ", bigram)
                    #     print(d)
        if match_count == 0:
            print("no found matched bigram in tokenized_text:  ", highest_pair)
        for tokenized_word in tokenized_text:
            discount = 0
            for i in range(len(tokenized_word) - 1):
                word1 = tokenized_word[i + discount]
                word2 = tokenized_word[i + 1 + discount]
                bigram = (word1, word2)
                if bigram == highest_pair:
                    tokenized_word[i + discount] = word1 + word2
                    del tokenized_word[i + 1 + discount]
                    discount -= 1
                    # print("tokenized_text", tokenized_text)
        x = len(vocab)
        xs.append(x)
        y = 0
        for tokenized_word in tokenized_text:
            y += len(tokenized_word)
        ys.append(y)
        # print("dictionary: ", d)
    plot_n_save(xs, ys)

    final_output = "final number of type: " + str(len(vocab)) + " \n"
    final_output += "final length of the training data under the type dictionary: " + str(y)
    # print(vocab)
    # print(d)
    with open("output.txt", "w") as f:
        f.write(final_output)