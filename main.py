from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5.QtCore import QRegExp
from PyQt5 import uic
from math import floor
from os.path import exists

# Written on 28/07/2021
# by @jwesleylima -> https://github.com/jwesleylima

REQUIRED_FILES = ('ui/main.ui', 'res/icon.png')
X_ALIGNMENTS = ('Left', 'Center', 'Right')
Y_ALIGNMENTS = ('Top', 'Center', 'Bottom')

# Fields instances
user_window_width = None
user_window_height = None
user_object_width = None
user_object_height = None
user_alignment_x = X_ALIGNMENTS[0]
user_alignment_y = Y_ALIGNMENTS[0]


def pre_enter() -> None:
    """Makes some presets."""
    # Add default values for alignment fields
    main_window.x_alignment.addItems(X_ALIGNMENTS)
    main_window.y_alignment.addItems(Y_ALIGNMENTS)

    # Add validators to allow only numbers in geometry fields
    validator = QRegExpValidator(QRegExp('[0-9]+'))
    main_window.window_width.setValidator(validator)
    main_window.window_height.setValidator(validator)
    main_window.object_width.setValidator(validator)
    main_window.object_height.setValidator(validator)

    # Add the button event that calculates the positions
    main_window.find_position.clicked.connect(find_position)


def get_field_instances() -> None:
    """Saves the text field instances for use by the other functions."""
    global user_window_width, user_window_height,user_object_width, \
        user_object_height, user_alignment_x, user_alignment_y

    user_window_width = main_window.window_width
    user_window_height = main_window.window_height
    user_object_width = main_window.object_width
    user_object_height = main_window.object_height
    user_alignment_x = main_window.x_alignment.currentText().upper()
    user_alignment_y = main_window.y_alignment.currentText().upper()


def check_empty_fields(field_list) -> bool:
    """Returns whether any of the fields are empty."""
    for field in field_list:
        if not field.text():
            QMessageBox.warning(main_window,
                'Attempting to find with empty fields',
                'All fields must be filled in to find the correct positions. Please fill in all fields and try again.')
            # Focus on the empty field
            field.setFocus(True)
            return False
    # No empty fields found
    return True


def check_exceeded_fields(field_list) -> bool:
    """Returns whether any of the object's fields exceed the window size."""
    for i, field in enumerate(field_list[2:]):
        if int(field.text()) > int(field_list[i].text()) or \
            int(field.text()) < 0:
            QMessageBox.warning(main_window,
                'The size of the object exceeds the size of the window',
                'The size of the object must be smaller or equal to the size of the window, but can never be larger.')
            # Focus on the field exceeded
            field.setFocus(True)
            return False
    # No exceeded fields found
    return True


def validate_fields() -> bool:
    """Checks if the fields are empty or invalid."""
    fields = (user_window_width, user_window_height,
                user_object_width, user_object_height)

    # Check if the fields are empty
    # Check if the object size exceeds the window size
    return (check_empty_fields(fields) and check_exceeded_fields(fields))


def get_position_x() -> int:
    """Calculates the X position respecting the user's requirements."""
    position_x = 0 # LEFT by default

    window_width_number = int(user_window_width.text())
    object_width_number = int(user_object_width.text())

    if user_alignment_x == 'CENTER':
        position_x = floor((window_width_number / 2) - (object_width_number / 2))
    elif user_alignment_x == 'RIGHT':
        position_x = window_width_number - object_width_number

    return position_x


def get_position_y() -> int:
    """Calculates the Y position respecting the user's requirements."""
    position_y = 0 # TOP by default

    window_height_number = int(user_window_height.text())
    object_height_number = int(user_object_height.text())

    if user_alignment_y == 'CENTER':
        position_y = floor((window_height_number / 2) - (object_height_number / 2))
    elif user_alignment_y == 'BOTTOM':
        position_y = window_height_number - object_height_number

    return position_y


def show_positions() -> None:
    """Shows the calculated positions to the user."""
    position_x = get_position_x()
    position_y = get_position_y()

    # Show the results to the user
    main_window.result_x_position.setText(str(position_x))
    main_window.result_y_position.setText(str(position_y))


def find_position() -> None:
    """Basically it is what calls all the other functions."""
    get_field_instances()
    valid_fields = validate_fields()

    if valid_fields:
        show_positions()
    else:
        # Set the default text when a field is invalid
        main_window.result_x_position.setText('Nothing yet')
        main_window.result_y_position.setText('Nothing yet')


def browse_required_files() -> None:
    """It ensures that the program runs only if the necessary files are present."""
    for file in REQUIRED_FILES:
        if not exists(file):
            show_critical_message('Unable to run', f'Could not execute because "{file}" is missing. Reinstalling the program again may solve this.')
            sys.exit(1)


def show_critical_message(title, message) -> None:
    """Displays an error message."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.setWindowIcon(QIcon('res/icon.png'))
    msg.exec_()


if __name__ == '__main__':
    import sys

    program = QApplication(sys.argv)

    # Make sure the necessary files are present
    browse_required_files()

    # Required files found
    main_window = uic.loadUi(REQUIRED_FILES[0])
    main_window.setWindowIcon(QIcon(REQUIRED_FILES[1]))
    
    # WARNING -> Keep the original names
    main_window.statusbar.showMessage('Developed by @jwesleylima | https://github.com/jwesleylima')

    if main_window != None:
        main_window.setWindowTitle('Position Calculator')
        pre_enter()
        main_window.show()

    sys.exit(program.exec_())
