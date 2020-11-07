def check_word(given_word,word):#given_word=word word=Motus[name]['motus']['word']
    state = []#0=:x: 1=:large_orange_diamond: 2=:red_circle:
    word_list = list(word)
    for i in range(len(given_word)):
        state.append(0)
    for i in range(len(given_word)):
        if given_word[i] == word[i]:
            word_list[i] = '!'
            state[i] = 2
    for i in range(len(given_word)):
        if given_word[i] in word_list and state[i] != 2:
            index = word_list.index(given_word[i])
            word_list[index] = '!'
            state[i] = 1
        elif state[i] != 2:
            state[i] = 0
    return state

def convert(state,word):
    good = 0
    text = ''
    for i in range(len(state)):
        if state[i] == 0:
            text += ':x:'
        if state[i] == 1:
            text += ':large_orange_diamond:'
        if state[i] == 2:
            good += 1
            text += ':regional_indicator_' + word[i].lower() + ':'
    return [text,good]

a = check_word('EPEISTE','EPSTEIN')
text = convert(a,'EPSTEIN')
print(text)
