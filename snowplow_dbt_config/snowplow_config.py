# snowplow_config.py
import json
import os
import yaml
from typing import Dict, Any

class SnowplowDbtConfigGenerator:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file not found at {self.config_path}")
            raise
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in configuration file {self.config_path}")
            raise
            
    def generate_project_structure(self, output_dir: str):
        try:
            # project directory
            os.makedirs(output_dir, exist_ok=True)
            
            # project.yml
            project_config = {
                'name': f"snowplow_{self.config['brand_name'].lower().replace(' ', '_')}",
                'version': '1.0.0',
                'config-version': 2,
                'profile': 'default',
                
                'packages': [{
                    'package': 'snowplow/unified',
                    'version': '0.1.0'
                }],
                
                'vars': self._generate_vars()
            }
            
            # Write project.yml
            project_path = os.path.join(output_dir, 'dbt_project.yml')
            with open(project_path, 'w') as f:
                yaml.dump(project_config, f, default_flow_style=False)
            print(f"Generated dbt_project.yml at {project_path}")
            
            # Generate packages.yml
            packages_config = {
                'packages': [
                    {
                        'package': 'snowplow/unified',
                        'version': '0.1.0'
                    }
                ]
            }
            
            # Write packages.yml
            packages_path = os.path.join(output_dir, 'packages.yml')
            with open(packages_path, 'w') as f:
                yaml.dump(packages_config, f, default_flow_style=False)
            print(f"Generated packages.yml at {packages_path}")
            
        except Exception as e:
            print(f"Error generating project structure: {str(e)}")
            raise
            
    def _generate_vars(self) -> Dict[str, Any]:
        vars_config = {
            'snowplow__app_ids': self.config['app_ids'],
            'snowplow__start_date': self.config['historical_data_since'],
            'snowplow__enable_web': self.config['web_tracking'] == 'yes',
            'snowplow__enable_mobile': self.config['mobile_tracking'] == 'yes',
        }
        
        if 'user_set_variables' in self.config:
            vars_config.update(self.config['user_set_variables'])
            
        return vars_config

def process_all_configs():
    """Process all configuration files in the config directory."""
    config_dir = 'config'
    output_base_dir = 'dbt_projects'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_base_dir, exist_ok=True)
    
    # Process each JSON file in the config directory
    for filename in os.listdir(config_dir):
        if filename.endswith('.json'):
            print(f"\nProcessing configuration: {filename}")
            config_path = os.path.join(config_dir, filename)
            brand_name = filename.replace('.json', '')
            output_dir = os.path.join(output_base_dir, brand_name)
            
            try:
                generator = SnowplowDbtConfigGenerator(config_path)
                generator.generate_project_structure(output_dir)
                print(f"Successfully generated project for {brand_name}")
            except Exception as e:
                print(f"Failed to process {filename}: {str(e)}")

if __name__ == '__main__':
    process_all_configs()