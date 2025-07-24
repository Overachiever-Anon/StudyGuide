import re

def split_into_chapters(text):
    """
    Splits a given text into chapters based on common chapter headings.

    Args:
        text (str): The full text content of a document.

    Returns:
        list: A list of tuples, where each tuple contains a chapter title and its content.
              e.g., [('Chapter 1: The Beginning', 'Content of chapter 1...')]
    """
    # This pattern looks for 'Chapter' followed by a number/roman numeral, or common section titles.
    pattern = re.compile(
        r'^(Chapter\s+([IVXLCDM]+|\d+)|Introduction|Conclusion|Appendix|References|Summary|Epilogue|Prologue)([:\.\s].*)?$',
        re.IGNORECASE | re.MULTILINE
    )
    
    matches = list(pattern.finditer(text))
    
    if not matches:
        # If no chapters are found, return the whole text as a single chapter.
        return [('Full Document', text)]

    chapters = []
    
    # Capture text before the first match as a 'Preface' or 'Introduction'.
    text_before_first_chapter = text[:matches[0].start()].strip()
    if text_before_first_chapter:
        chapters.append(('Preface', text_before_first_chapter))

    # Iterate through matches to slice the text into chapters.
    for i in range(len(matches)):
        start_pos = matches[i].end()
        end_pos = matches[i+1].start() if i + 1 < len(matches) else len(text)
        
        title = matches[i].group(0).strip()
        content = text[start_pos:end_pos].strip()
        
        chapters.append((title, content))

    return chapters
