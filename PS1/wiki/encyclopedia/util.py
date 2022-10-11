import re
import markdown2

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def entry_name_is_taken(new_file):
    """
    Checks if a new encyclopedia entry's title is already present
    in the entries directory. Returns True, if the file-to-be name is
    already taken. Otherwise returns False.
    """
    entries = list_entries()
    for file_name in entries:
        if new_file.lower() == file_name.lower():
            return True 
    return False

def purge_CR(some_text):
    """
    If a line coming from a form is broken by both \\n and \\r, they will be
    replaced by a single \\n.
    """
    linebreaks = re.compile('(\r\n|\n\r)')
    return re.sub(linebreaks, '\n', some_text)

def convert(some_text):
    converter = markdown2.Markdown(extras=["tables", "cuddled-lists",])
    return converter.convert(some_text)