import sys
import os
from utils import get_all_views,get_all_text_to_translate,get_translate_key_and_content_by_list,transform_file_view_text_to_key_text,extract_folder_and_file,create_or_update_lang_file

project_path = "" 
if len(sys.argv) > 1:
    project_path = sys.argv[1] 
else:
    print('Missing arguments project_path')
    exit()

print('project_path', project_path)
exit()
    
list_views = get_all_views(project_path)

for i, view in enumerate(list_views): 
    file_path = os.path.join(project_path, view)
    file_path = os.path.expanduser(file_path)
    lang_texts = get_all_text_to_translate(file_path)
    dict_texts = get_translate_key_and_content_by_list(lang_texts)
    
    name_view, path_folder_view = extract_folder_and_file(view, '')
          
    __view = view.replace(os.path.join('resources', 'views') + os.path.sep, '')

    result, new_content, last_content = transform_file_view_text_to_key_text(file_path, dict_texts, __view)
    
    create_or_update_lang_file(name_view, path_folder_view, project_path, dict_texts)

messages = "The file lang for all view created successfully!"

print(messages)