class NoLanguageDataError(Exception):
    """An error that is raised when data is requested from a language, but that
    data is not available for the given language.

    Not necessarily a fatal error, as it is possible some languages lack data
    in some areas for legitimate reasons (e.g. a student dropped the course
    midway through collecting data).

    Clients should attempt to recover from this error gracefully whenever
    possible."""
    pass

class QuorumError(Exception):
    """An error that is raised by LingDB when more than half of its member languages
    lack data for a given query.

    For the user, this should indicate that there is
    'as yet insufficient data for a meaningful response' and for developers it
    likely means there's some issue reading data from the Google Sheets CSVs
    into the JSON, which is preventing queries from giving meaningful answers.

    This error is likely not recoverable from at runtime, as it suggests flaws
    with the underlying dataset"""
