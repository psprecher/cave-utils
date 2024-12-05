import re
import json
import sys
from typing import Dict, Any, List
from pathlib import Path
import jsonschema

class TherionConfigParser:
    def __init__(self):
        self.data = {'value': '', 'children': {}}
        
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
        last_key = None
        while i < len(lines):
            line = lines[i].strip()

            # Skip comments and empty lines
            if line.strip().startswith('#') or not line.strip():
                i += 1
                continue

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

            # Ignore other 'end' lines- these are implicitly handled through indentation. Note that
            # this is probably stricter regarding indentation than Therion itself.
            if line.startswith('end') and line.rstrip().isalpha():
                i += 1
                continue

            (key, value) = line.split(maxsplit=1)

            # 'def' keys in metapost code blocks have implicit continuation lines until 'enddef;' is encountered.
            # We need to collect all lines between 'def' and 'enddef;' into a single value.
            if key == 'def':
                code_lines = [value]
                while i + 1 < len(lines):
                    i += 1
                    lstrip = min(len(lines[i]) - len(lines[i].lstrip()), indent_level * 2)
                    next_line = lines[i][lstrip:].rstrip()
                    code_lines.append(next_line)
                    if next_line == 'enddef;':
                        line = '\n'.join(code_lines)
                        break
                value = '\n'.join(code_lines)
                print(f"code block: {value}")

            if indent_level > len(parent_items):
                # We skipped an indentation level- this is an error
                raise ValueError(f"Indentation error: {line}")

            # Trim the parent_items list to the current indentation level if we
            # popped out an indentation level
            parent_items = parent_items[:indent_level]
            parent_item = self.data if not parent_items else parent_items[-1]

            new_item = {'value': value}
            if 'children' not in parent_item:
                parent_item['children'] = {}
            parent_item['children'][key] = parent_item['children'].get(key, []) + [new_item]

            # push the current item to the parent items list, in case the next item is nested
            parent_items.append(new_item)

            i += 1

        return self.data['children']

    def print_file(self, data: Dict[str, Any], indent_level: int = 0) -> str:
        """Convert a parsed Therion config dict back to file format.
        
        Args:
            data: Dict in the format returned by parse_file()
            indent_level: Current indentation level (used recursively)
            
        Returns:
            String containing the Therion config file contents
        """
        output = []
        indent = "  " * indent_level  # Use 2 spaces per level to match parse_file
        
        # Process each key and its list of values
        for key, value_list in data.items():
            for item in value_list:
                # Get the value and any children
                value = item.get('value', '')
                children = item.get('children', {})
                
                # Handle special case of metapost def blocks
                if key == 'def':
                    # Split the value back into lines and maintain indentation
                    lines = value.split('\n')
                    output.append(f"{indent}{key} {lines[0]}")
                    for line in lines[1:]:
                        output.append(f"{indent}{line}")
                else:
                    # Output the key-value pair
                    output.append(f"{indent}{key} {value}")
                
                # Recursively process any children with increased indentation
                if children:
                    child_output = self.print_file(children, indent_level + 1)
                    output.append(child_output)
                    
                    # Add an 'end' line for certain block types that need it
                    if key in ['layout', 'map', 'centerline', 'survey']:
                        output.append(f"{indent}end{key}")
        
        return '\n'.join(output)

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
    config_data = parser.parse_file(sys.argv[1], schema)

    print(config_data)
    
    # Validate against schema
    # if parser.validate_against_schema(schema):
    #     print("Config file successfully validated against schema")
        
    # Print the resulting JSON
    print(json.dumps(config_data, indent=2))

    print("================")
    print(parser.print_file(config_data))


if __name__ == "__main__":
    main()