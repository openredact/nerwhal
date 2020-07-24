_recognizer_classes = ()
__all__ = [recognizer.__name__ for recognizer in _recognizer_classes]
__tags__ = set([tag for recognizer in _recognizer_classes for tag in recognizer.TAGS])
