import os
import shutil
import json



class Categorizer:

    OUTPUT_FOLDER_NAME = "OUTPUT"
    TYPES = ["copy", "move"]


    def __init__(self, src, dst, type : int = 0):
        self.set_type(type)
        self.set_src(src)
        self.set_target(dst)
        self.set_target_folder_structure()
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
        :param src : string
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
        :param dst : string
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
        :param ext : string
        :return str | bool
        """
        try:
            for record in self.folder_structure:
                if record["ext"] == ext:
                    return record["dir"]
                
                if "sub" in record: 
                    for sub_record in record["sub"]:
                        if sub_record["ext"] == ext:
                            return sub_record["dir"]

            return False

        except Exception as e:
            print(e)
            exit();


    def move_or_copy_files(self):
        """
        move or copy file in the self.src path to self.target path sub folders
        not replace anything that already exists in the self.target sub folders
        :return None
        """
        try:
            for root, dirs, files in os.walk(self.src):

                # copy all the folders of the src to DIRECTORY sub folder
                for folder in dirs:
                    sub_dir = self.get_sub_directory("directory")
                    if sub_dir:
                        if self.type == "copy":
                            if os.path.exists(os.path.join(self.target, sub_dir, folder)):
                                shutil.copytree(os.path.join(root, folder), os.path.join(self.target, sub_dir, folder))
                        elif self.type == "move":
                            if os.path.exists(os.path.join(self.target, sub_dir)):
                                shutil.move(os.path.join(root, folder), os.path.join(self.target, sub_dir))

                # copy all files to the sub direcotories according to their extension
                for file in files:
                    ext = os.path.splitext(file)
                    sub_dir = self.get_sub_directory(ext[1][1:]) # get the file extension

                    if sub_dir:
                        if os.path.exists(os.path.join(self.target, sub_dir)):
                            if self.type == "copy":
                                shutil.copy(os.path.join(root, file), os.path.join(self.target, sub_dir))
                            else:
                                shutil.move(os.path.join(root, file), os.path.join(self.target, sub_dir))
                break
        
        except Exception as e:
            print(e)
            exit()
            