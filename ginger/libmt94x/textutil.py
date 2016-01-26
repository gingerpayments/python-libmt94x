def break_at_width(text, width=65, newline='\r\n'):
    lines = []

    iterations = len(text) / width
    for i in range(iterations + 1):
        line = text[i * width:(i + 1) * width]
        if i < iterations:
            line = '%s%s' % (line, newline)

        lines.append(line)

    block = ''.join(lines)
    return block
