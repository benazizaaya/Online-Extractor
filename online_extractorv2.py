import os
import shutil
import re

def find_examples_root(base_dir):
    """Find the 'examples' directory."""
    for root, dirs, _ in os.walk(base_dir):
        for dir_name in dirs:
            if dir_name.lower() == "examples":
                return os.path.join(root, dir_name)
    return None

def find_example_dir(examples_root, example_name):
    """Find the directory for the specific example."""
    for root, dirs, _ in os.walk(examples_root):
        for dir_name in dirs:
            if example_name.lower() in dir_name.lower():
                return os.path.join(root, dir_name)
    return None

def list_sub_examples(example_dir):
    """List all sub-examples in the given example directory."""
    sub_examples = [d for d in os.listdir(example_dir) if os.path.isdir(os.path.join(example_dir, d))]
    return sub_examples

def find_board_dir(example_dir, board_name):
    """Find the directory for the specific board."""
    for root, dirs, _ in os.walk(example_dir):
        for dir_name in dirs:
            if board_name.lower() in dir_name.lower():
                return os.path.join(root, dir_name)
    return None

def extract_model_number(board_name):
    """Extract the model number from the board name following the letter 'U'."""
    match = re.search(r'U(\d{3})', board_name)
    if match:
        return match.group(1)
    return None

def find_startup_file(dfp_dir, model_number):
    """Find the startup file in the dfp directory containing the model number."""
    for root, _, files in os.walk(dfp_dir):
        for file_name in files:
            if file_name.lower().startswith('startup') and model_number in file_name:
                return os.path.join(root, file_name)
    return None

def find_include_file(dfp_dir, model_number):
    """Find the include file in the dfp directory containing the model number."""
    for root, _, files in os.walk(dfp_dir):
        for file_name in files:
            if model_number in file_name and file_name.lower().startswith('stm32'):
                return os.path.join(root, file_name)
    return None

def copy_iar_files(source_dir, destination_dir):
    """Copy IAR-specific files and folders."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    for root, dirs, _ in os.walk(source_dir):
        for dir_name in dirs:
            if dir_name.lower() == 'ewarm':
                ewarm_path = os.path.join(root, dir_name)
                # Check for required extensions
                if any(f.endswith(('.ewd', '.ewp', '.eww')) for f in os.listdir(ewarm_path)):
                    shutil.copytree(ewarm_path, os.path.join(destination_dir, dir_name), dirs_exist_ok=True)
                    break  # Copy once if any of the specified files exist

def copy_directories_with_keywords(src_dir, dest_dir, keywords):
    """Copy directories containing any of the specified keywords, ignoring unwanted ones."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for root, dirs, _ in os.walk(src_dir):
        for dir_name in dirs:
            # Skip unwanted directories
            if dir_name.startswith('hal_') and any(f.endswith(('.ewd', '.ewp')) for f in os.listdir(os.path.join(root, dir_name))):
                continue
            if any(keyword.lower() in dir_name.lower() for keyword in keywords):
                shutil.copytree(os.path.join(root, dir_name), os.path.join(dest_dir, dir_name), dirs_exist_ok=True)

def copy_debug_dir(board_dir, destination_dir):
    """Copy 'debug' directories within the board directory."""
    # Iterate through all levels under the board directory
    for root, dirs, _ in os.walk(board_dir):
        for dir_name in dirs:
            if 'debug' in dir_name.lower():
                shutil.copytree(os.path.join(root, dir_name), os.path.join(destination_dir, dir_name), dirs_exist_ok=True)

def copy_files(src_dir, dest_dir):
    """Copy specific files from the source to the destination."""
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for root, dirs, files in os.walk(src_dir):
        for file_name in files:
            if file_name.lower() in ['readme'] or file_name.lower().startswith('readme.') or file_name.endswith(('.sha', '.sha1', '.pdsc')):
                shutil.copy(os.path.join(root, file_name), dest_dir)

def find_cmsis_dir(base_dir):
    """Find the 'CMSIS' directory."""
    for root, dirs, _ in os.walk(base_dir):
        for dir_name in dirs:
            if dir_name.upper() == "CMSIS":
                return os.path.join(root, dir_name)
    return None

def copy_cmsis_dir(cmsis_dir, destination_dir):
    """Copy the entire 'CMSIS' directory."""
    dest_cmsis_dir = os.path.join(destination_dir, "CMSIS")
    if os.path.exists(cmsis_dir):
        shutil.copytree(cmsis_dir, dest_cmsis_dir, dirs_exist_ok=True)

def copy_include_file(include_file, destination_dir):
    """Copy the include file to the 'inc' directory."""
    inc_dir = os.path.join(destination_dir, "inc")
    if not os.path.exists(inc_dir):
        os.makedirs(inc_dir)
    shutil.copy(include_file, inc_dir)

def copy_example_files(example_dir, board_dir, destination_dir, ide_name, cmsis_dir, startup_file, include_file):
    """Copy necessary files based on the IDE specified."""
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    
    # Copy application directory and README files from the example_dir
    copy_files(example_dir, destination_dir)
    # Copy directories with keywords 'hal' and 'device'
    copy_directories_with_keywords(example_dir, destination_dir, ['hal', 'device'])
    
    # Copy debug directory from the board directory
    copy_debug_dir(board_dir, destination_dir)

    # Copy CMSIS directory
    copy_cmsis_dir(cmsis_dir, destination_dir)

    # Copy startup file
    if startup_file:
        shutil.copy(startup_file, destination_dir)

    # Copy include file
    if include_file:
        copy_include_file(include_file, destination_dir)

    if ide_name.lower() == "iar":
        copy_iar_files(board_dir, destination_dir)
    else:
        # Additional conditions for other IDEs can be added here
        shutil.copytree(board_dir, os.path.join(destination_dir, os.path.basename(board_dir)), dirs_exist_ok=True)

def main():
    # Demander le chemin du répertoire local
    base_dir = input("Entrez le chemin du répertoire local : ")
    
    # Demande des informations utilisateur
    user_input = input("Entrez le nom de l'exemple, la carte de développement, et l'IDE (séparés par des virgules) : ")
    example_name, board_name, ide_name = map(str.strip, user_input.split(','))
    
    # Trouver le répertoire "exemples"
    examples_root = find_examples_root(base_dir)
    if not examples_root:
        print("Le répertoire 'exemples' n'a pas été trouvé.")
        return
    
    # Trouver le répertoire de l'exemple
    example_dir = find_example_dir(examples_root, example_name)
    if not example_dir:
        print("L'exemple spécifié n'a pas été trouvé.")
        return
    
    # Lister les sous-exemples
    sub_examples = list_sub_examples(example_dir)
    if len(sub_examples) > 1:
        print("Plusieurs sous-exemples trouvés :")
        for i, sub_example in enumerate(sub_examples, start=1):
            print(f"{i}. {sub_example}")
        chosen_index = int(input("Sélectionnez le numéro du sous-exemple souhaité : ")) - 1
        example_dir = os.path.join(example_dir, sub_examples[chosen_index])
    
    # Trouver le répertoire de la carte de développement
    board_dir = find_board_dir(example_dir, board_name)
    if not board_dir:
        print("La carte de développement spécifiée n'a pas été trouvée.")
        return
    
    # Trouver le répertoire "CMSIS"
    cmsis_dir = find_cmsis_dir(base_dir)
    if not cmsis_dir:
        print("Le répertoire 'CMSIS' n'a pas été trouvé.")
        return
    
    # Extraire le numéro de modèle de la carte
    model_number = extract_model_number(board_name)
    if not model_number:
        print("Numéro de modèle non trouvé dans le nom de la carte.")
        return

    # Trouver le fichier startup
    dfp_dir = os.path.join(base_dir, "dfp")  # Assurez-vous que le chemin du répertoire dfp est correct
    startup_file = find_startup_file(dfp_dir, model_number)
    if not startup_file:
        print("Fichier startup non trouvé pour le numéro de modèle spécifié.")
        return
    
    # Trouver le fichier include
    include_file = find_include_file(dfp_dir, model_number)
    if not include_file:
        print("Fichier include non trouvé pour le numéro de modèle spécifié.")
        return

    # Copier les fichiers nécessaires sur le bureau
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    destination_dir = os.path.join(desktop_dir, f"{example_name}_{os.path.basename(example_dir)}_extracted")
    copy_example_files(example_dir, board_dir, destination_dir, ide_name, cmsis_dir, startup_file, include_file)
    print(f"Exemple copié dans le répertoire : {destination_dir}")

if __name__ == "__main__":
    main()
