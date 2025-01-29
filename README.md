# Snowplow dbt Project Configuration Generator
## Developer Guide

This guide explains how to use and extend the Snowplow dbt Project Configuration Generator, a tool designed to automate the creation of dbt project structures for Snowplow customers.

## Overview

The configuration generator is designed to:
1. Read customer-specific JSON configurations
2. Generate appropriate dbt project structures
3. Configure variables based on customer requirements
4. Set up the Snowplow Unified package integration

## Key Components

### SnowplowDbtConfigGenerator Class

The main class responsible for generating dbt project configurations. It handles:

- Loading customer JSON configurations
- Generating project structure
- Setting up appropriate variables
- Creating necessary YAML files

### Configuration Files

The generator expects a JSON configuration file with the following structure:

```json
{
  "brand_name": "Brand Name",
  "brand_summary": "Description of the brand",
  "app_ids": ["list", "of", "app_ids"],
  "historical_data_since": "YYYY-MM-DD",
  "web_tracking": "yes/no",
  "mobile_tracking": "yes/no",
  "user_set_variables": {
    "variable_name": "value"
  }
}
```

## Generated Project Structure

The generator creates:

1. `dbt_project.yml`: Main project configuration file
2. `packages.yml`: Package dependencies file

### Project Naming Convention

Projects are named using the pattern: `snowplow_<brand_name>` where brand_name is lowercase with spaces replaced by underscores.

## Usage

```python
# Initialize the generator
generator = SnowplowDbtConfigGenerator('path/to/config.json')

# Generate project structure
generator.generate_project_structure('output/directory/path')
```

## Variable Configuration

The generator automatically configures:

1. Basic variables:
   - `snowplow__app_ids`: From configuration
   - `snowplow__start_date`: Historical data start date
   - `snowplow__enable_web`: Based on web_tracking setting
   - `snowplow__enable_mobile`: Based on mobile_tracking setting

2. Custom variables:
   - Any variables specified in `user_set_variables` are included in the configuration

## Extending the Generator

To add new configuration options:

1. Add new fields to the JSON schema
2. Extend the `_generate_vars()` method to handle new variables
3. Update the project configuration generation if needed

## Best Practices

1. Always validate JSON configurations before processing
2. Keep package versions up to date
3. Document any custom variables added to the configuration
4. Test generated configurations with dbt before deployment

## Error Handling

The generator includes basic error handling for:
- File not found errors
- Invalid JSON format
- Missing required fields

## Maintenance

Regular maintenance tasks:
1. Update Snowplow package versions


## Support

For issues or questions:
1. Check the Snowplow documentation
2. Review the dbt project configuration
3. Contact the Snowplow support team

