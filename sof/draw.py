from colorama import init, Fore

init()


class WordLengthExceed(Exception):
    pass


def break_line(line, width):
    line = line.rstrip()
    total_length = len(line)

    if total_length <= width:
        return [line]

    # 切分一行为多行
    words = line.split()
    # 如果某个单词都比行长限制大, 那么说明行长限制不合理, 上报异常
    max_len = max(map(len, words))
    if max_len > width:
        for word in words:
            if len(word) == max_len:
                max_word = word
                break
        raise WordLengthExceed("Width is too small to cover word:%s, set at least: %s" % (max_word, max_len))
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + word) > width:
            lines.append(current_line[:-1])
            current_line = word + " "
        else:
            current_line = current_line + word + " "
    if current_line:
        lines.append(current_line[:-1])
    return lines


def output(content, width=100, max_line=50, color=Fore.GREEN):
    lines = content.split('\n')
    lines = [break_line(line, width) for line in lines]
    # flat lines
    lines = [line for bl in lines for line in bl]
    for i, line in enumerate(lines):
        print(color, line)
        if i == max_line - 1:
            print(color, "...")
            break


