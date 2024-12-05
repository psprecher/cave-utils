import re
import json
import sys
from typing import Dict, Any, List
from pathlib import Path
import jsonschema

class TherionConfigParser:
    def __init__(self):
        self.data = {
            "encoding": None,
            "source": None,
            "layouts": {},
            "select": [],
            "export": []
        }
        
    def parse_file(self, filepath: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Parse a Therion config file and return a JSON-compatible dict."""
        current_layout = None
        current_code_block = None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        i = 0

        append_line = '' # Used for continuation lines
        indent_level = 0

        # The active item is the last item processed- any lines with a greater indent level than
        # 'active_indent_level' will be nested under it.
        #
        # We only support therion files that use 2-space indentation.
        parent_items = []
        while i < len(lines):
            # Skip comments and empty lines
            if line.strip().startswith('#') or not line.strip():
                i += 1
                continue

            line = lines[i].strip()
            if append_line:
                line = append_line + ' ' + line
                append_line = ''
            else:
                indent = len(lines[i]) - len(lines[i].lstrip())
                indent_level = indent // 2

            # Handle continuation lines
            if line.endswith('\\'):
                append_line = line.rstrip('\\').rstrip()
                i += 1
                continue

            # Ignore 'end' lines- these are implicitly handled through indentation. Note that
            # this is probably stricter regarding indentation than Therion itself.
            if line.startswith('end'):
                i += 1
                continue

            if indent_level > len(parent_items):
                # We skipped an indentation level- this is an error
                raise ValueError(f"Indentation error: {line}")

            parent_items = parent_items[:indent_level]

            (key, value) = line.split(maxsplit=1)
            # Default to self.data if we don't have a parent item
            parent_item = parent_items[-1] if parent_items else self.data
            parent_item[key] = parent_item.get(key, []) + [value]

            # Parse encoding
            if line.startswith('encoding'):
                self.data['encoding'] = line.split()[1]
                
            # Parse source
            elif line.startswith('source'):
                self.data['source'] = line.split()[1]
                
            # Parse layout blocks
            elif line.startswith('layout'):
                layout_name = line.split()[1]
                current_layout = {}
                self.data['layouts'][layout_name] = current_layout
                i += 1
                
                # Process layout block
                while i < len(lines) and not lines[i].strip().startswith('layout'):
                    layout_line = lines[i].strip()
                    
                    # Handle code blocks
                    if layout_line.startswith('code'):
                        code_type = layout_line.split()[1]
                        code_content = []
                        i += 1
                        while i < len(lines) and not lines[i].strip().startswith('enddef;'):
                            code_content.append(lines[i])
                            i += 1
                        if code_type not in current_layout:
                            current_layout['code'] = {}
                        current_layout['code'][code_type] = ''.join(code_content)
                    
                    # Handle simple key-value pairs
                    elif layout_line and not layout_line.startswith('#'):
                        try:
                            key, *values = layout_line.split()
                            # Handle numeric values
                            if all(v.isdigit() for v in values):
                                current_layout[key] = [int(v) for v in values]
                            else:
                                current_layout[key] = ' '.join(values).strip('"')
                        except ValueError:
                            pass
                    i += 1
                continue
                
            # Parse select statements
            elif line.startswith('select'):
                self.data['select'].append(line.split()[1])
                
            # Parse export statements
            elif line.startswith('export'):
                export_data = {}
                export_parts = re.findall(r'-(\w+(?:-\w+)*)\s+([^-][^\s]*)', line)
                for key, value in export_parts:
                    if key == 'layout-map-header':
                        # Parse the three values for layout-map-header
                        header_values = value.split()
                        export_data[key] = [
                            float(header_values[0]),
                            float(header_values[1]),
                            header_values[2]
                        ]
                    else:
                        export_data[key] = value
                self.data['export'].append(export_data)
                
            i += 1
            
        return self.data

    def validate_against_schema(self, schema: Dict[str, Any]) -> bool:
        """Validate the parsed data against the provided JSON schema."""
        try:
            jsonschema.validate(instance=self.data, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            print(f"Validation error: {e}")
            return False

def main():
    # Load the schema
    with open('thconfig.schema.json') as f:
        schema = json.load(f)

    # Parse the config file
    parser = TherionConfigParser()

    if len(sys.argv) < 2:
        print("Please provide a config filename as argument")
        sys.exit(1)
    config_data = parser.parse_file(sys.argv[1])
    
    # Validate against schema
    if parser.validate_against_schema(schema):
        print("Config file successfully validated against schema")
        
    # Print the resulting JSON
    print(json.dumps(config_data, indent=2))

if __name__ == "__main__":
    main()