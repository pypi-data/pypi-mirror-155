
class SwipError(Exception):
    pass


class NoSwipError(SwipError):
    pass


class CommitError(SwipError):
    pass


class CommitRequiredError(FileNotFoundError):
    pass


class BranchExistsError(SwipError):
    pass  


class NoBranchError(SwipError):
    pass


class CheckoutError(SwipError):
    pass


class MergeError(SwipError):
    pass
