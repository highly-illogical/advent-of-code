def read_input(filename):
    with open(filename) as file:
        return [line.strip("\n") for line in file]

def find_word_in_string(word, s):
    start, counter, total = 0, 0, 0
    while start < len(s):
        while counter < len(word) and start + counter < len(s) and s[start + counter] == word[counter]:
            counter = counter + 1
        if counter == len(word):
            total = total + 1
        counter = 0
        start = start + 1
    print(s, total)
    return total

def find_word_in_wordsearch(wordsearch, word="XMAS"):
    count = 0

    for row in wordsearch:
        count += sum((find_word_in_string(word, row), find_word_in_string(word[::-1], row)))
    print(count)

    for i in range(len(wordsearch[0])):
        s = "".join(row[i] for row in wordsearch)
        count += sum((find_word_in_string(word, s), find_word_in_string(word[::-1], s)))
    print(count)

    for d in range(len(wordsearch)): # Assuming m == n
        s, t = "", ""
        s = "".join(wordsearch[d + i][i] for i in range(len(wordsearch) - d))
        if d > 0:
            t = "".join(wordsearch[i][d + i] for i in range(len(wordsearch) - d))
        print(s, t)
        count += sum((find_word_in_string(word, s), find_word_in_string(word[::-1], s), find_word_in_string(word, t), find_word_in_string(word[::-1], t)))

        s, t = "", ""
        s = "".join(wordsearch[d + i][len(wordsearch[0]) - 1 - i] for i in range(len(wordsearch) - d))
        if d > 0:
            t = "".join(wordsearch[i][len(wordsearch[0]) - 1 - (d + i)] for i in range(len(wordsearch) - d))
        print(s, t)
        count += sum((find_word_in_string(word, s), find_word_in_string(word[::-1], s), find_word_in_string(word, t), find_word_in_string(word[::-1], t)))

    return count

def find_xmas_in_wordsearch(wordsearch):
    rows = len(wordsearch)
    cols = len(wordsearch[0])

    count = 0

    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if wordsearch[row][col] == 'A':
                d1 = wordsearch[row-1][col-1] + wordsearch[row][col] + wordsearch[row+1][col+1]
                d2 = wordsearch[row+1][col-1] + wordsearch[row][col] + wordsearch[row-1][col+1]

                if d1 in ["MAS", "SAM"] and d2 in ["MAS", "SAM"]:
                    count = count + 1
    return count

if __name__ == "__main__":
    wordsearch = read_input("input.txt")
    print(find_xmas_in_wordsearch(wordsearch))
