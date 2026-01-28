"""
Animations Module for Hiring Bias Intelligence Engine

CSS animations and transitions for enhanced UX.
"""

def get_card_animation(delay=0):
    """
    Get CSS for animated card entrance.
    
    Parameters:
    -----------
    delay : float
        Animation delay in seconds
        
    Returns:
    --------
    str
        CSS animation style
    """
    return f"animation: slideInUp 0.6s ease {delay}s backwards;"


def get_fade_in_animation(delay=0):
    """
    Get CSS for fade-in animation.
    
    Parameters:
    -----------
    delay : float
        Animation delay in seconds
        
    Returns:
    --------
    str
        CSS animation style
    """
    return f"animation: fadeIn 0.8s ease {delay}s backwards;"


def create_animated_container(content, animation_type="fadeIn", delay=0):
    """
    Wrap content in an animated container.
    
    Parameters:
    -----------
    content : str
        HTML content to animate
    animation_type : str
        Type of animation (fadeIn, slideInUp, slideInLeft)
    delay : float
        Animation delay in seconds
        
    Returns:
    --------
    str
        HTML with animation wrapper
    """
    return f"""
    <div style="animation: {animation_type} 0.6s ease {delay}s backwards;">
        {content}
    </div>
    """


def create_metric_card(title, value, subtitle="", icon="📊", animated=True):
    """
    Create an animated metric card.
    
    Parameters:
    -----------
    title : str
        Card title
    value : str or float
        Main metric value
    subtitle : str
        Optional subtitle
    icon : str
        Emoji icon
    animated : bool
        Whether to animate the card
        
    Returns:
    --------
    str
        HTML for metric card
    """
    animation = "slide-in-up" if animated else ""
    
    return f"""
    <div class="metric-card {animation}">
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
            <span style="font-size: 2rem;">{icon}</span>
            <span class="metric-label">{title}</span>
        </div>
        <div class="metric-value">{value}</div>
        {f'<div style="color: #b0b0b0; font-size: 0.9rem; margin-top: 0.5rem;">{subtitle}</div>' if subtitle else ''}
    </div>
    """


def create_progress_bar(value, max_value=100, color="#667eea", height="8px"):
    """
    Create an animated progress bar.
    
    Parameters:
    -----------
    value : float
        Current value
    max_value : float
        Maximum value
    color : str
        Bar color
    height : str
        Bar height
        
    Returns:
    --------
    str
        HTML for progress bar
    """
    percentage = (value / max_value * 100) if max_value > 0 else 0
    
    return f"""
    <div style="
        width: 100%;
        height: {height};
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
    ">
        <div style="
            width: {percentage}%;
            height: 100%;
            background: linear-gradient(90deg, {color} 0%, {color}cc 100%);
            border-radius: 10px;
            transition: width 1s ease;
            animation: slideInLeft 1s ease;
        "></div>
    </div>
    """


def create_status_badge(status, text):
    """
    Create a status badge with appropriate styling.
    
    Parameters:
    -----------
    status : str
        Status type (success, warning, error, info)
    text : str
        Badge text
        
    Returns:
    --------
    str
        HTML for status badge
    """
    colors = {
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'info': '#3b82f6',
        'accept': '#10b981',
        'review': '#f59e0b',
        'reject': '#ef4444'
    }
    
    color = colors.get(status.lower(), '#b0b0b0')
    
    return f"""
    <span style="
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        background-color: {color}22;
        border: 1px solid {color}44;
        color: {color};
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        animation: fadeIn 0.5s ease;
    ">
        {text}
    </span>
    """


def create_loading_spinner(text="Loading..."):
    """
    Create a custom loading spinner.
    
    Parameters:
    -----------
    text : str
        Loading text
        
    Returns:
    --------
    str
        HTML for loading spinner
    """
    return f"""
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        gap: 1rem;
    ">
        <div style="
            width: 50px;
            height: 50px;
            border: 4px solid rgba(102, 126, 234, 0.2);
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        "></div>
        <div style="color: #b0b0b0; font-weight: 600;">{text}</div>
    </div>
    <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    """


if __name__ == "__main__":
    print("✓ Animations module created")
    print(f"  - Card animation: {get_card_animation()}")
    print(f"  - Fade in animation: {get_fade_in_animation()}")
