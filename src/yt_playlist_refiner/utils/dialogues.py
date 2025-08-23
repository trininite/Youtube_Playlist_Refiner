def yes_no(assume_yes:bool=True) -> bool:
    if assume_yes:
        q_str = "[Y/n]"
        true_responses = ["y", ""]
    else:
        q_str = "[y/N]"
        true_responses = ["y"]

    while True:
        print(q_str)
        usr_res = input(">> ").lower()
        
        if usr_res not in ["y", "n", ""]:
            print(f"invalid input '{usr_res}'")
            continue
        
        if usr_res in true_responses:
            return True

        return False 