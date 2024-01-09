import os
import re

def get_all_views(path_project):
    
    views = [] 
    
    path_folder_views = os.path.join(path_project, 'resources')
    path_folder_views = os.path.join(path_folder_views, 'views')
    path_folder_views = os.path.expanduser(path_folder_views)
    
    start_path = "resources/views/"
      
    for root_folder, sub_folder, files in os.walk(path_folder_views): 
        ##print('\n')
        for file in files:
            if '.blade.php' in file:
                ##print('file', file)
                full_url = os.path.join(root_folder, file)
                
                # Chemin relatif par rapport au répertoire de départ avec le début spécifié
                relative_path = os.path.relpath(full_url, path_folder_views).replace(os.sep, "/")

                relative_path = os.path.join(start_path, relative_path)
                
                views.append(relative_path) 
     
    ##print('views', views)
    
    return views

def get_all_text_to_translate(path_file):
    
    view_content = None
    
    ##print('\nget_all_text_to_translate\n')
    
    with open(path_file, 'r') as file: 
        view_content = file.read()
    
    if not view_content:
        return []
    
    # Utilisation de regex pour extraire le contenu entre ***__ et __***
    matches = re.findall(r'\*\*\*__(.*?)__\*\*\*', view_content, re.DOTALL)

    # Affichage des résultats
    ##print('matches', matches)
    
    # ##print('content', view_content)
    return matches
    
def get_translate_key_and_content_by_list(list):
    
    final_list = []
    
    for i,item in enumerate(list): 
        original_content = item
        
        item = item.lstrip()
        item = item.rstrip()
        
        key = transform_text_to_key_lang(item)
        
        check = True
        # for val in final_list:
        #     if val['key'] == key:
        #         check = False
        #         break
        
        if check:
            final_list.append({
                "key": key,
                "content": item,
                "original_content": original_content
            })
        
    ##print('final_list', final_list)
    
    return final_list    
    
def transform_text_to_key_lang(text):
    
    key = None
    
    if len(text)  <= 60:
        key = text_to_snack_case(text)
    else: 
        first_20_chars = text[:20]        
        last_20_chars = text[-20:] 
        key = text_to_snack_case(f"{first_20_chars}___{last_20_chars}")      
    
    return key

def text_to_snack_case(text):
    
    text = text.replace(' ', '_')
    text = text.lstrip()
    text = text.rstrip()
    text = text.lower()
    # text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)
    # ne pas faire un php dans un ***__ __***
    html_special_characters = ['<', '>', '!', '?', '.', '&', "'", '"', '/', '\\', ',', ';', '*', '+']
    
    for i,item in enumerate(html_special_characters):
        text = text.replace(item, '_')
    
    return text
 
def transform_file_view_text_to_key_text(path_file, dict_texts, name_view):
     
    last_view_content = None
    new_view_content = None
     
    with open(path_file, 'r') as file: 
        last_view_content = file.read()
    
    if not last_view_content:
        return False, new_view_content, last_view_content
    
    ##print(dict_texts, type(dict_texts))

    def custom_replace(match): 
        matched_text = match.group(1)  
        for key,value in enumerate(dict_texts): 
            if value.get('original_content') == matched_text:
                return "{!! __('"+ get_filename_lang(name_view) +"."+ value.get('key') +"') !!}"

        return matched_text

    new_view_content = re.sub(r'\*\*\*__(.*?)__\*\*\*', custom_replace, last_view_content, flags=re.DOTALL)

    # for key,value in enumerate(dict_texts):
        # view_content = re.sub(r'\*\*\*__'+ value.get('original_content') +'__\*\*\*', "{!! __('"+ get_filename_lang(name_view) +"."+ value.get('key') +"') !!}", view_content, flags=re.DOTALL)
         
         
    ##print('\n')
    ##print('transform_file_view_text_to_key_text', new_view_content)
    ##print('\n')
    
    with open(path_file, 'w') as file: 
        file.write(new_view_content)
     
    return True, new_view_content, last_view_content


def get_filename_lang(path_file):
    
    return path_file.replace(os.path.sep, '_').replace('.blade.php', '')
    

def extract_folder_and_file(path, path_folder): 
    # Utilisez os.path.relpath pour obtenir le chemin relatif par rapport à path_folder
    relative_path = os.path.relpath(path, path_folder)
    
    # Divisez le chemin relatif pour obtenir le nom du dossier et le nom du fichier
    folder, filename = os.path.split(relative_path)
     
    return filename, folder


def subtract_parent_path(parent_path, child_path):
    try:
        relative_path = os.path.relpath(child_path, parent_path)
        return relative_path if not relative_path.startswith('..') else ''
    except ValueError:
        return ''
    
def filter_by_key(input_list):
    seen_keys = set()
    result_list = []

    for d in input_list:
        key = d['key']
        
        if key not in seen_keys:
            result_list.append(d)
            seen_keys.add(key)

    return result_list


def make_str_array_php_to_list_dict(array_php):
    # Vérifie l'existence de <?php et return dans la chaîne PHP
    if "<?php" in array_php and "return" in array_php:
        # Retire <?php et return de la chaîne PHP
        php_code = re.sub(r'<\?php|return', '', array_php)

        # Utilise une expression régulière pour extraire les paires clé-valeur de la chaîne PHP
        matches = re.findall(r'"([^"]+)"\s*=>\s*"([^"]+)"', php_code)
        
        # Crée la liste de dictionnaires avec les clés "key" et "content"
        result_list = [{"key": match[0], "content": match[1]} for match in matches]

        return result_list

    else:
        ##print("Les balises PHP ou le mot clé 'return' sont absents dans la chaîne.")
        return []

def create_or_update_lang_file(name_view, path_folder_view, project_path, dict_texts):
    
    dict_texts = filter_by_key(dict_texts)
       
    base_path = 'resources/views'
    relatif_path_view = subtract_parent_path(base_path, path_folder_view)  
    ##print('\nrelatif_path_view 1',relatif_path_view)

    relatif_path_view = os.path.join(relatif_path_view, name_view) 
    
    ##print('\nrelatif_path_view 2',relatif_path_view)

    path_folder_lang = "lang/en"
    name_file_lang = relatif_path_view.replace('.blade.php', '').replace(' ', '').replace('./', '').replace(os.path.sep, '_') + '.php'
    path_file_lang = os.path.join(path_folder_lang, name_file_lang) 
    
    full_path_file_lang = os.path.join(project_path, path_file_lang)
    
    ##print('\npath_folder_lang', path_folder_lang)
    ##print('\nname_file_lang', name_file_lang)
    ##print('\npath_file_lang', path_file_lang)
    ##print('\nfull_path_file_lang 1', full_path_file_lang)
    
    full_path_file_lang = os.path.expanduser(full_path_file_lang)
    ##print('\nfull_path_file_lang 2', full_path_file_lang)
    
      
    if os.path.isfile(full_path_file_lang):
    
        actual_content = ''
    
        with open(full_path_file_lang, 'r') as file:
            actual_content = file.read()
    
        list_content_in_file = make_str_array_php_to_list_dict(actual_content)
        
        final_list = merge_to_list_dict_lang(list_content_in_file, dict_texts)
           
        new_content_file = list_dict_to_form_array_php(final_list)
         
        final_new_content_file = f"<?php \n\nreturn  [\n{new_content_file}\n];"
        
        # Créez le fichier avec le contenu
        with open(full_path_file_lang, 'w') as file:
            file.write(final_new_content_file)
    
    else:
           
        new_content_file = list_dict_to_form_array_php(dict_texts)
        
        final_new_content_file = f"<?php \n\nreturn  [\n{new_content_file}\n];"
         
        full_path_folder_lang = os.path.dirname(full_path_file_lang)

        # Créez les sous-dossiers si nécessaire
        if not os.path.exists(full_path_folder_lang):
            os.makedirs(full_path_folder_lang)

        # Créez le fichier avec le contenu
        with open(full_path_file_lang, 'w') as file:
            file.write(final_new_content_file)

def merge_to_list_dict_lang(original_list, new_list):
    
    ##print('merge_to_list_dict_lang - original_list', original_list, type(original_list))
    ##print('merge_to_list_dict_lang - new_list', new_list, type(new_list))
    
    final_list = []
    
    for i, val in enumerate(original_list):
        
        ##print('val original_list', val, type(val))
    
        final_list.append({
            "key": val["key"],
            "content": val["content"],
        })
        
    for i, val in enumerate(new_list): 
        
        ##print('val new_list', val, type(val))
    
        check = True
        for j, val_1 in enumerate(final_list):
            if final_list[j]["key"] == val["key"]:
                check = False
                break
        
        if check:
            final_list.append({
                "key": val["key"],
                "content": val["content"],
            })
    
    return final_list

def list_dict_to_form_array_php(list_content_in_file):
    
    new_content_file = '\n'
    
    for key,value in enumerate(list_content_in_file):
         
        content = re.sub(r'(?<!\\)"', r'\\"', value.get("content"))
        
        new_content_file += f'\t"{value.get("key")}" => "{content}", \n'
        
    ##print('\ncontent_file', new_content_file)
    
    return new_content_file