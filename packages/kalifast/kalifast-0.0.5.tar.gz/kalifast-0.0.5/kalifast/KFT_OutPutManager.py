# Kalifast main package class
import os
import shutil

class KFT_OutPutManager :
    LOG_FILE_NAME          = "logs.txt"
    OUTPUT_STATE_FILE_NAME = "KFT_OUTPUT_STATE"
    OUTPUT_PARAMS_DIR_NAME = "output" #output
    IMAGE_DIR_NAME = "images"

    def __init__(self, base_path):
    
        if base_path[-1] != '/' :
            base_path += '/'

        if os.path.isdir(base_path) == False :
            os.mkdir(base_path)



        self.base_path = base_path
        self.clearAll()


    def initLog(self):
        f = open(self.base_path + self.LOG_FILE_NAME, "w")
        f.write("==LOGS== \n")
        f.close()

    def writeLog(self, value):
        f = open(self.base_path + self.LOG_FILE_NAME, "a")
        f.write(value + "\n")
        f.close()


    def setOutPutState(self, output_state):
        if os.path.isdir(self.base_path + self.OUTPUT_PARAMS_DIR_NAME) == False :
             os.mkdir(self.base_path + self.OUTPUT_PARAMS_DIR_NAME)

        f = open(self.base_path + self.OUTPUT_PARAMS_DIR_NAME + "/" + self.OUTPUT_STATE_FILE_NAME, "w")
        f.write(output_state)
        f.close()


    def addOutPutParam(self, param, value):
        if os.path.isdir(self.base_path + self.OUTPUT_PARAMS_DIR_NAME) == False :
            os.mkdir(self.base_path + self.OUTPUT_PARAMS_DIR_NAME)


        f = open(self.base_path + self.OUTPUT_PARAMS_DIR_NAME + "/" + param, "w")
        f.write(value)
        f.close()

    def pushImage(self, path_image):
        if os.path.isdir(self.base_path + self.IMAGE_DIR_NAME) == False :
            os.mkdir(self.base_path + self.IMAGE_DIR_NAME)

        shutil.copy(path_image, self.base_path + self.IMAGE_DIR_NAME)
        print()


    def clearAll(self):
        #remove log file

        if os.path.exists(self.base_path + self.LOG_FILE_NAME) :
            os.remove(self.base_path + self.LOG_FILE_NAME)

        #output state file
        if os.path.exists(self.base_path + self.OUTPUT_STATE_FILE_NAME) :
            os.remove(self.base_path + self.OUTPUT_STATE_FILE_NAME)

        #output param dir
        if os.path.isdir(self.base_path + self.OUTPUT_PARAMS_DIR_NAME) == True :
            shutil.rmtree(self.base_path + self.OUTPUT_PARAMS_DIR_NAME)

        #images dir
        if os.path.isdir(self.base_path + self.IMAGE_DIR_NAME) == True :
            shutil.rmtree(self.base_path + self.IMAGE_DIR_NAME)


    def getKalifastVar(self, var_name) :
        if os.path.isdir("./input") == True :
            if os.path.exists("./input/"+var_name) :
                f = open("./input/"+var_name, "r")
                var_value = f.read()
                f.close()
                return var_value

        return False
    







