# Utilities/WidgetsUtilities.py
class WidgetsUtilities():
    @staticmethod
    def IsChildOf(widget, parents: tuple ) -> bool:
            while widget is not None:
                if widget in parents:
                    return True
                widget = widget.master
            return False