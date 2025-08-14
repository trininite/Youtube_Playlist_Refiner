#TODO change OS import to only include used functions
import os

from utils import resolve_path

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

    def __init__(self):

        self.mirror_paths :list[str] = []

        try:
            assert os.path.exists(self.cache_file_path)
        except AssertionError as e:
            cache_created :bool = self._create_cache()
            if not cache_created:
                print("Cache folder or file could not be created. Please check permissions or path validity.")
                raise e("Could not assert cache file exists")
        
        self._read_cache()
        self._check_cache()
        self._update_cache()
        


    @property
    def cache_folder_path(self):
        ytpr_cache_folder_name :str = "yt_playlist_refiner"

        user_cache_folder :str = os.path.expanduser("~/.cache")

        cache_folder_path :str = os.path.join(user_cache_folder, ytpr_cache_folder_name)

        return cache_folder_path
    
    @property
    def cache_file_path(self):
        ytpr_cache_file_name :str = "mirror_paths.txt"

        cache_file_path :str = os.path.join(self.cache_folder_path, ytpr_cache_file_name)

        return cache_file_path



    def _create_cache(self):
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
        #TODO handle specific exceptions
        try:
            os.mkdir(self.cache_folder_path)
            with open(self.cache_file_path, "w", encoding="UTF+8") as f:
                f.close()
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def _read_cache(self) -> None:
        """
        Reads the cache file and populates the mirror_paths attribute.

        This method opens the cache file specified by cache_file_path, reads each line,
        cleans up the paths using the clean_path method, and appends them to the mirror_paths list.

        Parameters:
            None

        Returns:
            None
        """
        #TODO add error handling
        with open(self.cache_file_path, "r", encoding="UTF+8") as f:
            raw_paths = f.readlines()
        for raw_path in raw_paths:
            cooked_path = resolve_path(raw_path)
            self.mirror_paths.append(cooked_path)


    #TODO combine cache_check and read_cache
    def _check_cache(self) -> None:
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

        print("checking cache...")

        verified_mirror_paths :list = []
        pruned_mirror_paths :list = []
        seen :set = set()

        for path in self.mirror_paths:
            cooked_path = resolve_path(path)
            del path

            if not os.path.exists(cooked_path):
                pruned_mirror_paths.append(cooked_path)
                continue


            if cooked_path in seen:
                pruned_mirror_paths.append()

            seen.add(cooked_path)
            verified_mirror_paths.append(cooked_path)

        
        if pruned_mirror_paths:
            print(f"removed {len(pruned_mirror_paths)} mirror path(s) from cache")
            for pruned in pruned_mirror_paths:
                print(pruned)

        self.mirror_paths :list[str] = verified_mirror_paths
    

    def _update_cache(self):
        with open(self.cache_file_path, "w", encoding="UTF+8") as f:
                for verified in self.mirror_paths:
                    f.write(verified + "\n")


    def add_mirror_path(self, new_mirror_path :str) -> bool:
        """
        Adds a new mirror path to the cache if it doesn't already exist.

        Parameters:
            new_mirror_path (str): The path to the new mirror folder.

        Returns:
            bool: True if the path was added successfully, False otherwise.
        """

        cooked_path :str = resolve_path(new_mirror_path)

        if not os.path.exists(cooked_path):
            print(Exception("mirror doesn't exist"))
            return False

        if cooked_path in self.mirror_paths:
            print(Exception("path already in cache file"))
            return False

        self.mirror_paths.append(new_mirror_path)
        return True
    

    def mirror_path_unique(self, new_mirror_path :str) -> bool:
        cooked_path :str = resolve_path(new_mirror_path)

        if cooked_path in self.mirror_paths:
            print(Exception("path already in cache file"))
            return False
        
        return True

    

