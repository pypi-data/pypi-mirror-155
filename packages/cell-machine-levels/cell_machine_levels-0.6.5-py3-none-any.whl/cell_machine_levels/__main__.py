"""CLI for cell_machine_levels."""

import cell_machine_levels

get_level_code = lambda: input("Input level code (V1, V2 or V3): ")
get_level = lambda: cell_machine_levels.level.open(get_level_code())

get_format = lambda: input("Format to output in (V1, V2 or V3): ")

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
            lambda: print(get_level().optimized().save(get_format())) or 2,
            lambda: print(
                get_level()
                .resized(
                    int(input("Add to cells the left: ")),
                    int(input("Add to cells the right: ")),
                    int(input("Add to cells the top: ")),
                    int(input("Add to cells the bottom: ")),
                )
                .save(get_format())
            )
            or 2,
            lambda: print(get_level().save(get_format())) or 2,
        ],
        [
            "Go Back",
            "Optimize Level (only good for V2 and V3)",
            "Resize Level",
            "Convert Level To Other Format",
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
