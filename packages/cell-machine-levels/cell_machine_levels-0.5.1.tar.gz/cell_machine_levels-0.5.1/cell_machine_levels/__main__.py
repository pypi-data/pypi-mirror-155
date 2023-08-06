"""CLI for cell_machine_levels."""

import cell_machine_levels

choices = [
    [
        [
            exit,
            lambda: 1,
        ],
        [
            "Exit",
            "Base 74 Encoding",
        ],
    ],
    [
        [
            lambda: 0,
            lambda: print(cell_machine_levels.base74.b74_encode(int(input("Number: "))))
            or 1,
            lambda: print(cell_machine_levels.base74.b74_decode(input("Base 74: ")))
            or 1,
        ],
        [
            "Go Back",
            "Encode",
            "Decode",
        ],
    ],
]

current_menu = 0

while True:
    # Choices
    for i, j in enumerate(choices[current_menu][1]):
        print(f"{i}. {j}")
    print()

    try:
        # Get and run choice
        choice = int(input("Enter your choice: "))
        current_menu = choices[current_menu][0][choice]()
    except (ValueError, IndexError):
        print("Invalid choice")
        continue
