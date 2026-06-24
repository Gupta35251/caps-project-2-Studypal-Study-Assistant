import os

working_directory = os.path.dirname(os.path.abspath(__file__))
# parent_directory = os.path.dirname(working_directory)
parent_directory = working_directory

# print(parent_directory)
def get_chapter_list(book_name):
    book_dir = f"{parent_directory}/Data_ind/Class 9/{book_name}"
    chapter_names = os.listdir(book_dir)
    chapter_names = [chapter[:-4] for chapter in chapter_names]
    chapter_names.sort(key=lambda x:int(x.split(' ')[1]))
    return chapter_names 

# print(get_chapter_list("Science"))

