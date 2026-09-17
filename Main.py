# Main.py
from customtkinter import *
from Views import MainView
from ViewModels import MainPresenter

def Main():
    deactivate_automatic_dpi_awareness()
    root = CTk()
    presenter = MainPresenter.Presenter()
    view = MainView.View(presenter, root)

    view.Execute()
    root.mainloop()

if __name__ == "__main__":
    Main()

# TODO
# add blocks and connections deletion
# start blocks functionalities
# deleting blocks and connections
