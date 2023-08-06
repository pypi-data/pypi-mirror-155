"""CLI for cell_machine_levels."""

import cell_machine_levels

choices = [
    [
        [
            exit,
            lambda: 1,
            lambda: 2,
        ],
        [
            "Exit",
            "Base 74 Encoding",
            "Level Stuff",
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
    [
        [
            lambda: 0,
            lambda: print(
                cell_machine_levels.level.open(
                    input("Input level code (V1 or V2): ")
                ).save(input("Format to output in (V1 or V2): "))
            )
            or 2,
        ],
        [
            "Go Back",
            "Optimize Level (only good for V2 and V3 (not yet))",
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
