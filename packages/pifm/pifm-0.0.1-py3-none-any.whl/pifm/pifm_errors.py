import sys

def raise_pifm_error(error_text, blocks=[]):
    print("Your code is not valid pifm code!", file=sys.stderr)
    print('\t' + error_text.replace('\n', '\n\t') + '\n', file=sys.stderr)

    for block in blocks:
        print(block, file=sys.stderr)

    sys.exit(0)

DEFAULT_CONTEXT = 3 # lines of context to show

def format_code_block(hint_text, code_text, file_name, real_start_line, real_col_offset, real_end_line, real_end_col_offset):
    formatted_text = f"Note: {hint_text} (at {file_name}:{real_start_line}:{real_col_offset} to {real_end_line}:{real_end_col_offset})\n"

    code_lines = code_text.split('\n')
    index_start_line = real_start_line - 1
    display_start_line = max(0, index_start_line - DEFAULT_CONTEXT)
    index_end_line = real_end_line - 1
    display_end_line = min(len(code_lines) - 1, index_end_line + DEFAULT_CONTEXT)

    for display_line_number in range(display_start_line, display_end_line + 1):
        formatted_text += f"{display_line_number + 1:4} "
        if display_line_number in range(index_start_line, index_end_line + 1):
            formatted_text += "> "
        else:
            formatted_text += "  "

        formatted_text += code_lines[display_line_number] + "\n"

    return formatted_text
