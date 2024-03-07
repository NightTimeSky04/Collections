"""
Collections
This program is designed to handle any list of collectable items provided to it in a compatible format.
Details of items will remain concealed until the name of the item is inputted by a user.
An updating list of discovered items is provided to the user.
"""

import re
import os.path
import json as js
import tkinter as tk

# Standardised format for file names
game = "Test Collection"
game_title = re.sub(' ', '-', game.lower())
txt_file_name = f"{game_title}.txt"
json_file_name = f"{game_title}.json"

# Load existing collection data from JSON file, or create a new collection
if os.path.isfile(json_file_name):

    with open(json_file_name) as input_filepath:
        collection = js.load(input_filepath)

else:

    with open(txt_file_name) as collection_input:
        collection_list = collection_input.readlines()

    collection = {}

    for item in collection_list:
        collection[item.strip()] = False

    with open(json_file_name, "x") as output_filepath:
        js.dump(collection, output_filepath)


# UI must take a user input as items are found, and update the display of which collectables have been found

# Handle item submission via the GUI
def submit_item():
    """
    Check whether a specified item appears in the collection and if it has been collected, then update the collection accordingly and display a descriptive message to the user.
    """
    item = ent_user_input.get().title()

    if item in collection:

        if not collection.get(item):
            lbl_output["text"] = f"Found {item}!\n"
            collection[item] = True
            with open(json_file_name, "w") as output_filepath:
                js.dump(collection, output_filepath)

        else:
            lbl_output["text"] = f"{item} already found.\n"

    else:
        lbl_output["text"] = f"{item} is not in the collection.\n"

    ent_user_input.delete(0, tk.END)


window = tk.Tk()
window.title("Collections")


frm_submission = tk.Frame(master=window)
frm_submission.grid(row=0, column=0, padx=20)

lbl_item_submission = tk.Label(
    master=frm_submission, text="Enter collected item here:")
lbl_item_submission.grid(row=0, column=0, sticky="e")

ent_user_input = tk.Entry(master=frm_submission, width=50)
ent_user_input.grid(row=0, column=1, sticky="w")

btn_submit = tk.Button(master=frm_submission,
                       text="submit", command=submit_item)
btn_submit.grid(row=0, column=3, padx=5)

lbl_output = tk.Label(master=window)
lbl_output.grid(row=1, column=0, sticky="n")


window.mainloop()
