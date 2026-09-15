# Main.py
from customtkinter import *
from Views import MainView
from ViewModels import MainViewModel

def Main():
    deactivate_automatic_dpi_awareness()
    root = CTk()
    viewmodel = MainViewModel.ViewModel()
    view = MainView.View(viewmodel, root)

    view.Execute()
    root.mainloop()

if __name__ == "__main__":
    Main()

