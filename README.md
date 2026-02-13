# joy-config 🎮

A simple, flexible Python configuration loader that automatically detects and loads project configuration files.

## ✨ Features

- **🔄 Multiple Format Support**: Compatible with YAML, JSON, INI, ENV, and other configuration file formats
- **🔍 Auto Detection**: Automatically finds and loads configuration files in your project without requiring explicit paths
- **🌍 Environment Awareness**: Loads environment-specific configuration files based on environment variables
- **🔗 Config Merging**: Intelligently merges base configurations with environment-specific overrides
- **🔑 Flexible Access**: Access configuration values via attributes or dictionary-style lookups
- **📊 Nested Configuration**: Full support for nested configuration structures

## 📦 Installation

```bash
pip install joy-config
```

## 🚀 Quick Start

### Auto-loading Configuration

```python
from joy_config.loader import auto_loader

# Automatically detect and load configuration files in your project
config = auto_loader()

# Access configuration items
db_host = config.database.host
# or
db_host = config['database.host']
# or with default value
db_host = config.get('database.host', 'localhost')
```

### Specifying Configuration Files

```python
from joy_config.loader import auto_loader

# Specify a configuration file path
config = auto_loader('config/app_config.yaml')

# Specify an environment
config = auto_loader(env='production')
```

## 📄 Supported Configuration Formats

### YAML 📝

```yaml
database:
  host: localhost
  port: 5432
  username: admin
  password: secret

app:
  debug: false
  log_level: info
```

### JSON 📝

```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "username": "admin",
    "password": "secret"
  },
  "app": {
    "debug": false,
    "log_level": "info"
  }
}
```

### INI 📝

```ini
[database]
host = localhost
port = 5432
username = admin
password = secret

[app]
debug = false
log_level = info
```

### Environment Variables (.env) 📝

```env
DATABASE_HOST=localhost 
DATABASE_PORT=5432 
DATABASE_USERNAME=admin 
DATABASE_PASSWORD=secret 
APP_DEBUG=false 
APP_LOG_LEVEL=info
```

## 🌐 Environment-Specific Configuration

joy-config supports loading different configuration files based on the current environment:

1. 🔍 Automatically detects the current environment from environment variables (ENV, ENVIRONMENT, or PROFILE)
2. 📁 Looks for environment-specific configuration files like `config-dev.yaml`, `application-prod.json`, etc.
3. 🔄 Intelligently merges base configuration with environment-specific overrides

Example:

```python
# With environment variable ENV=dev
config = auto_loader()  # Will automatically load both config.yaml and config-dev.yaml
```

## 🔧 Advanced Usage

### Configuration Merging 🔄

```python
# Base config (config.yaml)
# database:
#   host: localhost
#   port: 5432
#   username: admin

# Environment config (config-prod.yaml)
# database:
#   host: db.example.com
#   password: prod-secret

# Merged configuration
# config.database.host == "db.example.com"
# config.database.port == 5432
# config.database.username == "admin"
# config.database.password == "prod-secret"
```

### Converting to Dictionary 🔄

```python
# Convert the configuration object to a dictionary
config_dict = config.as_dict()
```

## 📜 License

MIT

---

This README provides comprehensive information about the project's main features, installation instructions, usage examples, and advanced usage patterns. The document is structured to help users quickly understand how to use the library effectively. 🚀