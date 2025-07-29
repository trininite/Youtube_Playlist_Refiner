#TODO change OS import to only include used functions
import os

def resolve_cache_path(cache_folder_path :str) -> dict:
    """
    Resolves and returns the cache file and folder paths.

    Parameters:
        cache_folder_path (str): The path to the cache folder. If not provided,
                                 the default path "~/.cache/yt_playlist_refiner" is used.

    Returns:
        dict: A dictionary containing:
            - 'cache_file_path' (str): The path to the cache file "mirror_paths.txt".
            - 'cache_folder_path' (str): The resolved path to the cache folder.
    """

    if not cache_folder_path:
        cache_folder_path :str = os.path.join(os.path.expanduser("~/.cache"), "yt_playlist_refiner")
    cache_file_path :str = os.path.join(cache_folder_path, "mirror_paths.txt")
    return {
        "cache_file_path": cache_file_path,
        "cache_folder_path": cache_folder_path
    }


class CacheManager:
    """
    CacheManager is responsible for managing the cache of mirror paths.

    This class handles the creation, reading, and verification of cache files
    and folders. It maintains a list of valid mirror paths and ensures that the
    cache is up-to-date with existing paths.

    Attributes:
        cache_folder_path (str): The path to the cache folder.
        cache_file_path (str): The path to the cache file.
        mirror_paths (list[str]): A list of validated mirror paths.

    Methods:
        __init__(cache_folder_path: str): Initializes the CacheManager with the
                                          specified cache folder path and ensures
                                          the cache is created if it doesn't exist.
        create_cache(): Creates the cache folder and file if they do not exist.
        add_mirror_path(new_mirror_path: str) -> bool: Adds a new mirror path to
                                                       the cache if it is valid.
        cache_check() -> list[str]: Verifies all paths in the cache and removes
                                    any non-existent paths.
        read_cache(): Reads the cache file and populates the mirror_paths attribute.
        clean_path(dirty_path: str) -> str: Cleans a given path by removing
                                            unnecessary whitespace and slashes.
    """

    def __init__(self, cache_folder_path :str):
        cache_paths :dict = resolve_cache_path(cache_folder_path)
        self.cache_folder_path = cache_paths["cache_folder_path"]
        self.cache_file_path = cache_paths["cache_file_path"]
        try:
            assert os.path.exists(self.cache_file_path)
        except AssertionError:
            self.create_cache()

        self.mirror_paths :list[str] = []


    def create_cache(self):
        """
        Creates the cache folder and cache file if they don't exist.

        If the cache folder does not exist, it is created. If the cache file does not exist,
        it is created.

        Parameters:
            None

        Returns:
            None

        Raises:
            OSError: If the cache folder cannot be created.
        """
        #TODO add error handling
        os.mkdir(self.cache_folder_path)
        with open(self.cache_file_path, "w", encoding="UTF+8") as f:
            f.close()


    def clean_path(self, dirty_path :str) -> str:
        """
        Strips leading and trailing whitespace, and trailing slashes from a given path.

        Parameters:
            dirty_path (str): The path to be cleaned.

        Returns:
            str: The cleaned path.
        """
        return dirty_path.strip().rstrip("/")


    def read_cache(self):
        """
        Reads the cache file and populates the mirror_paths attribute.

        This method opens the cache file specified by cache_file_path, reads each line,
        cleans up the paths using the clean_path method, and appends them to the mirror_paths list.

        Parameters:
            None

        Returns:
            None
        """

        with open(self.cache_file_path, "r", encoding="UTF+8") as f:
            raw_paths = f.readlines()
        for raw_path in raw_paths:
            self.mirror_paths.append(self.clean_path(raw_path))


    def add_mirror_path(self, new_mirror_path :str) -> bool:
        """
        Adds a new mirror path to the cache if it doesn't already exist.

        Parameters:
            new_mirror_path (str): The path to the new mirror folder.

        Returns:
            bool: True if the path was added successfully, False otherwise.
        """
        new_mirror_path = self.clean_path(new_mirror_path)

        resolved_path = os.path.abspath(os.path.normpath(os.path.realpath(new_mirror_path)))

        if not os.path.exists(resolved_path):
            print(Exception("mirror doesn't exist"))
            return False

        if resolved_path in self.mirror_paths:
            print(Exception("path already in cache file"))
            return False

        self.mirror_paths.append(new_mirror_path)
        return True


    def cache_check(self) -> list[str]:
        """
        Verifies all paths in the cache and removes any non-existent paths.

        Returns the verified list of mirror paths.

        If any paths in the cache are pruned, a message is printed to the console
        indicating the number of paths removed and the paths themselves.

        The cache file is then rewritten with the verified paths.

        The verified list of mirror paths is then stored in self.mirror_paths.

        Parameters:
            None

        Returns:
            list[str]: A list of verified mirror paths.
        """
        verified_mirror_paths :list = []
        pruned_mirror_paths :list = []
        seen :set = set()

        for path in self.mirror_paths:
            path = self.clean_path(path)

            if not os.path.exists(path):
                pruned_mirror_paths.append(path)
                continue

            resolved_path = os.path.abspath(os.path.normpath(os.path.realpath(path)))

            if resolved_path in seen:
                pruned_mirror_paths.append()

            seen.add(resolved_path)
            verified_mirror_paths.append(path)

        #TODO make own cache dialogue file in cli module (maybe)
        if pruned_mirror_paths:
            print(f"removed {len(pruned_mirror_paths)} mirror path(s) from cache")
            for deleted in pruned_mirror_paths:
                print(deleted)

            with open(self.cache_file_path, "w", encoding="UTF+8") as f:
                for path in verified_mirror_paths:
                    f.write(path + "\n")

        self.mirror_paths :list[str] = verified_mirror_paths
        return self.mirror_paths
