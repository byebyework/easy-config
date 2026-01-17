from easy_config.base_loader.dotenv_loader import dotenv_loader


def test_dotenv_loader():
    # Test with a valid .env file
    config = dotenv_loader(".env")
    assert config["env"] == "dev"
    assert config["username"] == "username"
    assert config['password'] == '123456'
    
    # Test with a non-existent .env file
    config = dotenv_loader("nonexistent.env")
    assert config == {}
    
    # Test with a .env file that contains invalid lines
    config = dotenv_loader("invalid.env")
    assert config == {} 
    
    # Test with a .env file that contains empty lines and comments
    config = dotenv_loader("empty_and_comments.env")
    assert config == {} 
    
    # Test with a .env file that contains duplicate keys
    config = dotenv_loader("duplicate_keys.env")
    assert config["KEY1"] == "value2"  # The last occurrence of the key should be used  
    
    # Test with a .env file that contains keys with spaces around the equals sign
    config = dotenv_loader("spaces_around_equals.env")
    assert config["KEY1"] == "value1"
    assert config["KEY2"] == "value2"
       
    # Test with a .env file that contains keys with spaces around the equals sign
    config = dotenv_loader("spaces_around_equals.env")
    assert config["KEY1"] == "value1"        