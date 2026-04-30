#!/usr/bin/env python3

import os

def parse_config(filepath):
    sections = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n')
        if '{' in line:
            section_name = line.split('{')[0].strip()
            
            # If the section name is on the previous line (e.g., Browser \n {)
            if not section_name:
                j = i - 1
                while j >= 0 and not lines[j].strip():
                    j -= 1
                if j >= 0:
                    section_name = lines[j].strip()
            
            section_content = []
            i += 1
            bracket_depth = 1
            
            while i < len(lines):
                l = lines[i].rstrip('\n')
                if '{' in l:
                    bracket_depth += 1
                if '}' in l:
                    bracket_depth -= 1
                    if bracket_depth == 0:
                        sections[section_name] = section_content
                        break
                section_content.append(l)
                i += 1
        i += 1
    return sections

def write_config(sections, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        for name, lines in sections.items():
            f.write(f"{name}\n{{\n")
            for line in lines:
                f.write(f"{line}\n")
            f.write("}\n\n")

def merge_configs(base_path, override_path, output_path):
    base_sections = parse_config(base_path)
    override_sections = parse_config(override_path)
    
    for name, lines in override_sections.items():
        if name in base_sections:
            base_sections[name].extend(lines)
        else:
            base_sections[name] = lines
            
    write_config(base_sections, output_path)

if __name__ == "__main__":
    overrides_dir = "./Overrides"
    configs_dir = "./Configs"
    network_file = os.path.join(overrides_dir, "network.txt")
    
    if not os.path.isfile(network_file):
        print(f"Error: {network_file} not found in {overrides_dir}.")
        exit(1)
        
    os.makedirs(configs_dir, exist_ok=True)
    
    for filename in os.listdir(overrides_dir):
        if filename.endswith('.txt') and filename != "network.txt":
            file_path = os.path.join(overrides_dir, filename)
            output_path = os.path.join(configs_dir, filename)
            merge_configs(network_file, file_path, output_path)
            print(f"Merged {filename} -> {output_path}")