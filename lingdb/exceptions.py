class NoLanguageDataError(Exception):
    """An error that is raised when data is requested from a language, but that
    data is not available for the given language"""
    pass
