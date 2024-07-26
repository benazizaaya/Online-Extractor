import os
import shutil

# Chemin du firmware Cube 2
firmware_base_path = r"C:\Users\PC\Desktop\FWcube2"

# Fonction pour trouver le chemin du projet selon le choix de la carte, de l'exemple et du sous-exemple
def find_project_path(board, example, sub_example=None):
    for root, dirs, files in os.walk(firmware_base_path):
        if board in root and example in root:
            if sub_example:
                if sub_example in root:
                    return root
            else:
                return root
    return None

# Fonction pour copier les fichiers et réorganiser le projet dans un nouveau répertoire
def copy_and_reorganize_project(example, sub_example, ide, project_path, destination_base_path):
    new_dir_name = f"{example}_{ide}" if not sub_example else f"{example}_{sub_example}_{ide}"
    new_dir_path = os.path.join(destination_base_path, new_dir_name)

    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)

    # Copier le répertoire include global (Inc) à partir du dossier HAL
    global_include_path = os.path.join(firmware_base_path, "hal", "Inc")
    if os.path.exists(global_include_path):
        shutil.copytree(global_include_path, os.path.join(new_dir_path, "Inc"))

    if ide == "IAR":
        # Copier le contenu de EWARM
        ewarm_path = os.path.join(project_path, "EWARM")
        if os.path.exists(ewarm_path) and ewarm_path != new_dir_path:
            shutil.copytree(ewarm_path, os.path.join(new_dir_path, "EWARM"))

        # Copier le répertoire src
        src_path = os.path.join(project_path, "src")
        if os.path.exists(src_path) and src_path != new_dir_path:
            shutil.copytree(src_path, os.path.join(new_dir_path, "src"))

        # Copier le répertoire include de l'exemple
        include_path = os.path.join(project_path, "include")
        if os.path.exists(include_path) and include_path != new_dir_path:
            shutil.copytree(include_path, os.path.join(new_dir_path, "include"))

    elif ide == "STM32CubeMX2":
        # Copier le contenu de Core et Drivers
        core_path = os.path.join(project_path, "Core")
        if os.path.exists(core_path) and core_path != new_dir_path:
            shutil.copytree(core_path, os.path.join(new_dir_path, "Core"))

        drivers_path = os.path.join(project_path, "Drivers")
        if os.path.exists(drivers_path) and drivers_path != new_dir_path:
            shutil.copytree(drivers_path, os.path.join(new_dir_path, "Drivers"))

    elif ide == "STM32VSCode":
        # Copier le contenu de src et inc
        src_path = os.path.join(project_path, "src")
        if os.path.exists(src_path) and src_path != new_dir_path:
            shutil.copytree(src_path, os.path.join(new_dir_path, "src"))

        inc_path = os.path.join(project_path, "inc")
        if os.path.exists(inc_path) and inc_path != new_dir_path:
            shutil.copytree(inc_path, os.path.join(new_dir_path, "inc"))

        # Copier le fichier Makefile
        makefile_path = os.path.join(project_path, "Makefile")
        if os.path.exists(makefile_path):
            shutil.copy2(makefile_path, os.path.join(new_dir_path, "Makefile"))

    print(f"Le projet a été copié et réorganisé dans {new_dir_path}")

# Fonction pour lister les sous-exemples d'un exemple
def list_sub_examples(board, example):
    example_path = find_project_path(board, example)
    sub_examples = []
    for item in os.listdir(example_path):
        if os.path.isdir(os.path.join(example_path, item)):
            sub_examples.append(item)
    return sub_examples

# Choix de la carte, de l'exemple, de l'IDE et du chemin de destination
board_choice = input("Entrez le nom de la carte: ")
example_choice = input("Entrez le nom de l'exemple: ")
sub_examples = list_sub_examples(board_choice, example_choice)

sub_example_choice = None
if sub_examples:
    print("Les sous-exemples disponibles sont :")
    for i, sub_example in enumerate(sub_examples):
        print(f"{i + 1}. {sub_example}")
    sub_example_index = int(input("Entrez le numéro du sous-exemple: ")) - 1
    sub_example_choice = sub_examples[sub_example_index]

ide_choice = input("Entrez le nom de l'IDE (IAR, STM32CubeMX2, STM32VSCode): ")
destination_base_path = input("Entrez le chemin de destination: ")

# Trouver le chemin du projet
project_path = find_project_path(board_choice, example_choice, sub_example_choice)

if project_path:
    # Copier et réorganiser le projet dans un nouveau répertoire
    copy_and_reorganize_project(example_choice, sub_example_choice, ide_choice, project_path, destination_base_path)
else:
    print("Projet non trouvé.")
