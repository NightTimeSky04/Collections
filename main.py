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

    # Read from input file
    with open(txt_file_name) as collection_input:
        collection_list = collection_input.readlines()

    # Dict to contain all collection information
    collection = {}

    # Parse input into collection
    for item in collection_list:
        # All collections begin empty
        collection[item.strip()] = False

    # Save as new JSON file
    with open(json_file_name, "x") as output_filepath:
        js.dump(collection, output_filepath)


# UI takes a user input as items are found, and updates the display of which collectables have been found

# Handle item submission via the GUI
def submit_item():
    """
    Check whether a user specified item appears in the collection and if it has previously been collected, then update the collection accordingly and display a descriptive message to the user.
    """
    # Get user input, discarding capitalisation
    item = ent_user_input.get()

    # Track whether item appears in the collection
    is_not_in_collection = True

    for collectable in collection:

        if item.lower() == collectable.lower():
            is_not_in_collection = False  # Item found in the collection

            # Update collection, text output and diplay if a new collectable has been found
            if not collection.get(collectable):
                collection[collectable] = True

                lbl_output["text"] = f"Found {collectable}!\n"

                collection_labels[collectable].config(text=collectable)

                # Save changes to collection
                with open(json_file_name, "w") as output_filepath:
                    js.dump(collection, output_filepath)

            # Prompt user if the collectable had been found previously
            else:
                lbl_output["text"] = f"{collectable} already found.\n"

    # Prompt user if the item is not in the collection
    if item != "":
        if is_not_in_collection:
            lbl_output["text"] = f"{item.title()} is not in the collection.\n"

    # Remove user input, making space for a new submission
    ent_user_input.delete(0, tk.END)


# GUI structure and contents

# Launch an instance of Tk
window = tk.Tk()
window.title(f"Collections for {game}")
# window.geometry("1080x540")


# Frame containing widgets for item submission
frm_submission = tk.Frame(master=window)
frm_submission.grid(row=0, column=0)

# Label prompt to submit items
lbl_item_submission = tk.Label(
    master=frm_submission, text="Enter items here:")
lbl_item_submission.grid(row=0, column=0, sticky="e")

# Entry which takes item input
ent_user_input = tk.Entry(master=frm_submission, width=50)
ent_user_input.grid(row=0, column=1, sticky="w")

# Submission button which calls submit_item
btn_submit = tk.Button(master=frm_submission,
                       text="submit", command=submit_item)
btn_submit.grid(row=0, column=3)

# Output text to user describing the outcome of their submission
lbl_output = tk.Label(master=frm_submission)
lbl_output.grid(row=1, column=1, sticky="n")


# Frame containing widgets which display the collection
frm_collection = tk.Frame(master=window)
frm_collection.grid(row=1, column=0, padx=10, pady=10)


# Number of columns in collection display
column_count = 4
# Track position of collectables in list in order to determine row position in diplay
entry_index = 0

# Dict to contain label for each collectable
collection_labels = {}

# Display grid of collectables, concealing information until they have been found
for collectable in collection:

    display_text = ""  # Default to no text
    if collection[collectable]:
        display_text = collectable

    # Frame for each collectable, contains widgets which display information
    frm_collectable = tk.Frame(
        master=frm_collection, borderwidth=4, relief=tk.RAISED)

    # Position frame in grid according to number of columns and entry index
    row_index = entry_index // column_count
    column_index = entry_index % column_count
    frm_collectable.grid(row=row_index, column=column_index)

    # Label to display collectable name
    lbl_collectable = tk.Label(
        master=frm_collectable, text=display_text, width=25, relief=tk.GROOVE)
    lbl_collectable.grid(row=0, column=0)

    # Label to display item description or hint
    lbl_description = tk.Label(master=frm_collectable,
                               text="Hints/description here")
    lbl_description.grid(row=1, column=0)

    collection_labels[collectable] = lbl_collectable

    entry_index += 1  # Update index tracker


window.mainloop()
