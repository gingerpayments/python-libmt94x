def break_at_width(text, width=None, newline=None):
    width = width or 65
    newline = newline or '\r\n'

    # If text is 130 chars + newline then we will produce:
    #   line1 + newline
    #   line2 + newline
    #   newline
    # So to avoid this remove the newline proactively
    if text.endswith(newline) and (len(text) - len(newline)) % width == 0:
        text = text[:-len(newline)]

    # Figure out how many lines we will need to output
    num_iterations = len(text) / width

    # Chop the text into lines of length width and terminated with newline
    lines = []
    for idx in range(num_iterations + 1):
        begin_pos = idx * width
        end_pos = (idx + 1) * width
        line = text[begin_pos:end_pos]

        # If it's not the last line we need to append a newline
        if idx < num_iterations:
            line = '%s%s' % (line, newline)

        lines.append(line)

    # Re-assemble all the lines into a block of text
    block = ''.join(lines)

    return block

def format_amount(amount, locale):
    if locale == 'nl_NL':
        bytes = b'%.2f' % amount
        bytes = bytes.replace('.', ',')
        return bytes

    raise NotImplementedError
