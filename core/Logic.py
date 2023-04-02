import os
import shutil
import json



class Categorizer:

    OUTPUT_FOLDER_NAME = "OUTPUT"
    TYPES = ["copy", "move"]


    def __init__(self, src, dst, func, type : int = 0):
        self.progress = 0 # get the progress value from the gui
        self.finish_items = 0 # the total count that compleatly move or copy
        self.total_items = 0 # the total files and dir count that have to move or copy
        self.update_func = func # the update function of the Gui(Gui class)

        self.set_type(type)
        self.set_src(src)
        self.set_target(dst)
        self.set_target_folder_structure()
        self.set_all_files_dirs()
        self.create_target_folders()
        self.move_or_copy_files()


    def set_type(self, type):
        """
        set type copy or move
        :param type : int
        :return None
        """
        try:
            index = int(type)

            if index == 0 or index == 1:
                self.type = Categorizer.TYPES[type]
            else:
                raise Exception("Invalid type, it should be either 0 or 1")

        except Exception as e:
            print(e)
            exit()


    def set_src(self, src):
        """
        set src folder 
        :param src : str
        :return None
        """
        try:
            # check if path is exists
            if os.path.exists(src):

                # then check this path is a dir or not
                if os.path.isdir(src):
                    self.src = src 
                else:
                    raise Exception("The given src path is not pointing to a directory")
            else: 
                raise Exception("The given src path to source is invalid")

        except Exception as e:
            print(e)
            exit()


    def set_target(self, dst):
        """
        set target folder (dst/OUTPUT_FOLDER_NAME)
        :param dst : str
        :return None
        """
        try:
            # check if path is exists
            if os.path.exists(dst):

                # then check this path is a dir or not
                if os.path.isdir(dst):
                    self.target = os.path.join(dst, Categorizer.OUTPUT_FOLDER_NAME)
                else:
                    raise Exception("The given dst path is not pointing to a directory")
            else: 
                raise Exception("The given dst path to source is invalid")

        except Exception as e:
            print(e)
            exit()


    def set_all_files_dirs(self):
        """
        get the all files and folders of the src path
        and set it to self.all property
        :return None
        """
        try:
            self.all = list(os.walk(self.src).__next__())
            root, dirs, _ = self.all 

            if Categorizer.OUTPUT_FOLDER_NAME in dirs:
                if os.path.join(root, Categorizer.OUTPUT_FOLDER_NAME) == self.target:
                    self.all[1].remove(Categorizer.OUTPUT_FOLDER_NAME) # delete output folder from the dirs
            
            # set the total tiles and folder counts that hove to move or copy
            self.set_total_items()
            self.update_func(self.progress, self.total_items, self.finish_items)

        except Exception as e:
            print(e)
            exit()

    
    def set_total_items(self):
        """
        set total_items that have to copy or move
        if any file that in source already exists in the dstination's sub directory
        that file is skip
        :return None
        """
        _, dirs, files = self.all

        for folder in dirs:
            sub_dir = self.get_sub_directory("directory")
            if sub_dir:
                if not os.path.exists(os.path.join(self.target, sub_dir, folder)):
                    self.total_items += 1

        for file in files:
            ext = os.path.splitext(file)
            sub_dir = self.get_sub_directory(ext[1][1:]) or "OTHERS"# get the file extension
            if sub_dir:
                if not os.path.exists(os.path.join(self.target, sub_dir, file)):
                    self.total_items += 1



    def set_target_folder_structure(self):
        """
        set target_folder_structure according to the dirs_and_exts.json file data
        :return None
        """
        try:
            with open("dirs_and_exts.json", "r") as f:
                self.folder_structure= json.load(f)
        
        except Exception as e:
            print(e)
            exit()


    def create_target_folders(self):
        """
        create target folder structure according to the value of self.target_folder_structure values
        :return None
        """
        try:
            # create the target folder
            if not os.path.exists(self.target):
                os.mkdir(self.target)

            # then create the sub folders
            for record in self.folder_structure:
                if "dir" not in record:
                    continue

                subpath = os.path.join(self.target, record["dir"])

                if not os.path.exists(subpath):
                    os.mkdir(subpath)

                if "sub" not in record:
                    continue

                for sub_sub_folder in record["sub"]:
                    sub_sub_path = os.path.join(subpath, sub_sub_folder["dir"])

                    if not os.path.exists(sub_sub_path):
                        os.mkdir(sub_sub_path)

        except Exception as e:
            print(e)
            exit()

    
    # get sub directory according to the file extension
    def get_sub_directory(self, ext):
        """
        get the extenstion of a file and return the sub directory according to the extenstion
        if no folder according to the given extension then return false
        :param ext : str
        :return str | bool
        """
        try:
            for record in self.folder_structure:
                if record["ext"] == ext:
                    return record["dir"]
                
                if "sub" in record: 
                    for sub_record in record["sub"]:
                        if sub_record["ext"] == ext:
                            return os.path.join(record["dir"], sub_record["dir"])

            return False

        except Exception as e:
            print(e)
            exit()


    def copy_or_move_print(self, src:str, dst:str) -> None:
        """
        print the file previous path and copy or move path values with some alignments using fstrings
        :param src: str 
        :param dst: str
        :return None
        """
        print(f"{src:<70}   =>        {dst}")


    def move_or_copy_files(self):
        """
        move or copy file in the self.src path to self.target path sub folders
        not replace anything that already exists in the self.target sub folders
        :return None
        """
        try:
            root, dirs, files = self.all

            # copy all the folders of the src to DIRECTORY sub folder
            for folder in dirs:
                sub_dir = self.get_sub_directory("directory")
                if sub_dir:
                    if not os.path.exists(os.path.join(self.target, sub_dir, folder)):
                        if self.type == "copy":
                            shutil.copytree(os.path.join(root, folder), os.path.join(self.target, sub_dir, folder))
                        elif self.type == "move":
                            shutil.move(os.path.join(root, folder), os.path.join(self.target, sub_dir))

                        self.copy_or_move_print(os.path.join(self.src, folder), os.path.join(self.target, sub_dir, folder))
                        self.finish_items += 1 
                        self.progress = 100 * self.finish_items / self.total_items
                        self.update_func(int(self.progress), self.total_items, self.finish_items)


            # copy all files to the sub direcotories according to their extension
            for file in files:
                ext = os.path.splitext(file)
                sub_dir = self.get_sub_directory(ext[1][1:]) or "OTHERS" # get the file extension

                if sub_dir:
                    if not os.path.exists(os.path.join(self.target, sub_dir, file)):
                        if self.type == "copy":
                            shutil.copy(os.path.join(root, file), os.path.join(self.target, sub_dir))
                        else:
                            shutil.move(os.path.join(root, file), os.path.join(self.target, sub_dir))

                        self.copy_or_move_print(os.path.join(root, file), os.path.join(self.target, sub_dir, file))
                        self.finish_items += 1 
                        self.progress = 100 * self.finish_items / self.total_items
                        self.update_func(int(self.progress), self.total_items, self.finish_items)

            # set compleated to True
            self.update_func(int(self.progress), self.total_items, self.finish_items, compleated=True)
        
        except Exception as e:
            print(e)
            exit()