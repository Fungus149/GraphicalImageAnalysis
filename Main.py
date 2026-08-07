# Main.py
from customtkinter import *
from Views import ContextMenusView, MainView
from ViewModels import MainViewModel

def Main():
    deactivate_automatic_dpi_awareness()
    root = CTk()
    viewmodel = MainViewModel.ViewModel()
    contextMenus = ContextMenusView.View(viewmodel)
    view = MainView.View(viewmodel, contextMenus, root)


    view.Execute()
    print(root.winfo_children())
    root.mainloop()

if __name__ == "__main__":
    Main()

