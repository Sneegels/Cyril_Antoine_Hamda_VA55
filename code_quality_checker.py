import os
import sys
import json
import subprocess
import re
import time
from typing import Tuple, Dict, List
from pylint import lint
from pylint.reporters import JSONReporter
from radon.cli import cc
from radon.cli import raw
from radon.cli import mi

def run_flake8(src_path: str, verbose: bool = True) -> Tuple[Dict[str, int], str]:
    """
    Execute Flake8 sur le dossier spécifié, en analysant chaque fichier individuellement
    
    Args:
        src_path: Chemin absolu vers le dossier à analyser
        verbose: Si True, affiche la progression de l'analyse
    
    Returns:
        Tuple[Dict[str, int], str]: (statistiques des erreurs trouvées, chemin du fichier de résultats)
    """
    output_dir = "code_quality_checker_result"
    os.makedirs(output_dir, exist_ok=True)
    flake8_output_file = os.path.join(output_dir, "flake8.txt")
    
    # Initialiser les statistiques
    stats = {
        'style': 0,      # Erreurs de style (E)
        'bugs': 0,       # Bugs potentiels (F)
        'warnings': 0,   # Avertissements (W)
        'bugbear': 0,    # Erreurs Bugbear (B, B9)
        'total': 0
    }
    
    try:
        # Trouver tous les fichiers Python
        python_files = []
        for root, _, files in os.walk(src_path):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        
        if not python_files:
            print("Aucun fichier Python trouvé dans le répertoire.")
            return stats, flake8_output_file
        
        if verbose:
            print(f"Analyse de {len(python_files)} fichiers Python...")
        
        # Analyser chaque fichier individuellement
        with open(flake8_output_file, 'w', encoding='utf-8') as f:
            for i, file_path in enumerate(python_files, 1):
                if verbose:
                    print(f"Analyse du fichier {i}/{len(python_files)}: {os.path.relpath(file_path, src_path)}")
                
                # Configuration de Flake8 pour un seul fichier
                flake8_command = [
                    sys.executable,
                    "-m",
                    "flake8",
                    "--select=E,F,W",
                    "--format=default",
                    file_path
                ]
                
                try:
                    # Exécuter Flake8 sur le fichier
                    process = subprocess.run(
                        flake8_command,
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=5  # Timeout plus court pour un seul fichier
                    )
                    
                    # Écrire les résultats dans le fichier
                    if process.stdout:
                        f.write(process.stdout)
                    
                    # Analyser les erreurs pour ce fichier
                    for line in process.stdout.splitlines():
                        if ':' in line:  # Ligne d'erreur
                            error_code = re.search(r'[EFWB]\d{3}', line)
                            if error_code:
                                code = error_code.group(0)
                                if code.startswith('E'):
                                    stats['style'] += 1
                                elif code.startswith('F'):
                                    stats['bugs'] += 1
                                elif code.startswith('W'):
                                    stats['warnings'] += 1
                                elif code.startswith('B'):
                                    stats['bugbear'] += 1
                                stats['total'] += 1
                
                except subprocess.TimeoutExpired:
                    print(f"  Timeout lors de l'analyse de {os.path.relpath(file_path, src_path)}")
                    f.write(f"Timeout lors de l'analyse de {file_path}\n")
                except Exception as e:
                    print(f"  Erreur lors de l'analyse de {os.path.relpath(file_path, src_path)}: {e}")
                    f.write(f"Erreur lors de l'analyse de {file_path}: {e}\n")
        
        return stats, flake8_output_file
    
    except Exception as e:
        print(f"Erreur lors de l'exécution de Flake8 : {e}")
        return stats, flake8_output_file

def run_bandit(src_path: str) -> Tuple[Dict[str, int], str]:
    """
    Execute Bandit sur le dossier spécifié et sauvegarde les résultats dans un fichier
    
    Args:
        src_path: Chemin absolu vers le dossier à analyser
    
    Returns:
        Tuple[Dict[str, int], str]: (statistiques des problèmes trouvés, chemin du fichier de résultats)
    """
    output_dir = "code_quality_checker_result"
    os.makedirs(output_dir, exist_ok=True)
    bandit_output_file = os.path.join(output_dir, "bandit.txt")
    
    try:
        # Configuration de Bandit
        bandit_command = [
            sys.executable, "-m", "bandit",
            "-r",  # Analyse récursive
            "-ll",  # Log level (low pour tout voir)
            "-i",  # Afficher les informations
            "-f", "txt",  # Format de sortie en texte
            "-o", bandit_output_file,  # Fichier de sortie
            src_path  # Dossier à analyser
        ]
        
        # Exécution de Bandit
        process = subprocess.run(bandit_command, capture_output=True, text=True, check=False)
        
        # Initialiser les statistiques
        stats = {
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0,
            'total_issues': 0
        }
        
        # Analyser la sortie pour compter les problèmes par niveau
        for line in process.stdout.splitlines():
            if "Issue:" in line:
                if "High Severity" in line:
                    stats['HIGH'] += 1
                elif "Medium Severity" in line:
                    stats['MEDIUM'] += 1
                elif "Low Severity" in line:
                    stats['LOW'] += 1
                stats['total_issues'] += 1
        
        return stats, bandit_output_file
    
    except Exception as e:
        print(f"Erreur lors de l'exécution de Bandit : {e}")
        return {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'total_issues': 0}, bandit_output_file

def run_radon(src_path: str) -> Tuple[Dict, str]:
    """
    Execute Radon sur le dossier spécifié et sauvegarde les résultats dans un fichier
    
    Args:
        src_path: Chemin absolu vers le dossier à analyser

    Returns:
        Tuple[Dict, str]: (statistiques, chemin du fichier de résultats)
    """
    output_dir = "code_quality_checker_result"
    os.makedirs(output_dir, exist_ok=True)
    radon_output_file = os.path.join(output_dir, "radon.txt")
    
    try:
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Le dossier n'a pas été trouvé à l'emplacement : {src_path}")

        # Analyse de la complexité cyclomatique
        complexity_command = [
            sys.executable, "-m", "radon", "cc",
            "--min", "A",  # Inclure toutes les fonctions
            "--show-complexity",  # Montrer la complexité
            "--average",  # Calculer la moyenne
            src_path  # Chemin absolu
        ]
        complexity_process = subprocess.run(complexity_command, capture_output=True, text=True)
        
        # Analyse des métriques brutes (LOC, SLOC, etc.)
        raw_command = [sys.executable, "-m", "radon", "raw", src_path]
        raw_process = subprocess.run(raw_command, capture_output=True, text=True, check=False)
        
        # Analyse de l'index de maintenabilité avec l'option --show pour plus de détails
        mi_command = [sys.executable, "-m", "radon", "mi", "--show", src_path]
        mi_process = subprocess.run(mi_command, capture_output=True, text=True, check=False)
        
        if not any([complexity_process.stdout, raw_process.stdout, mi_process.stdout]):
            print(f"Attention: Aucun fichier Python n'a été trouvé dans {src_path}")
        
        # Préparer les statistiques
        stats = {
            'complexity': {
                'A': 0,  # Simple (1-5)
                'B': 0,  # Légèrement complexe (6-10)
                'C': 0,  # Plus complexe (11-20)
                'D': 0,  # Trop complexe (21-30)
                'E': 0,  # Très complexe (31-40)
                'F': 0   # Extrêmement complexe (41+)
            },
            'maintainability': {
                'A': 0,  # Excellent (> 20)
                'B': 0,  # Bon (10-19)
                'C': 0   # Mauvais (0-9)
            }
        }
        
        # Sauvegarder les résultats détaillés et analyser les sorties
        with open(radon_output_file, 'w', encoding='utf-8') as f:
            # Écrire et analyser la complexité cyclomatique
            f.write("=== Analyse de complexité cyclomatique ===\n")
            f.write(complexity_process.stdout)
            
            # Analyser la complexité cyclomatique
            for line in complexity_process.stdout.splitlines():
                if ':' in line and '(' in line:  # Format typique: "function_name (...) - A (1)"
                    complexity_part = line.split('(')[-1].split(')')[0]
                    try:
                        complexity = int(complexity_part)
                        if complexity > 40:
                            stats['complexity']['F'] += 1
                        elif complexity > 30:
                            stats['complexity']['E'] += 1
                        elif complexity > 20:
                            stats['complexity']['D'] += 1
                        elif complexity > 10:
                            stats['complexity']['C'] += 1
                        elif complexity > 5:
                            stats['complexity']['B'] += 1
                        else:
                            stats['complexity']['A'] += 1
                    except ValueError:
                        continue
            
            # Écrire et analyser les métriques brutes
            f.write("\n=== Métriques brutes ===\n")
            f.write(raw_process.stdout)
            
            # Écrire et analyser l'index de maintenabilité
            f.write("\n=== Index de maintenabilité ===\n")
            f.write(mi_process.stdout)
            
            # Analyser l'index de maintenabilité
            for line in mi_process.stdout.splitlines():
                parts = line.split(' - ')
                if len(parts) == 2 and parts[0] and parts[1]:
                    try:
                        score = float(parts[1].strip())
                        if score >= 20:
                            stats['maintainability']['A'] += 1
                        elif score >= 10:
                            stats['maintainability']['B'] += 1
                        else:
                            stats['maintainability']['C'] += 1
                    except ValueError:
                        continue
        
        return stats, radon_output_file
    
    except Exception as e:
        print(f"Erreur lors de l'exécution de Radon : {e}")
        return {'complexity': {}, 'maintainability': {}}, radon_output_file

def run_mypy(src_path: str) -> Tuple[int, str]:
    """
    Execute Mypy sur le dossier spécifié et sauvegarde les résultats dans un fichier
    
    Args:
        src_path: Chemin absolu vers le dossier à analyser

    Returns:
        Tuple[int, str]: (nombre d'erreurs, chemin du fichier de résultats)
    """
    output_dir = "code_quality_checker_result"
    os.makedirs(output_dir, exist_ok=True)
    mypy_output_file = os.path.join(output_dir, "mypy.txt")
    
    try:
        # Configuration de Mypy
        mypy_command = [
            sys.executable, "-m", "mypy",
            src_path,  # Le dossier à analyser
            "--ignore-missing-imports",  # Ignorer les imports non trouvés
            "--follow-imports=skip",  # Ne pas analyser les bibliothèques externes
        ]
        
        # Exécution de Mypy
        process = subprocess.run(
            mypy_command,
            capture_output=True,
            text=True,
            check=False
        )
        
        # Sauvegarder la sortie dans le fichier
        with open(mypy_output_file, 'w', encoding='utf-8') as f:
            f.write(process.stdout)
            if process.stderr:
                f.write("\n=== Erreurs ===\n")
                f.write(process.stderr)
        
        # Compter le nombre d'erreurs
        error_count = len([line for line in process.stdout.splitlines() if "error:" in line])
        
        return error_count, mypy_output_file
    except Exception as e:
        print(f"Erreur lors de l'exécution de Mypy : {e}")
        return 0, mypy_output_file

def run_pylint(src_path: str):
    """
    Execute Pylint sur le dossier spécifié et sauvegarde les résultats dans un fichier
    
    Args:
        src_path: Chemin absolu vers le dossier à analyser
    """
    # Création du dossier de résultats s'il n'existe pas
    output_dir = "code_quality_checker_result"
    os.makedirs(output_dir, exist_ok=True)
    
    # Configuration de Pylint
    pylint_output_file = os.path.join(output_dir, "pylint.txt")
    
    # Options pour Pylint
    pylint_opts = [
        src_path,  # Le dossier à analyser
        "--output-format=text",  # Format de sortie en texte
        f"--output={pylint_output_file}",  # Fichier de sortie
        "--recursive=y"  # Analyse récursive des sous-dossiers
    ]
    
    try:
        # Exécution de Pylint et récupération des résultats
        results = lint.Run(pylint_opts, exit=False)
        print("\nRésumé de l'analyse Pylint:")
        by_msg = results.linter.stats.by_msg
        total_count = sum(by_msg.values())
        warning_count = sum(count for msg_id, count in by_msg.items() if msg_id.startswith('W'))
        error_count = sum(count for msg_id, count in by_msg.items() if msg_id.startswith('E'))
        
        print(f"Nombre total de messages: {total_count}")
        print(f"Nombre d'avertissements: {warning_count}")
        print(f"Nombre d'erreurs: {error_count}")
        print(f"Score global: {results.linter.stats.global_note:.2f}/10")
        print(f"\nLes résultats détaillés sont dans {pylint_output_file}")
    except (ImportError, TypeError) as e:
        print(f"Erreur lors de l'exécution de Pylint : {e}")
        sys.exit(1)

def main():
    """
    Fonction principale qui exécute tous les outils d'analyse de code
    """
    # Configuration du chemin du code source
    src_path = os.path.abspath("src")
    if not os.path.exists(src_path):
        print(f"Erreur : Le dossier 'src' n'a pas été trouvé à l'emplacement : {src_path}")
        sys.exit(1)
    
    print(f"Analyse du code dans : {src_path}")
    
    print("\n=== Exécution de Pylint ===")
    run_pylint(src_path)
    
    print("\n=== Exécution de Mypy ===")
    error_count, mypy_output_file = run_mypy(src_path)
    print(f"\nNombre d'erreurs de typage trouvées : {error_count}")
    print(f"Les résultats détaillés sont dans {mypy_output_file}")
    
    print("\n=== Exécution de Radon ===")
    stats, radon_output_file = run_radon(src_path)
    
    # Afficher les résultats de complexité
    print("\nComplexité cyclomatique:")
    for grade in ['A', 'B', 'C', 'D', 'E', 'F']:
        count = stats['complexity'][grade]
        if count > 0:
            grade_desc = {
                'A': 'Simple (1-5)',
                'B': 'Légèrement complexe (6-10)',
                'C': 'Plus complexe (11-20)',
                'D': 'Trop complexe (21-30)',
                'E': 'Très complexe (31-40)',
                'F': 'Extrêmement complexe (41+)'
            }[grade]
            print(f"  Grade {grade} - {grade_desc}: {count} fonctions")
    
    # Afficher les résultats de maintenabilité
    print("\nIndex de maintenabilité:")
    # Modifier les seuils pour l'index de maintenabilité
    grade_descriptions = {
        'A': 'Excellent (>= 100)',
        'B': 'Bon (85-99)',
        'C': 'À améliorer (< 85)'
    }
    
    # Afficher les résultats de maintenabilité
    has_results = False
    for grade in ['A', 'B', 'C']:
        count = stats['maintainability'][grade]
        if count > 0:
            has_results = True
            print(f"  Grade {grade} - {grade_descriptions[grade]}: {count} fichiers")
    
    if not has_results:
        print("  Aucun résultat de maintenabilité disponible")
    
    print(f"\nLes résultats détaillés sont dans {radon_output_file}")
    
    print("\n=== Exécution de Bandit ===")
    security_stats, bandit_output_file = run_bandit(src_path)
    
    print("\nRésultats de l'analyse de sécurité:")
    severity_descriptions = {
        'HIGH': 'Haute sévérité',
        'MEDIUM': 'Sévérité moyenne',
        'LOW': 'Faible sévérité'
    }
    
    if security_stats['total_issues'] == 0:
        print("  Aucun problème de sécurité détecté")
    else:
        for severity in ['HIGH', 'MEDIUM', 'LOW']:
            count = security_stats[severity]
            if count > 0:
                print(f"  {severity_descriptions[severity]}: {count} problème(s)")
        print(f"\nNombre total de problèmes de sécurité: {security_stats['total_issues']}")
    
    print(f"Les résultats détaillés sont dans {bandit_output_file}")
    
    print("\n=== Exécution de Flake8 ===")
    flake8_stats, flake8_output_file = run_flake8(src_path, verbose=True)
    
    print("\nRésultats de l'analyse Flake8:")
    error_descriptions = {
        'style': 'Erreurs de style (E)',
        'bugs': 'Bugs potentiels (F)',
        'warnings': 'Avertissements (W)',
        'bugbear': 'Problèmes avancés (B/B9)'
    }
    
    if flake8_stats['total'] == 0:
        print("  Aucune erreur détectée")
    else:
        for error_type, description in error_descriptions.items():
            count = flake8_stats[error_type]
            if count > 0:
                print(f"  {description}: {count}")
        print(f"\nNombre total de problèmes: {flake8_stats['total']}")
    
    print(f"Les résultats détaillés sont dans {flake8_output_file}")

if __name__ == "__main__":
    main()
