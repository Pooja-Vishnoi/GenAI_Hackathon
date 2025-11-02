from functools import wraps
import inspect

def tool(description: str):
    """
    A decorator to mark a method as a tool that can be used by an agent.
    
    Args:
        description: A description of what the tool does.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Attach tool metadata to the function object
        wrapper._is_tool = True
        wrapper._tool_description = description
        wrapper._tool_name = func.__name__
        
        # Introspect parameter and return types
        sig = inspect.signature(func)
        parameters = {
            name: str(param.annotation) if param.annotation != inspect.Parameter.empty else 'Any'
            for name, param in sig.parameters.items() if name != 'self'
        }
        return_type = str(sig.return_annotation) if sig.return_annotation != inspect.Signature.empty else 'Any'
        
        wrapper._tool_metadata = {
            'name': func.__name__,
            'description': description,
            'parameters': parameters,
            'returns': return_type
        }
        
        return wrapper
    return decorator
