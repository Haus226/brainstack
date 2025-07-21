from mcp.server.fastmcp import FastMCP
import datetime

# Create FastMCP instance
mcp = FastMCP("My FastMCP Server")

@mcp.tool()
def calculate(operation: str, a: float, b: float) -> str:
    """Perform basic arithmetic calculations
    
    Args:
        operation: The arithmetic operation (add, subtract, multiply, divide)
        a: First number
        b: Second number
    
    Returns:
        The result of the calculation
    """
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero"
        result = a / b
    else:
        return f"Error: Unknown operation '{operation}'. Supported operations: add, subtract, multiply, divide"
    
    return f"Result: {result}"

@mcp.tool()
def get_current_time() -> str:
    """Get the current date and time
    
    Returns:
        Current date and time as a formatted string
    """
    return f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@mcp.tool()
def echo(message: str) -> str:
    """Echo back the input message
    
    Args:
        message: The message to echo back
        
    Returns:
        The echoed message
    """
    return f"Echo: {message}"

@mcp.tool()
def generate_password(length: int = 12, include_symbols: bool = True) -> str:
    """Generate a random password
    
    Args:
        length: Length of the password (default: 12)
        include_symbols: Whether to include symbols (default: True)
        
    Returns:
        A randomly generated password
    """
    import random
    import string
    
    if length < 4:
        return "Error: Password length must be at least 4 characters"
    
    characters = string.ascii_letters + string.digits
    if include_symbols:
        characters += "!@#$%^&*"
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return f"Generated password: {password}"

mcp.run()