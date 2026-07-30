import glob
import re
import os

def get_title(text):
    text_lower = text.lower()
    if 'harmonic' in text_lower or 'shm' in text_lower or 'ddot{x} = -' in text_lower:
        return 'Simple Harmonic Motion'
    elif 'projectile' in text_lower or 'projected' in text_lower or 'angle of elevation' in text_lower or 'horizontal range' in text_lower:
        return 'Projectile Motion'
    elif 'resist' in text_lower or 'drag' in text_lower or 'retardation' in text_lower:
        return 'Resisted Motion'
    elif 'circular' in text_lower:
        return 'Circular Motion'
    elif 'acceleration' in text_lower or 'velocity' in text_lower or 'force' in text_lower:
        return 'Kinematics and Dynamics'
    return 'Mechanics Problem'

for file_path in glob.glob('/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Mechanics/problems/*.tex'):
    with open(file_path, 'r') as f:
        content = f.read()

    # Find all \begin{problem} without []
    # We use a function to replace it
    def replacer(match):
        problem_start = match.start()
        # Find the end of the problem to get the text
        end_idx = content.find(r'\end{problem}', problem_start)
        if end_idx != -1:
            problem_text = content[problem_start:end_idx]
            title = get_title(problem_text)
            return f'\\begin{{problem}}[{title}]'
        return match.group(0)

    new_content = re.sub(r'\\begin\{problem\}(?!\[)', replacer, content)

    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(file_path)}")

