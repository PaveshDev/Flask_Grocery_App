"""
UI Components and Utilities for Modern Grocery App
Extracted from modern_app.py to keep it clean and maintainable
"""
import tkinter as tk
from datetime import datetime, timedelta
import calendar


class UIColors:
    """Color theme for the application"""
    COLORS = {
        'primary': '#8B3FD9',      # Purple (main brand)
        'primary_dark': '#6D2DAD', # Darker purple
        'secondary': '#FFC107',    # Gold/Amber accent
        'accent': '#2196F3',       # Blue accent
        'accent_light': '#E3F2FD', # Light blue
        'danger': '#F44336',       # Red
        'success': '#4CAF50',      # Green
        'bg': '#F8F9FA',          # Light background
        'bg_secondary': '#FFFFFF', # White
        'card': '#FFFFFF',         # White cards
        'card_shadow': '#E0E0E0',  # Shadow color
        'text': '#212121',         # Dark text
        'text_light': '#757575',   # Medium gray
        'text_muted': '#BDBDBD',   # Light gray
        'border': '#EEEEEE',       # Light border
        'input_bg': '#F5F5F5',     # Input background
        'input_border': '#DDDDDD', # Input border
        'hover': '#F5F5F5',        # Hover state
        'rating': '#FFC107',       # Yellow for ratings
        'badge': '#FF4081'         # Pink for badges
    }

    @classmethod
    def get_colors(cls):
        """Get all colors"""
        return cls.COLORS.copy()


class ColorUtils:
    """Utility functions for color manipulation"""
    
    @staticmethod
    def darken_color(color_hex):
        """Darken a hex color by reducing brightness"""
        # Remove '#' if present
        color_hex = color_hex.lstrip('#')
        
        # Convert hex to RGB
        try:
            r = int(color_hex[0:2], 16)
            g = int(color_hex[2:4], 16)
            b = int(color_hex[4:6], 16)
        except:
            return color_hex
        
        # Darken by reducing each component
        r = max(0, int(r * 0.8))
        g = max(0, int(g * 0.8))
        b = max(0, int(b * 0.8))
        
        # Convert back to hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    @staticmethod
    def lighten_color(color):
        """Lighten a hex color by 20% for hover effect"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, int(c * 1.15)) for c in rgb)
        return '#%02x%02x%02x' % lighter


class UIComponentFactory:
    """Factory for creating modern UI components"""
    
    def __init__(self, colors):
        """Initialize with color scheme"""
        self.colors = colors
    
    def create_button(self, parent, text, command, style='primary', width=20):
        """Create modern e-commerce button with smooth effects"""
        bg_color = self.colors.get(style, self.colors['primary'])
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            padx=25,
            pady=12,
            width=width,
            cursor='hand2',
            borderwidth=0,
            activebackground=self.colors['primary_dark'],
            activeforeground='white',
            highlightthickness=0
        )
        
        # Smooth hover effect
        def on_enter(e):
            btn.config(bg=self.colors['primary_dark'])
        
        def on_leave(e):
            btn.config(bg=bg_color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        return btn
    
    def create_entry(self, parent, show=None, width=30):
        """Create modern entry field"""
        entry = tk.Entry(
            parent,
            font=('Segoe UI', 11),
            relief=tk.SOLID,
            borderwidth=1,
            show=show,
            width=width,
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            highlightthickness=0
        )
        return entry
    
    def create_label(self, parent, text, font_size=11, bold=False, color='text'):
        """Create styled label"""
        font_weight = 'bold' if bold else 'normal'
        label = tk.Label(
            parent,
            text=text,
            font=('Segoe UI', font_size, font_weight),
            bg=self.colors['card'] if parent.cget('bg') == self.colors['card'] else self.colors['bg'],
            fg=self.colors[color]
        )
        return label
    
    def create_card(self, parent, **kwargs):
        """Create clean white card with subtle shadow"""
        card = tk.Frame(
            parent,
            bg=self.colors['card'],
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            **kwargs
        )
        return card


class AnimationUtils:
    """Utility functions for animations"""
    
    @staticmethod
    def pulse_animation(widget, color1, color2, step=0):
        """Create pulsing animation effect"""
        if step < 3:
            widget.after(100, lambda: AnimationUtils.pulse_animation(widget, color1, color2, step + 1))
    
    @staticmethod
    def fade_in(widget, alpha=0):
        """Fade in animation for widgets"""
        if alpha < 1.0:
            alpha += 0.1
            widget.after(30, lambda: AnimationUtils.fade_in(widget, alpha))
    
    @staticmethod
    def slide_in(widget, start_x, end_x, current_x=None):
        """Slide in animation from left or right"""
        if current_x is None:
            current_x = start_x
        
        if abs(current_x - end_x) > 5:
            current_x += (end_x - start_x) * 0.2
            widget.place(x=current_x)
            widget.after(20, lambda: AnimationUtils.slide_in(widget, start_x, end_x, current_x))


class CalendarPickerDialog:
    """Calendar picker dialog for date selection"""
    
    def __init__(self, root, colors, date_entry_field):
        """Initialize calendar picker"""
        self.root = root
        self.colors = colors
        self.date_entry_field = date_entry_field
        
        # Create window
        self.cal_window = tk.Toplevel(self.root)
        self.cal_window.title("Pick Date")
        self.cal_window.geometry("400x350")
        self.cal_window.resizable(False, False)
        self.cal_window.grab_set()
        self.cal_window.transient(self.root)
        
        self.current_date = datetime.now()
        self.selected_date = [self.current_date]
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the calendar UI"""
        # Header frame
        header_frame = tk.Frame(self.cal_window, bg=self.colors['primary'])
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.month_year_label = tk.Label(
            header_frame,
            text=self.current_date.strftime("%B %Y"),
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        self.month_year_label.pack(pady=10)
        
        # Navigation frame
        nav_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        nav_frame.pack(pady=5)
        
        tk.Button(
            nav_frame,
            text="< Prev",
            command=self._prev_month,
            bg=self.colors['secondary'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            padx=10,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            nav_frame,
            text="Next >",
            command=self._next_month,
            bg=self.colors['secondary'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            padx=10,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        # Calendar grid
        self.cal_grid_frame = tk.Frame(self.cal_window, bg=self.colors['bg'])
        self.cal_grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._draw_calendar(self.current_date)
        
        # Close button
        btn_frame = tk.Frame(self.cal_window, bg=self.colors['bg'])
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            btn_frame,
            text="✕ Close",
            command=self.cal_window.destroy,
            bg=self.colors['text_light'],
            fg=self.colors['text'],
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        ).pack(fill=tk.X)
    
    def _prev_month(self):
        """Go to previous month"""
        prev_date = self.selected_date[0] - timedelta(days=self.selected_date[0].day)
        self._update_calendar(prev_date)
    
    def _next_month(self):
        """Go to next month"""
        first_of_month = self.selected_date[0].replace(day=1)
        next_date = first_of_month + timedelta(days=32)
        next_date = next_date.replace(day=1)
        self._update_calendar(next_date)
    
    def _update_calendar(self, date_obj):
        """Update calendar display"""
        self.selected_date[0] = date_obj
        self.month_year_label.config(text=date_obj.strftime("%B %Y"))
        
        # Clear previous calendar
        for widget in self.cal_grid_frame.winfo_children():
            widget.destroy()
        
        self._draw_calendar(date_obj)
    
    def _draw_calendar(self, date_obj):
        """Draw calendar for given date"""
        year = date_obj.year
        month = date_obj.month
        
        # Weekday headers
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(weekdays):
            tk.Label(
                self.cal_grid_frame,
                text=day,
                font=('Segoe UI', 9, 'bold'),
                bg=self.colors['primary'],
                fg='white',
                width=5,
                relief=tk.RAISED,
                bd=1
            ).grid(row=0, column=i, sticky='nsew', padx=2, pady=2)
        
        # Get calendar matrix
        cal_matrix = calendar.monthcalendar(year, month)
        
        # Display dates
        for week_num, week in enumerate(cal_matrix, 1):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Empty cell
                    tk.Label(
                        self.cal_grid_frame,
                        text='',
                        bg=self.colors['bg'],
                        width=5,
                        height=2
                    ).grid(row=week_num, column=day_num, sticky='nsew', padx=2, pady=2)
                else:
                    # Date button
                    is_today = (day == datetime.now().day and 
                               month == datetime.now().month and 
                               year == datetime.now().year)
                    
                    btn_bg = self.colors['accent'] if is_today else self.colors['card']
                    btn_fg = 'white' if is_today else self.colors['text']
                    
                    def select_date(d=day, m=month, y=year):
                        """Select date and close window"""
                        selected = datetime(y, m, d).strftime('%Y-%m-%d')
                        self.date_entry_field.config(state=tk.NORMAL)
                        self.date_entry_field.delete(0, tk.END)
                        self.date_entry_field.insert(0, selected)
                        self.date_entry_field.config(state=tk.DISABLED)
                        self.cal_window.destroy()
                    
                    btn = tk.Button(
                        self.cal_grid_frame,
                        text=str(day),
                        command=select_date,
                        bg=btn_bg,
                        fg=btn_fg,
                        font=('Segoe UI', 10, 'bold'),
                        width=5,
                        height=2,
                        relief=tk.RAISED,
                        bd=1,
                        cursor='hand2'
                    )
                    btn.grid(row=week_num, column=day_num, sticky='nsew', padx=2, pady=2)
                    
                    # Hover effect
                    def on_enter(event, button=btn):
                        if button['text'].strip():
                            button.config(bg=self.colors['primary'], fg='white')
                    
                    def on_leave(event, button=btn, bg=btn_bg, fg=btn_fg):
                        if button['text'].strip():
                            button.config(bg=bg, fg=fg)
                    
                    btn.bind('<Enter>', on_enter)
                    btn.bind('<Leave>', on_leave)
