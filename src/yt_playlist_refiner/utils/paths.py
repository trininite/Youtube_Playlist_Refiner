from os import path

#TODO implement these functions to replace copied logic

def resolve_path(unresolved_path :str) -> str:
    normalized_path :str = path.normpath(unresolved_path) 

    resolved_path :str = path.abspath(normalized_path)

    return resolved_path


def valid_path(unreviewed_path :str) -> True:
    resolved :str = resolve_path(unreviewed_path)

    if path.exists(resolved):
        return True
    
    return False