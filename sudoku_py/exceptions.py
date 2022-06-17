
class InvalidPuzzleError(Exception):
    """Raised when no options are found for a cell in a puzzle."""
    pass

class EmptyCheckpointer(Exception):
    """Exception when attempting to pop from an empty Checkpointer."""

class UnsolvedWarning(UserWarning):
    """Raised when Solver fails to find a solution."""

