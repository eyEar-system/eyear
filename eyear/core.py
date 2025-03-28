class EyEar:
    """Main class for eyEar functionalities."""

    def __init__(self, name="User"):
        self.name = name

    def greet(self):
        """Returns a greeting message."""
        return f"Hello, {self.name}! Welcome to eyEar."
