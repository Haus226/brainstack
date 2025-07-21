from mcp.server.fastmcp import FastMCP
import datetime
from typing import Dict, List, Optional

# Create FastMCP instance
mcp = FastMCP("Stateful Demo Server")

# SERVER STATE - This persists across function calls!
class ServerState:
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.user_preferences: Dict = {}
        self.session_data: Dict = {}
        self.calculation_history: List[Dict] = []
        self.connection_count: int = 0
        self.last_activity: Optional[datetime.datetime] = None
        
    def add_conversation(self, user_input: str, response: str):
        self.conversation_history.append({
            'timestamp': datetime.datetime.now(),
            'user': user_input,
            'assistant': response
        })
        self.last_activity = datetime.datetime.now()

# Global state instance - persists across all function calls
state = ServerState()

@mcp.tool()
def start_session(user_name: str) -> str:
    """Start a new user session
    
    Args:
        user_name: Name of the user starting the session
        
    Returns:
        Welcome message with session info
    """
    state.connection_count += 1
    state.session_data['user_name'] = user_name
    state.session_data['session_start'] = datetime.datetime.now()
    state.last_activity = datetime.datetime.now()
    
    response = f"Welcome {user_name}! Session started. You're connection #{state.connection_count}."
    state.add_conversation(f"start_session({user_name})", response)
    
    return response

@mcp.tool()
def set_preference(key: str, value: str) -> str:
    """Set a user preference that persists across calls
    
    Args:
        key: Preference key (e.g., 'theme', 'language', 'timezone')
        value: Preference value
        
    Returns:
        Confirmation message
    """
    state.user_preferences[key] = value
    response = f"Preference set: {key} = {value}"
    state.add_conversation(f"set_preference({key}, {value})", response)
    
    return response

@mcp.tool()
def get_preferences() -> str:
    """Get all stored user preferences
    
    Returns:
        String representation of all preferences
    """
    if not state.user_preferences:
        response = "No preferences set yet."
    else:
        prefs = "\n".join([f"- {k}: {v}" for k, v in state.user_preferences.items()])
        response = f"Your preferences:\n{prefs}"
    
    state.add_conversation("get_preferences()", response)
    return response

@mcp.tool()
def calculate_and_remember(operation: str, a: float, b: float) -> str:
    """Perform calculation and store in history
    
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
        return f"Error: Unknown operation '{operation}'"
    
    # Store in persistent history
    calculation = {
        'timestamp': datetime.datetime.now(),
        'operation': operation,
        'operands': [a, b],
        'result': result,
        'expression': f"{a} {operation} {b} = {result}"
    }
    state.calculation_history.append(calculation)
    
    response = f"Result: {result} (Calculation #{len(state.calculation_history)})"
    state.add_conversation(f"calculate_and_remember({operation}, {a}, {b})", response)
    
    return response

@mcp.tool()
def get_calculation_history() -> str:
    """Get all previous calculations from this session
    
    Returns:
        Formatted list of all calculations
    """
    if not state.calculation_history:
        response = "No calculations performed yet."
    else:
        history = "\n".join([
            f"{i+1}. {calc['expression']} (at {calc['timestamp'].strftime('%H:%M:%S')})"
            for i, calc in enumerate(state.calculation_history)
        ])
        response = f"Calculation History:\n{history}"
    
    state.add_conversation("get_calculation_history()", response)
    return response

@mcp.tool()
def get_conversation_summary() -> str:
    """Get a summary of the current conversation
    
    Returns:
        Summary of conversation history
    """
    if not state.conversation_history:
        return "No conversation history yet."
    
    summary = f"""
Conversation Summary:
- Total interactions: {len(state.conversation_history)}
- Session started: {state.session_data.get('session_start', 'Unknown')}
- User: {state.session_data.get('user_name', 'Anonymous')}
- Last activity: {state.last_activity}
- Calculations performed: {len(state.calculation_history)}
- Preferences set: {len(state.user_preferences)}

Recent interactions:
"""
    
    # Show last 3 interactions
    recent = state.conversation_history[-3:]
    for interaction in recent:
        summary += f"- {interaction['timestamp'].strftime('%H:%M:%S')}: {interaction['user']} → {interaction['assistant'][:50]}...\n"
    
    return summary

@mcp.tool()
def build_on_previous_calculation(operation: str, operand: float) -> str:
    """Use the result of the last calculation as input for a new calculation
    
    Args:
        operation: The arithmetic operation to perform
        operand: The second operand
        
    Returns:
        Result of the new calculation
    """
    if not state.calculation_history:
        return "Error: No previous calculations to build on"
    
    last_result = state.calculation_history[-1]['result']
    
    # This demonstrates TRUE statefulness - using previous results!
    return calculate_and_remember(operation, last_result, operand)

@mcp.tool()
def reset_session() -> str:
    """Reset all session data
    
    Returns:
        Confirmation message
    """
    state.conversation_history.clear()
    state.user_preferences.clear()
    state.session_data.clear()
    state.calculation_history.clear()
    state.last_activity = None
    
    return "Session reset. All data cleared."

@mcp.tool()
def get_server_stats() -> str:
    """Get server statistics (demonstrates persistent server state)
    
    Returns:
        Server statistics
    """
    uptime = datetime.datetime.now() - state.session_data.get('session_start', datetime.datetime.now())
    
    stats = f"""
Server Statistics:
- Total connections: {state.connection_count}
- Current session uptime: {uptime}
- Conversations tracked: {len(state.conversation_history)}
- Calculations performed: {len(state.calculation_history)}
- Preferences stored: {len(state.user_preferences)}
- Last activity: {state.last_activity or 'None'}
"""
    
    return stats

# Run the server
# if __name__ == "__main__":
#     print("Starting Stateful MCP Server...")
#     print("This server maintains state across function calls!")
#     mcp.run()
mcp.run()