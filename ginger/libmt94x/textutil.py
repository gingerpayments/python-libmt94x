def break_at_width(text, width=65, newline='\r\n'):
    lines = []

    # If text is 130 chars + newline then we will produce:
    #   line1 + newline
    #   line2 + newline
    #   newline
    # So to avoid this remove the newline proactively
    if text.endswith(newline) and (len(text) - len(newline)) % width == 0:
        text = text[:-len(newline)]

    iterations = len(text) / width
    for i in range(iterations + 1):
        line = text[i * width:(i + 1) * width]
        if i < iterations:
            line = '%s%s' % (line, newline)

        lines.append(line)

    block = ''.join(lines)
    return block


def format_amount(amount, locale):
    if locale == 'nl_NL':
        bytes = b'%.2f' % amount
        bytes = bytes.replace('.', ',')
        return bytes

    raise NotImplementedError
