import glob
import re
import os

for file_path in glob.glob('/Users/vuhung/00.Work/00.Workspace/math-olympiad-ml/HSC-Mechanics/problems/*.tex'):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Split by \begin{problem} to process each problem block
    parts = content.split('\\begin{problem}')
    new_content = parts[0]
    
    for part in parts[1:]:
        # If it already has a title, skip (though we know they don't, but just in case it's [Title])
        if part.startswith('['):
            new_content += '\\begin{problem}' + part
            continue
        
        title = "Mechanics Problem"
        
        # Find the next takeaways block
        takeaways_match = re.search(r'\\begin\{takeaways\}(.*?)\\end\{takeaways\}', part, re.DOTALL)
        if takeaways_match:
            takeaways_text = takeaways_match.group(1)
            # Find the first \textbf{...}
            textbf_match = re.search(r'\\textbf\{([^}]+)\}', takeaways_text)
            if textbf_match:
                title = textbf_match.group(1)
                # Remove trailing colon if it exists
                if title.endswith(':'):
                    title = title[:-1]
        
        new_content += f'\\begin{{problem}}[{title}]' + part
    
    if new_content != content:
        with open(file_path, 'w') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(file_path)}")

