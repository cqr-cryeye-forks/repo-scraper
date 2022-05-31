# Add extensions here (lowercase)
from functools import reduce

DEFAULT_EXTENSIONS = ["py", "ipynb", "json", "sql", "sh", "txt", "r", "md", "log", "yaml", 'php']
DEFAULT_EXTENSIONS_FORMAT = reduce(lambda x, y: f'{x}, {y}', DEFAULT_EXTENSIONS)
