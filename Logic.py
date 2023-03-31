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


    def set_type(self, type):
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
        try:
            # check if path is exists
            if os.path.exists(dst):

                # then check this path is a dir or not
                if os.path.isdir(dst):
                    self.target = dst 
                else:
                    raise Exception("The given dst path is not pointing to a directory")
            else: 
                raise Exception("The given dst path to source is invalid")

        except Exception as e:
            print(e)
            exit()


    def set_target_folder_structure(self):
        try:
            with open("dirs_and_exts.json", "r") as f:
                self.folder_structure= json.load(f)
        
        except Exception as e:
            print(e)
            exit()


    def create_target_folders(self):
        try:
            self.target = os.getcwd() 

            # create the target folder
            path = os.path.join(self.target, Categorizer.OUTPUT_FOLDER_NAME)
            if not os.path.exists(path):
                os.mkdir(path)

            # then create the sub folders
            for record in self.folder_structure:
                if "dir" not in record:
                    continue

                subpath = os.path.join(path, record["dir"])

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