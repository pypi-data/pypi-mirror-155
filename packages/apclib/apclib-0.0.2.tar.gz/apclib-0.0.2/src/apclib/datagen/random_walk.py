import numpy as np
np.random.seed(1)
class random_walk:
    '''
        random walk data generation class
    '''
    def __init__(self, start, std):
        self.value = start
        self.std   = std

    def walk(self):
        self.value += np.random.normal(0,self.std)
        return self.value

def gen_data(tag_info_dict=None, rows=1000):
    
    if tag_info_dict is None:
        tag_info_dict = {}
        for i,tag in enumerate(["x1", "x2", "x3", "x4"]):
            tag_info_dict[tag] = {"start":i+1, "std": i+1}

    data_gen_objects = {}
    data = {}
    for tag in tag_info_dict.keys():
        data_gen_objects[tag] = random_walk(tag_info_dict[tag]["start"],tag_info_dict[tag]["std"])
        data[tag] = []
    
    for i in range(rows):
        for tag in tag_info_dict.keys():
            data[tag].append(data_gen_objects[tag].value)
            data_gen_objects[tag].walk()

    return data

if __name__ == "__main__":
    data = gen_data(rows=5)
    print (data)
