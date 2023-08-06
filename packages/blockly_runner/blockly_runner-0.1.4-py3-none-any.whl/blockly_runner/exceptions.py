class BlocklyException(Exception):
    pass


class UndefinedVariable(BlocklyException):
    pass


class InvalidBlock(BlocklyException):
    pass
