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


class Collectable:
    """Defines an object containing all the information that may be provided for a collectable item. Enables conversion to and from a string."""

    def __init__(self, string: str):
        """Parse a string with compatible formatting into a `Collectable`."""
        input = string.split('#')

        # The first input is always name
        self.name = input[0]

        # Parse found tag (always the last input) into a bool if present
        if input[-1] == ("found=True" or "found=False"):
            self.found = eval(input[-1][6:])
        else:
            # Collectables default to not found
            self.found = False

        # All other attributes default to empty
        self.hint = ""
        self.description = ""

        # Assign values to other attributes if present
        if len(input) > 1:
            for field in input[1:]:

                if re.match("desc=.+", field):
                    self.description = re.sub("desc=", "", field)

                if re.match("hint=.+", field):
                    self.hint = re.sub("hint=", "", field)

    def find(self):
        """Change a `Collectable's` `found` tag to `True`."""
        self.found = True

    def is_found(self):
        return self.found

    def get_description(self):
        return self.description

    def get_hint(self):
        return self.hint

    def get_name(self):
        return self.name

    def to_string(self):
        """Convert the information stored in a `Collectable` to a string."""
        string = f"{self.name}"

        if self.description != "":
            string += f"#desc={self.description}"

        if self.hint != "":
            string += f"#hint={self.hint}"

        string += f"#found={self.found}"

        return string


def export_to_json(collection: dict, json_file_name: str):
    """Converts a collection to a format that can be stored in a JSON file, then saves it under the specified file name."""

    export_collection = {}

    for subcollection in collection:

        export_subcollection = {}

        for collectable_name in collection[subcollection]:
            export_subcollection[collectable_name] = collection[subcollection][collectable_name].to_string(
            )

        export_collection[subcollection] = export_subcollection

    with open(json_file_name, "w") as export_filepath:
        js.dump(export_collection, export_filepath, indent=2)


def import_from_json(json_file_name: str):
    """Loads a collection from a JSON file, then parses the save formatting back into Collectable objects."""

    with open(json_file_name) as import_filepath:
        import_collection = js.load(import_filepath)

    collection = {}

    for import_subcollection in import_collection:

        subcollection = {}

        for collectable_name in import_collection[import_subcollection]:
            subcollection[collectable_name] = Collectable(
                import_collection[import_subcollection][collectable_name])

        collection[import_subcollection] = subcollection

    return collection


# Standardised format for file names
game = "Test Collection 2"
game_title = re.sub(' ', '-', game.lower())
txt_file_name = f"{game_title}.txt"
json_file_name = f"{game_title}.json"


# Get collection from file name

# Load existing collection data from JSON file, or create a new collection from text file template
if os.path.isfile(json_file_name):

    collection = import_from_json(json_file_name)

else:

    # Read from input file
    with open(txt_file_name) as collection_input:
        collectables_input = collection_input.readlines()

    # Dict to contain all collection information
    collection = {}

    # Default subcollection
    subcollection = {}
    subcollection_name = "All"

    # Parse input into collection
    for collectable_details in collectables_input:
        if collectable_details != "\n":  # Ignore empty lines in template
            collectable_details = collectable_details.strip()  # Remove newline chars

            # Identify subcollections
            if re.match("\[.+\]", collectable_details):
                if subcollection:
                    collection[subcollection_name] = subcollection

                subcollection = {}
                subcollection_name = re.sub("\[|\]", "", collectable_details)

            else:
                collectable = Collectable(collectable_details)
                collectable_name = collectable.get_name().lower()

                subcollection[collectable_name] = collectable

    if subcollection:
        collection[subcollection_name] = subcollection

    # Save as new JSON file
    export_to_json(collection, json_file_name)


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

    for subcollection in collection:
        for collectable_name in collection[subcollection]:

            if item.lower() == collectable_name:
                is_not_in_collection = False  # Item located in the collection

                # Update collection and change display if a new collectable has been found
                if not collection[subcollection][collectable_name].is_found():
                    collection[subcollection][collectable_name].find()

                    # Inform user that a collectable has been found
                    lbl_output["text"] = f"Found {collection[subcollection][collectable_name].get_name()}!\n"

                    # Update collection display accordingly
                    collection_labels[collectable_name][0].config(
                        text=collection[subcollection][collectable_name].get_name())
                    # Only update description if a description is available
                    if collection[subcollection][collectable_name].get_description() != "":
                        collection_labels[collectable_name][1].config(
                            text=collection[subcollection][collectable_name].get_description())

                    # Save changes to collection
                    export_to_json(collection, json_file_name)

                # Prompt user if the collectable had been found previously
                else:
                    lbl_output["text"] = f"{collection[subcollection][collectable_name].get_name()} already found.\n"

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
# TODO: add enter as a submission button shortcut
btn_submit = tk.Button(master=frm_submission,
                       text="submit", command=submit_item)
btn_submit.grid(row=0, column=3)

# Output text to user describing the outcome of their submission
lbl_output = tk.Label(master=frm_submission)
lbl_output.grid(row=1, column=1, sticky="n")


# Frame to contain widgets which display the collection
frm_collection = tk.Frame(master=window)
frm_collection.grid(row=1, column=0, padx=10, pady=10)


# Count subcollections in order to determine row position in display
subcollection_index = 0
# Set max length in entries for columns within each subcollection
max_column_length = 16

# Dict to track labels for each collectable
collection_labels = {}

# Display grid of collectables, concealing information until they have been found
for subcollection in collection:

    # Frame for subcollection
    frm_subcollection = tk.Frame(master=frm_collection)
    frm_subcollection.grid(row=0, column=subcollection_index)

    # If collectables do not belong to a subcollection, do not display a subcollection name
    if subcollection == "All":
        section_display_name = ""
    else:
        section_display_name = subcollection

    # Subcollection title
    lbl_subcollection = tk.Label(
        master=frm_subcollection, text=section_display_name)
    lbl_subcollection.grid(row=0, column=0)

    # Frame to contain list of collectables in subcollection
    frm_list = tk.Frame(master=frm_subcollection)
    frm_list.grid(row=1, column=0)

    # Track subcollection entry number for grid positioning reasons
    entry_index = 0

    for collectable_name in collection[subcollection]:

        # Default name to hidden
        collectable_display_name = ""
        # Default text to hint
        collectable_display_text = collection[subcollection][collectable_name].get_hint(
        )

        # Show name and description if found (and if description exists)
        if (collection[subcollection][collectable_name].is_found()):
            collectable_display_name = collection[subcollection][collectable_name].get_name(
            )
            if collection[subcollection][collectable_name].get_description():
                collectable_display_text = collection[subcollection][collectable_name].get_description(
                )

        # Frame for each collectable, contains widgets which display the information
        frm_collectable = tk.Frame(
            master=frm_list, borderwidth=4, relief=tk.RAISED)

        # Position frame in subcollection grid
        row_index = (entry_index) % max_column_length
        column_index = (entry_index) // max_column_length
        frm_collectable.grid(row=row_index, column=column_index)

        # Label to display collectable name
        lbl_collectable = tk.Label(
            master=frm_collectable, text=collectable_display_name, width=50, relief=tk.GROOVE)
        lbl_collectable.grid(row=0, column=0)

        # Label to display item description or hint
        lbl_description = tk.Label(master=frm_collectable,
                                   text=collectable_display_text)
        lbl_description.grid(row=1, column=0)

        # Track labels which will require updates
        collection_labels[collectable_name] = (
            lbl_collectable, lbl_description)

        entry_index += 1

    subcollection_index += 1


window.mainloop()
