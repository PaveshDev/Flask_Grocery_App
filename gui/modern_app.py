"""
Modern E-Commerce Grocery App - Main Application
GUI Layer that uses service-based architecture
"""
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.db_config import connect_db
except ImportError:
    from db_config import connect_db

# Import UI components
from gui.ui_components import (
    UIColors,
    UIComponentFactory,
    ColorUtils,
    AnimationUtils,
    CalendarPickerDialog
)

# Import services
from services import (
    UserService,
    ProductService,
    OrderService,
    InventoryService,
    ImageService
)


class ModernGroceryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("buyMe Grocery Stores")
        self.root.geometry("1200x800")
        self.root.configure(bg='#FAFAFA')
        
        # User session
        self.current_user = None
        self.current_staff = None
        self.user_type = None  # 'customer' or 'staff'
        
        # Screen state tracking
        self.current_screen = 'login'
        self.login_tab = 'customer'
        self.current_category = None
        
        # Get color scheme from UIColors
        self.colors = UIColors.get_colors()
        
        # Create UI component factory
        self.ui_factory = UIComponentFactory(self.colors)
        
        # Image cache
        self.image_cache = {}
        
        # Ensure image directory exists
        ImageService.ensure_image_directory()
        
        # Start with login screen
        self.show_login_screen()
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.image_cache.clear()
    
    # ==================== UI WRAPPER METHODS ====================
    # These methods delegate to UIComponentFactory and utility classes
    
    def create_button(self, parent, text, command, style='primary', width=20):
        """Create modern button using UI factory"""
        return self.ui_factory.create_button(parent, text, command, style, width)
    
    def create_entry(self, parent, show=None, width=30):
        """Create modern entry using UI factory"""
        return self.ui_factory.create_entry(parent, show, width)
    
    def create_label(self, parent, text, font_size=11, bold=False, color='text'):
        """Create styled label using UI factory"""
        return self.ui_factory.create_label(parent, text, font_size, bold, color)
    
    def create_card(self, parent, **kwargs):
        """Create card using UI factory"""
        return self.ui_factory.create_card(parent, **kwargs)
    
    def darken_color(self, color_hex):
        """Darken color using ColorUtils"""
        return ColorUtils.darken_color(color_hex)
    
    def _darken_color(self, color):
        """Darken color helper"""
        return self.darken_color(color)
    
    def _lighten_color(self, color):
        """Lighten color using ColorUtils"""
        return ColorUtils.lighten_color(color)
    
    def open_calendar_picker(self, date_entry_field):
        """Open calendar picker dialog"""
        CalendarPickerDialog(self.root, self.colors, date_entry_field)
    
    def pulse_animation(self, widget, color1, color2, step=0):
        """Pulse animation using AnimationUtils"""
        AnimationUtils.pulse_animation(widget, color1, color2, step)
    
    def fade_in(self, widget, alpha=0):
        """Fade in animation using AnimationUtils"""
        AnimationUtils.fade_in(widget, alpha)
    
    def slide_in(self, widget, start_x, end_x, current_x=None):
        """Slide in animation using AnimationUtils"""
        AnimationUtils.slide_in(widget, start_x, end_x, current_x)
    
    # ==================== LOGIN & REGISTRATION ====================
    
    def show_login_screen(self):
        """Show anime-themed login screen with dynamic effects"""
        self.clear_window()
        self.current_screen = 'login'
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Center container with fixed dimensions
        center_container = tk.Frame(main_frame, bg=self.colors['bg'])
        center_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Left side - Orange Branding
        left_frame = tk.Frame(center_container, bg=self.colors['primary'], width=400, height=650,
                             highlightthickness=1, highlightbackground=self.colors['primary_dark'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 0))
        left_frame.pack_propagate(False)
        
        # Branding content
        brand_content = tk.Frame(left_frame, bg=self.colors['primary'])
        brand_content.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Minimal app icon
        tk.Label(
            brand_content,
            text="🛒",
            font=('Segoe UI', 72),
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=(0, 30))
        
        # App name - buyMe branding
        tk.Label(
            brand_content,
            text="buyMe",
            font=('Segoe UI', 36, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=(0, 5))
        
        tk.Label(
            brand_content,
            text="Grocery Stores",
            font=('Segoe UI', 18),
            bg=self.colors['primary'],
            fg='white'
        ).pack(pady=(0, 30))
        
        # Minimal divider
        tk.Label(
            brand_content,
            text="─────────────",
            font=('Segoe UI', 14),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        ).pack(pady=(0, 20))
        
        # Sophisticated tagline
        tk.Label(
            brand_content,
            text="Premium quality delivered",
            font=('Segoe UI', 11),
            bg=self.colors['primary'],
            fg='white',
            wraplength=300
        ).pack()
        
        # Right side - Login form with sigma aesthetic
        right_frame = tk.Frame(center_container, bg=self.colors['card'], width=450, height=650,
                              highlightthickness=1, highlightbackground=self.colors['border'])
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        right_frame.pack_propagate(False)
        
        # Form container with padding
        form_container = tk.Frame(right_frame, bg=self.colors['card'])
        form_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=60)
        
        # Welcome text - minimal and clean
        tk.Label(
            form_container,
            text="Welcome Back",
            font=('Segoe UI', 28, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 5))
        
        tk.Label(
            form_container,
            text="Sign in to continue",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack(anchor='w', pady=(0, 30))
        
        # User type selection (Anime-styled tabs)
        user_type_var = tk.StringVar(value=self.login_tab)  # Restore previous tab selection
        
        tab_frame = tk.Frame(form_container, bg=self.colors['card'])
        tab_frame.pack(fill=tk.X, pady=(0, 25))
        
        def select_tab(tab_type):
            user_type_var.set(tab_type)
            self.login_tab = tab_type  # Save tab selection
            # Update tab styles - clean orange theme
            if tab_type == 'customer':
                customer_tab.config(bg=self.colors['primary'], fg='white')
                staff_tab.config(bg=self.colors['bg'], fg=self.colors['text_light'])
            else:
                staff_tab.config(bg=self.colors['primary'], fg='white')
                customer_tab.config(bg=self.colors['bg'], fg=self.colors['text_light'])
        
        customer_tab = tk.Label(
            tab_frame,
            text="Customer",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'] if self.login_tab == 'customer' else self.colors['bg'],
            fg='white' if self.login_tab == 'customer' else self.colors['text_light'],
            padx=30,
            pady=14,
            cursor='hand2',
            relief=tk.FLAT
        )
        customer_tab.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        customer_tab.bind('<Button-1>', lambda e: select_tab('customer'))
        
        staff_tab = tk.Label(
            tab_frame,
            text="Staff/Admin",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['primary'] if self.login_tab == 'staff' else self.colors['bg'],
            fg='white' if self.login_tab == 'staff' else self.colors['text_light'],
            padx=30,
            pady=14,
            cursor='hand2',
            relief=tk.FLAT
        )
        staff_tab.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        staff_tab.bind('<Button-1>', lambda e: select_tab('staff'))
        
        # Username field - minimal sigma design
        tk.Label(
            form_container,
            text="Username",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack(anchor='w', pady=(0, 8))
        
        username_frame = tk.Frame(form_container, bg=self.colors['input_bg'], 
                                 highlightbackground=self.colors['border'], highlightthickness=1)
        username_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            username_frame,
            text="👤",
            font=('Segoe UI', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT, padx=(12, 8))
        
        username_entry = tk.Entry(
            username_frame,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary']
        )
        username_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=12, padx=(0, 12))
        
        # Password field - minimal sigma design
        tk.Label(
            form_container,
            text="Password",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack(anchor='w', pady=(0, 8))
        
        password_frame = tk.Frame(form_container, bg=self.colors['input_bg'], 
                                 highlightbackground=self.colors['border'], highlightthickness=1)
        password_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(
            password_frame,
            text="🔒",
            font=('Segoe UI', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT, padx=(12, 8))
        
        password_entry = tk.Entry(
            password_frame,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            show="●",
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['primary']
        )
        password_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=12, padx=(0, 12))
        
        # Login button
        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            user_type = user_type_var.get()
            
            if not username or not password:
                messagebox.showerror("Error", "Please enter username and password")
                return
            
            if user_type == 'customer':
                user = UserService.login_user(username, password)
                if user:
                    self.current_user = user
                    self.user_type = 'customer'
                    messagebox.showinfo("Success", f"Welcome {user[1]}!")
                    self.show_customer_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid credentials")
            else:
                staff = UserService.login_staff(username, password)
                if staff:
                    self.current_staff = staff
                    self.user_type = 'staff'
                    messagebox.showinfo("Success", f"Welcome {staff[4]}!")
                    self.show_admin_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid credentials")
        
        self.create_button(
            form_container,
            "Login",
            do_login,
            'primary'
        ).pack(fill=tk.X, pady=(0, 15))
        
        # Register section (only for customers)
        register_section = tk.Frame(form_container, bg=self.colors['card'])
        register_section.pack(fill=tk.X)
        
        # Divider
        divider_frame = tk.Frame(register_section, bg=self.colors['card'])
        divider_frame.pack(fill=tk.X, pady=15)
        
        tk.Frame(divider_frame, bg=self.colors['border'], height=1).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(
            divider_frame,
            text="  OR  ",
            font=('Segoe UI', 9),
            bg=self.colors['card'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT)
        tk.Frame(divider_frame, bg=self.colors['border'], height=1).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Register button
        register_btn = tk.Button(
            register_section,
            text="Create New Account",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['primary'],
            relief=tk.FLAT,
            padx=20,
            pady=12,
            cursor='hand2',
            borderwidth=1,
            highlightbackground=self.colors['primary'],
            highlightthickness=1,
            command=self.show_registration_screen
        )
        register_btn.pack(fill=tk.X)
        register_btn.bind('<Enter>', lambda e: register_btn.config(bg=self.colors['hover']))
        register_btn.bind('<Leave>', lambda e: register_btn.config(bg=self.colors['card']))
        
        # Update select_tab to show/hide register section
        def update_select_tab(tab_type):
            select_tab(tab_type)
            if tab_type == 'customer':
                register_section.pack(fill=tk.X)
            else:
                register_section.pack_forget()
        
        customer_tab.bind('<Button-1>', lambda e: update_select_tab('customer'))
        staff_tab.bind('<Button-1>', lambda e: update_select_tab('staff'))

        
    def show_registration_screen(self):
        """Show modern registration screen"""
        self.clear_window()
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Center container
        center_container = tk.Frame(main_frame, bg=self.colors['bg'])
        center_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Registration card with fixed dimensions
        card = tk.Frame(center_container, bg=self.colors['card'], width=550, height=700)
        card.pack(fill=tk.BOTH, padx=20, pady=20)
        card.pack_propagate(False)
        
        # Scrollable form
        canvas = tk.Canvas(card, bg=self.colors['card'], highlightthickness=0)
        scrollbar = tk.Scrollbar(card, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['card'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form container
        form_container = tk.Frame(scrollable_frame, bg=self.colors['card'])
        form_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)
        
        # Header
        tk.Label(
            form_container,
            text="Create Account",
            font=('Segoe UI', 28, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 5))
        
        tk.Label(
            form_container,
            text="Join us and start shopping today!",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack(anchor='w', pady=(0, 30))
        
        # Form fields
        fields = {}
        
        # Username
        tk.Label(
            form_container,
            text="Username",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 8))
        
        username_frame = tk.Frame(form_container, bg=self.colors['input_bg'], highlightbackground=self.colors['border'], highlightthickness=1)
        username_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            username_frame,
            text="👤",
            font=('Segoe UI', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT, padx=(12, 8))
        
        username_entry = tk.Entry(
            username_frame,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        )
        username_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=12, padx=(0, 12))
        fields['username'] = username_entry
        
        # Password
        tk.Label(
            form_container,
            text="Password",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 8))
        
        password_frame = tk.Frame(form_container, bg=self.colors['input_bg'], highlightbackground=self.colors['border'], highlightthickness=1)
        password_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            password_frame,
            text="🔒",
            font=('Segoe UI', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT, padx=(12, 8))
        
        password_entry = tk.Entry(
            password_frame,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            show="●",
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        )
        password_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=12, padx=(0, 12))
        fields['password'] = password_entry
        
        # Email
        tk.Label(
            form_container,
            text="Email",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 8))
        
        email_frame = tk.Frame(form_container, bg=self.colors['input_bg'], highlightbackground=self.colors['border'], highlightthickness=1)
        email_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            email_frame,
            text="📧",
            font=('Segoe UI', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT, padx=(12, 8))
        
        email_entry = tk.Entry(
            email_frame,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        )
        email_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=12, padx=(0, 12))
        fields['email'] = email_entry
        
        # Full Name
        tk.Label(
            form_container,
            text="Full Name",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 8))
        
        name_frame = tk.Frame(form_container, bg=self.colors['input_bg'], highlightbackground=self.colors['border'], highlightthickness=1)
        name_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            name_frame,
            text="✏️",
            font=('Segoe UI', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT, padx=(12, 8))
        
        name_entry = tk.Entry(
            name_frame,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        )
        name_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=12, padx=(0, 12))
        fields['full_name'] = name_entry
        
        # Phone
        tk.Label(
            form_container,
            text="Phone",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 8))
        
        phone_frame = tk.Frame(form_container, bg=self.colors['input_bg'], highlightbackground=self.colors['border'], highlightthickness=1)
        phone_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            phone_frame,
            text="📱",
            font=('Segoe UI', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT, padx=(12, 8))
        
        phone_entry = tk.Entry(
            phone_frame,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text']
        )
        phone_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=12, padx=(0, 12))
        fields['phone'] = phone_entry
        
        # Address
        tk.Label(
            form_container,
            text="Address",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 8))
        
        address_frame = tk.Frame(form_container, bg=self.colors['input_bg'], highlightbackground=self.colors['border'], highlightthickness=1)
        address_frame.pack(fill=tk.X, pady=(0, 25))
        
        tk.Label(
            address_frame,
            text="🏠",
            font=('Segoe UI', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['text_muted']
        ).pack(side=tk.LEFT, padx=(12, 8), anchor='n', pady=12)
        
        address_entry = tk.Text(
            address_frame,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bg=self.colors['input_bg'],
            fg=self.colors['text'],
            insertbackground=self.colors['text'],
            height=3,
            width=30
        )
        address_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=12, padx=(0, 12))
        fields['address'] = address_entry
        
        def do_register():
            username = fields['username'].get().strip()
            password = fields['password'].get().strip()
            email = fields['email'].get().strip()
            full_name = fields['full_name'].get().strip()
            phone = fields['phone'].get().strip()
            address = fields['address'].get("1.0", tk.END).strip()
            
            if not all([username, password, email, full_name, phone, address]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            try:
                success, result = UserService.register_user(username, password, email, full_name, phone, address)
                if success:
                    messagebox.showinfo("Success", "Registration successful! Please login.")
                    self.show_login_screen()
                else:
                    messagebox.showerror("Error", "Registration failed. Username might already exist.")
            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {str(e)}")
        
        self.create_button(
            form_container,
            "Create Account",
            do_register,
            'success'
        ).pack(fill=tk.X, pady=(0, 15))
        
        # Back to login
        back_frame = tk.Frame(form_container, bg=self.colors['card'])
        back_frame.pack(fill=tk.X)
        
        tk.Label(
            back_frame,
            text="Already have an account?",
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).pack(side=tk.LEFT)
        
        login_link = tk.Label(
            back_frame,
            text=" Login here",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['primary'],
            cursor='hand2'
        )
        login_link.pack(side=tk.LEFT)
        login_link.bind('<Button-1>', lambda e: self.show_login_screen())
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    # ==================== CUSTOMER DASHBOARD ====================
    
    def show_customer_dashboard(self):
        """Show customer main dashboard - Modern e-commerce design"""
        self.clear_window()
        self.current_screen = 'customer_dashboard'
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Modern Header
        header = tk.Frame(self.root, bg='white', height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='white')
        header_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=15)
        
        # Greeting message
        tk.Label(
            header_content,
            text=f"Hello, {self.current_user[4] or self.current_user[1]}!",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        # Right side - Notification and Logout
        right_header = tk.Frame(header_content, bg='white')
        right_header.pack(side=tk.RIGHT)
        
        unread_count = OrderService.get_unread_count(self.current_user[0])
        notif_text = f"🔔" if unread_count == 0 else f"🔔 {unread_count}"
        
        notif_btn = tk.Label(
            right_header,
            text=notif_text,
            font=('Segoe UI', 18),
            bg='white',
            fg=self.colors['primary'] if unread_count > 0 else self.colors['text_light'],
            cursor='hand2'
        )
        notif_btn.pack(side=tk.LEFT, padx=15)
        notif_btn.bind('<Button-1>', lambda e: self.show_notifications())
        
        # Logout button
        logout_btn = tk.Button(
            right_header,
            text="🚪 Logout",
            command=self.logout,
            bg='#E53935',
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2',
            borderwidth=0
        )
        logout_btn.pack(side=tk.LEFT, padx=10)
        logout_btn.bind('<Enter>', lambda e: logout_btn.config(bg='#C62828'))
        logout_btn.bind('<Leave>', lambda e: logout_btn.config(bg='#E53935'))
        
        # Divider
        tk.Frame(self.root, bg=self.colors['border'], height=1).pack(fill=tk.X)
        
        # Main content - centered layout
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=80, pady=60)
        
        # Title for menu section
        tk.Label(
            main_frame,
            text="What would you like to do?",
            font=('Segoe UI', 14),
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        ).pack(pady=(0, 50))
        
        # Menu cards grid
        menu_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        menu_frame.pack(expand=True)
        
        menus = [
            ("🛍️", "Shop Now", "Browse products by category", self.show_shop_screen, self.colors['primary']),
            ("🛒", "My Cart", "View and manage your cart", self.show_cart_screen, '#FFC107'),
            ("📦", "My Orders", "Track your orders", self.show_order_history, '#2196F3'),
            ("👤", "My Profile", "Manage your account", self.show_profile_screen, '#4CAF50'),
        ]
        
        row_frame = None
        for i, (icon, title, desc, command, color) in enumerate(menus):
            if i % 2 == 0:
                row_frame = tk.Frame(menu_frame, bg=self.colors['bg'])
                row_frame.pack(pady=20)
            
            # Card container
            card = tk.Frame(row_frame, bg='white', relief=tk.FLAT, borderwidth=0,
                          highlightthickness=2, highlightbackground='#E0E0E0')
            card.pack(side=tk.LEFT, padx=25, fill=tk.BOTH, expand=True)
            card.config(width=280, height=180)
            card.pack_propagate(False)
            
            # Make card clickable
            card.bind('<Button-1>', lambda e, cmd=command: cmd())
            card.config(cursor='hand2')
            
            # Content frame inside card
            content = tk.Frame(card, bg='white', cursor='hand2')
            content.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
            content.bind('<Button-1>', lambda e, cmd=command: cmd())
            
            # Icon
            icon_label = tk.Label(
                content,
                text=icon,
                font=('Segoe UI', 40),
                bg='white',
                fg=color,
                cursor='hand2'
            )
            icon_label.pack(pady=(0, 10))
            icon_label.bind('<Button-1>', lambda e, cmd=command: cmd())
            
            # Title
            title_label = tk.Label(
                content,
                text=title,
                font=('Segoe UI', 13, 'bold'),
                bg='white',
                fg=self.colors['text'],
                cursor='hand2'
            )
            title_label.pack()
            title_label.bind('<Button-1>', lambda e, cmd=command: cmd())
            
            # Description
            desc_label = tk.Label(
                content,
                text=desc,
                font=('Segoe UI', 10),
                bg='white',
                fg=self.colors['text_light'],
                cursor='hand2'
            )
            desc_label.pack(pady=(5, 20))
            desc_label.bind('<Button-1>', lambda e, cmd=command: cmd())
            
            # Button
            btn = tk.Button(
                content,
                text="Open →",
                command=command,
                bg=color,
                fg='white',
                font=('Segoe UI', 11, 'bold'),
                relief=tk.FLAT,
                padx=35,
                pady=12,
                cursor='hand2',
                borderwidth=0
            )
            btn.pack()
            
            # Hover effect for button
            def on_btn_enter(e, button=btn, original_color=color):
                button.config(bg=self.darken_color(original_color))
            
            def on_btn_leave(e, button=btn, original_color=color):
                button.config(bg=original_color)
            
            btn.bind('<Enter>', on_btn_enter)
            btn.bind('<Leave>', on_btn_leave)
            
            # Card hover effect
            def on_card_enter(e, card_widget=card, color_val=color):
                card_widget.config(highlightbackground=color_val, highlightthickness=3)
            
            def on_card_leave(e, card_widget=card):
                card_widget.config(highlightbackground='#E0E0E0', highlightthickness=2)
            
            card.bind('<Enter>', on_card_enter)
            card.bind('<Leave>', on_card_leave)
            
            # Bind all child widgets to card hover
            for widget in content.winfo_children():
                widget.bind('<Enter>', on_card_enter)
                widget.bind('<Leave>', on_card_leave)
    
    def show_shop_screen(self):
        """Show product browsing screen - Modern Daraz-inspired design"""
        self.clear_window()
        self.current_screen = 'shop'
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Modern Header with search
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Header content container
        header_content = tk.Frame(header, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        # Left: Back button
        back_btn = tk.Label(
            header_content,
            text="←",
            font=('Segoe UI', 20),
            bg=self.colors['primary'],
            fg='white',
            cursor='hand2'
        )
        back_btn.pack(side=tk.LEFT, padx=(0, 15))
        back_btn.bind('<Button-1>', lambda e: self.show_customer_dashboard())
        
        # Center: Title
        tk.Label(
            header_content,
            text="Grocery Shop",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT)
        
        # Right: Search and icons
        right_icons = tk.Frame(header_content, bg=self.colors['primary'])
        right_icons.pack(side=tk.RIGHT)
        
        search_icon = tk.Label(
            right_icons,
            text="🔍",
            font=('Segoe UI', 16),
            bg=self.colors['primary'],
            fg='white',
            cursor='hand2'
        )
        search_icon.pack(side=tk.LEFT, padx=10)
        
        # Search bar section (below header)
        search_section = tk.Frame(self.root, bg=self.colors['primary'], height=60)
        search_section.pack(fill=tk.X)
        search_section.pack_propagate(False)
        
        search_container = tk.Frame(search_section, bg=self.colors['primary'])
        search_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=12)
        
        search_entry = tk.Entry(
            search_container,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bg='white',
            fg=self.colors['text_light'],
            insertbackground=self.colors['primary'],
            width=50
        )
        search_entry.pack(fill=tk.X, ipady=10)
        search_entry.insert(0, "Search for products...")
        
        def clear_search(e):
            if search_entry.get() == "Search for products...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg=self.colors['text'])
        
        def restore_search(e):
            if not search_entry.get():
                search_entry.insert(0, "Search for products...")
                search_entry.config(fg=self.colors['text_light'])
        
        def on_search_change(*args):
            search_term = search_entry.get()
            if search_term and search_term != "Search for products...":
                results = search_products(search_term)
                self.display_search_results(results, product_frame)
            elif not search_term or search_term == "Search for products...":
                self.load_products(None, product_frame)
        
        search_entry.bind('<FocusIn>', clear_search)
        search_entry.bind('<FocusOut>', restore_search)
        search_entry.bind('<KeyRelease>', on_search_change)
        
        # Main content area - Categories sidebar + Products grid
        content = tk.Frame(self.root, bg=self.colors['bg'])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Categories sidebar
        sidebar = tk.Frame(content, bg=self.colors['card'], width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5), pady=10)
        sidebar.pack_propagate(False)
        
        tk.Label(
            sidebar,
            text="Categories",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(pady=15)
        
        categories = ProductService.get_all_categories()
        
        # All products button
        btn = tk.Button(
            sidebar,
            text="🏪 All Products",
            command=lambda: self.load_products(None, product_frame),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text'],
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            anchor='w',
            padx=20,
            pady=10,
            cursor='hand2',
            activebackground=self.colors['hover'],
            activeforeground=self.colors['text']
        )
        btn.pack(fill=tk.X, padx=10, pady=2)
        btn.bind('<Enter>', lambda e: btn.config(bg=self.colors['hover']))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.colors['bg_secondary']))
        
        # Category buttons
        for cat in categories:
            cat_id, cat_name, icon = cat
            btn = tk.Button(
                sidebar,
                text=f"{icon} {cat_name}",
                command=lambda cid=cat_id: self.load_products(cid, product_frame),
                bg=self.colors['bg_secondary'],
                fg=self.colors['text'],
                font=('Segoe UI', 11),
                relief=tk.FLAT,
                anchor='w',
                padx=20,
                pady=10,
                cursor='hand2',
                activebackground=self.colors['hover'],
                activeforeground=self.colors['text']
            )
            btn.pack(fill=tk.X, padx=10, pady=2)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['hover']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.colors['bg_secondary']))
        
        # Products area with scrollbar
        products_container = tk.Frame(content, bg=self.colors['bg'])
        products_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)
        
        canvas = tk.Canvas(products_container, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(products_container, orient="vertical", command=canvas.yview)
        product_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        product_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=product_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load all products initially
        self.load_products(None, product_frame)
    
    def load_products(self, category_id, container):
        """Load and display products"""
        # Clear container
        for widget in container.winfo_children():
            widget.destroy()
        
        products = ProductService.get_products_by_category(category_id)
        
        if not products:
            tk.Label(
                container,
                text="No products available",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['text_light']
            ).pack(pady=50)
            return
        
        # Display products in grid (3 columns)
        row_frame = None
        for i, product in enumerate(products):
            if i % 3 == 0:
                row_frame = tk.Frame(container, bg=self.colors['bg'])
                row_frame.pack(fill=tk.X, pady=10, padx=10)
            
            self.create_product_card(row_frame, product)
    
    def display_search_results(self, products, container):
        """Display search results"""
        # Clear container
        for widget in container.winfo_children():
            widget.destroy()
        
        if not products:
            tk.Label(
                container,
                text="No products found",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['text_light']
            ).pack(pady=50)
            return
        
        # Display products in grid (3 columns)
        row_frame = None
        for i, product in enumerate(products):
            if i % 3 == 0:
                row_frame = tk.Frame(container, bg=self.colors['bg'])
                row_frame.pack(fill=tk.X, pady=10, padx=10)
            
            self.create_product_card(row_frame, product)
    
    def create_product_card(self, parent, product):
        """Create modern e-commerce product card (Daraz-style) for grid layout"""
        card = tk.Frame(parent, bg=self.colors['card'], relief=tk.FLAT, borderwidth=0,
                       highlightthickness=1, highlightbackground=self.colors['border'])
        card.pack(side=tk.LEFT, padx=8, pady=8)
        card.pack_propagate(False)
        card.config(width=200, height=280)
        
        # Product image container
        image_container = tk.Frame(card, bg=self.colors['input_bg'], height=150)
        image_container.pack(fill=tk.X, padx=0, pady=0)
        image_container.pack_propagate(False)
        
        image_label = tk.Label(image_container, bg=self.colors['input_bg'])
        image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        try:
            if product[3]:
                img = ImageService.load_image_for_display(product[3], (150, 150))
                self.image_cache[f"product_{product[0]}"] = img
                image_label.config(image=img)
            else:
                image_label.config(text="📦", font=('Segoe UI', 40), fg=self.colors['text_muted'])
        except Exception as e:
            print(f"Error loading image: {e}")
            image_label.config(text="📦", font=('Segoe UI', 40), fg=self.colors['text_muted'])
        
        # Discount badge (if applicable)
        if product[8] > 0:
            badge = tk.Label(
                image_container,
                text=f"-{int(product[8])}%",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['badge'],
                fg='white',
                padx=8,
                pady=4
            )
            badge.place(relx=0.05, rely=0.08)
        
        # Product info container
        info_frame = tk.Frame(card, bg=self.colors['card'])
        info_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        # Product name
        tk.Label(
            info_frame,
            text=product[1][:20],
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text'],
            anchor='w',
            justify='left',
            wraplength=150
        ).pack(anchor='w', pady=(0, 4))
        
        # Category
        tk.Label(
            info_frame,
            text=product[9][:15],
            font=('Segoe UI', 8),
            bg=self.colors['card'],
            fg=self.colors['text_light'],
            anchor='w'
        ).pack(anchor='w', pady=(0, 8))
        
        # Price row
        price = product[4]
        discount = product[8]
        final_price = price * (1 - discount / 100) if discount > 0 else price
        
        price_frame = tk.Frame(info_frame, bg=self.colors['card'])
        price_frame.pack(anchor='w', pady=(0, 8))
        
        tk.Label(
            price_frame,
            text=f"LKR {final_price:.2f}",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['primary']
        ).pack(side=tk.LEFT)
        
        if discount > 0:
            tk.Label(
                price_frame,
                text=f" LKR {price:.2f}",
                font=('Segoe UI', 9),
                bg=self.colors['card'],
                fg=self.colors['text_light']
            ).pack(side=tk.LEFT)
        
        # Add to cart button
        def add_to_cart_action():
            if product[6] > 0:
                success, msg = OrderService.add_to_cart(self.current_user[0], product[0], 1)
                if success:
                    messagebox.showinfo("Success", "Added to cart!")
                else:
                    messagebox.showerror("Error", msg)
            else:
                messagebox.showwarning("Out of Stock", "Product is out of stock")
        
        add_btn = tk.Button(
            info_frame,
            text="Add to Cart",
            command=add_to_cart_action,
            bg=self.colors['primary'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            padx=0,
            pady=8,
            cursor='hand2',
            borderwidth=0
        )
        add_btn.pack(fill=tk.X)
        add_btn.bind('<Enter>', lambda e: add_btn.config(bg=self.colors['primary_dark']))
        add_btn.bind('<Leave>', lambda e: add_btn.config(bg=self.colors['primary']))
        
        # Hover effect for the entire card
        def on_enter(e):
            card.config(highlightbackground=self.colors['primary'], highlightthickness=2)
        
        def on_leave(e):
            card.config(highlightbackground=self.colors['border'], highlightthickness=1)
        
        # Click to open product detail
        def on_card_click(e):
            self.show_product_detail(product)
        
        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)
        card.bind('<Button-1>', on_card_click)
        
        # Bind all child widgets to same events
        for widget in card.winfo_children():
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            widget.bind('<Button-1>', on_card_click)
    
    def show_product_detail(self, product):
        """Show product detail screen - Professional PC-optimized design"""
        self.clear_window()
        self.root.configure(bg=self.colors['bg'])
        
        stock = product[6]
        price = product[4]
        discount = product[8]
        final_price = price * (1 - discount / 100) if discount > 0 else price
        sold_count = ProductService.get_product_sold_count(product[0])
        
        # ==== HEADER ====
        header = tk.Frame(self.root, bg='white', height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='white')
        header_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=15)
        
        # Back button
        back_btn = tk.Label(
            header_content,
            text="← Back to Shop",
            font=('Segoe UI', 12),
            bg='white',
            fg=self.colors['primary'],
            cursor='hand2'
        )
        back_btn.pack(side=tk.LEFT)
        back_btn.bind('<Button-1>', lambda e: self.show_shop_screen())
        
        # Breadcrumb/Title
        tk.Label(
            header_content,
            text=f"/ {product[1][:30]}",
            font=('Segoe UI', 11),
            bg='white',
            fg=self.colors['text_light']
        ).pack(side=tk.LEFT, padx=15)
        
        # Divider line below header
        tk.Frame(self.root, bg=self.colors['border'], height=1).pack(fill=tk.X)
        
        # ==== MAIN CONTENT (Two-column layout) ====
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # LEFT COLUMN - Image
        left_column = tk.Frame(main_container, bg=self.colors['bg'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 60))
        
        # Product image container
        image_bg = tk.Frame(left_column, bg='white', width=450, height=500)
        image_bg.pack(side=tk.TOP)
        image_bg.pack_propagate(False)
        
        image_label = tk.Label(image_bg, bg='white')
        image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        try:
            if product[3]:
                img = ImageService.load_image_for_display(product[3], (400, 400))
                self.image_cache[f"product_detail_{product[0]}"] = img
                image_label.config(image=img)
            else:
                image_label.config(text="📦", font=('Segoe UI', 120), fg=self.colors['text_muted'])
        except Exception as e:
            print(f"Error loading image: {e}")
            image_label.config(text="📦", font=('Segoe UI', 120), fg=self.colors['text_muted'])
        
        # Image navigation dots
        dots_frame = tk.Frame(left_column, bg=self.colors['bg'])
        dots_frame.pack(pady=20)
        for i in range(4):
            color = self.colors['primary'] if i == 0 else '#E0E0E0'
            tk.Label(dots_frame, text="●", font=('Segoe UI', 12), bg=self.colors['bg'], fg=color).pack(side=tk.LEFT, padx=8)
        
        # RIGHT COLUMN - Product Info (Scrollable)
        right_scroll_frame = tk.Frame(main_container, bg=self.colors['bg'])
        right_scroll_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(right_scroll_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(right_scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        right_column = scrollable_frame
        
        # Product name
        tk.Label(
            right_column,
            text=product[1],
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text'],
            wraplength=500,
            justify='left'
        ).pack(anchor='w', pady=(0, 20))
        
        # Sold count info (from database)
        sold_info = tk.Frame(right_column, bg=self.colors['bg'])
        sold_info.pack(anchor='w', pady=(0, 20))
        
        tk.Label(
            sold_info,
            text=f"Units Sold: {sold_count}",
            font=('Segoe UI', 11),
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        ).pack(side=tk.LEFT)
        
        # Divider
        tk.Frame(right_column, bg=self.colors['border'], height=2).pack(fill=tk.X, pady=20)
        
        # ==== PRICING SECTION ====
        price_main = tk.Frame(right_column, bg=self.colors['bg'])
        price_main.pack(fill=tk.X, pady=(0, 25))
        
        # Current price (large)
        tk.Label(
            price_main,
            text=f"LKR {final_price:.2f}",
            font=('Segoe UI', 40, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['primary']
        ).pack(side=tk.LEFT)
        
        if discount > 0:
            price_info = tk.Frame(price_main, bg=self.colors['bg'])
            price_info.pack(side=tk.LEFT, padx=25)
            
            tk.Label(
                price_info,
                text=f"LKR {price:.2f}",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['text_light']
            ).pack(anchor='w')
            
            discount_badge = tk.Frame(price_info, bg=self.colors['badge'], highlightthickness=0)
            discount_badge.pack(anchor='w', pady=(8, 0))
            
            tk.Label(
                discount_badge,
                text=f"  Save {int(discount)}%  ",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['badge'],
                fg='white',
                padx=10,
                pady=4
            ).pack()
        
        # Divider
        tk.Frame(right_column, bg=self.colors['border'], height=1).pack(fill=tk.X, pady=20)
        
        # ==== PRODUCT SPECIFICATIONS (Only Category, Unit, Stock) ====
        spec_title = tk.Label(
            right_column,
            text="Product Details",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        spec_title.pack(anchor='w', pady=(0, 15))
        
        specs_data = [
            ("Category", product[9]),
            ("Unit", product[5]),
            ("Stock Available", f"{stock} units")
        ]
        
        for label, value in specs_data:
            spec_row = tk.Frame(right_column, bg=self.colors['bg'])
            spec_row.pack(fill=tk.X, pady=8)
            
            tk.Label(
                spec_row,
                text=label + ":",
                font=('Segoe UI', 10),
                bg=self.colors['bg'],
                fg=self.colors['text_light'],
                width=20,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                spec_row,
                text=value,
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack(side=tk.LEFT)
        
        # Divider
        tk.Frame(right_column, bg=self.colors['border'], height=1).pack(fill=tk.X, pady=20)
        
        # ==== DESCRIPTION ====
        if product[2]:
            desc_title = tk.Label(
                right_column,
                text="Description",
                font=('Segoe UI', 13, 'bold'),
                bg=self.colors['bg'],
                fg=self.colors['text']
            )
            desc_title.pack(anchor='w', pady=(0, 12))
            
            desc_label = tk.Label(
                right_column,
                text=product[2],
                font=('Segoe UI', 11),
                bg=self.colors['bg'],
                fg=self.colors['text_light'],
                wraplength=500,
                justify='left',
                anchor='w'
            )
            desc_label.pack(anchor='w', pady=(0, 40))
        
        # ==== ACTION BUTTONS (Fixed at bottom) ====
        button_container = tk.Frame(self.root, bg='white', height=130)
        button_container.pack(fill=tk.X, side=tk.BOTTOM)
        button_container.pack_propagate(False)
        
        # Divider
        tk.Frame(button_container, bg=self.colors['border'], height=1).pack(fill=tk.X)
        
        button_content = tk.Frame(button_container, bg='white')
        button_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=15)
        
        # Quantity selector section
        qty_section = tk.Frame(button_content, bg='white')
        qty_section.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            qty_section,
            text="Quantity:",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        # Quantity frame with minus, input, plus buttons
        qty_frame = tk.Frame(qty_section, bg='white')
        qty_frame.pack(side=tk.LEFT, padx=(15, 0))
        
        qty_var = tk.StringVar(value="1")
        
        def decrease_qty():
            try:
                current = int(qty_var.get())
                if current > 1:
                    qty_var.set(str(current - 1))
            except:
                qty_var.set("1")
        
        def increase_qty():
            try:
                current = int(qty_var.get())
                if current < stock:
                    qty_var.set(str(current + 1))
            except:
                qty_var.set("1")
        
        # Minus button
        minus_btn = tk.Button(
            qty_frame,
            text="−",
            command=decrease_qty,
            bg=self.colors['border'],
            fg=self.colors['text'],
            font=('Segoe UI', 14, 'bold'),
            relief=tk.FLAT,
            width=3,
            height=1,
            cursor='hand2',
            borderwidth=0
        )
        minus_btn.pack(side=tk.LEFT)
        
        # Quantity input
        qty_input = tk.Entry(
            qty_frame,
            textvariable=qty_var,
            font=('Segoe UI', 11, 'bold'),
            width=5,
            justify=tk.CENTER,
            relief=tk.SOLID,
            borderwidth=1
        )
        qty_input.pack(side=tk.LEFT, padx=5)
        
        # Plus button
        plus_btn = tk.Button(
            qty_frame,
            text="＋",
            command=increase_qty,
            bg=self.colors['border'],
            fg=self.colors['text'],
            font=('Segoe UI', 14, 'bold'),
            relief=tk.FLAT,
            width=3,
            height=1,
            cursor='hand2',
            borderwidth=0
        )
        plus_btn.pack(side=tk.LEFT)
        
        # Stock info
        tk.Label(
            qty_section,
            text=f"(Available: {stock})",
            font=('Segoe UI', 10),
            bg='white',
            fg=self.colors['text_light']
        ).pack(side=tk.LEFT, padx=(20, 0))
        
        def add_to_cart_action():
            try:
                quantity = int(qty_var.get())
                if quantity < 1:
                    messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity")
                    return
                if quantity > stock:
                    messagebox.showwarning("Insufficient Stock", f"Only {stock} units available")
                    return
                success, msg = OrderService.add_to_cart(self.current_user[0], product[0], quantity)
                if success:
                    messagebox.showinfo("Success", f"✓ Added {quantity} item(s) to cart!")
                    self.show_shop_screen()
                else:
                    messagebox.showerror("Error", msg)
            except:
                messagebox.showwarning("Invalid Input", "Please enter a valid quantity")
        
        # Add to Cart Button (full width below quantity selector)
        add_cart_btn = tk.Button(
            button_content,
            text="🛒  Add to Cart",
            command=add_to_cart_action,
            bg=self.colors['primary'],
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            pady=16,
            cursor='hand2',
            borderwidth=0
        )
        add_cart_btn.pack(fill=tk.X)
        add_cart_btn.bind('<Enter>', lambda e: add_cart_btn.config(bg=self.colors['primary_dark']))
        add_cart_btn.bind('<Leave>', lambda e: add_cart_btn.config(bg=self.colors['primary']))
    
    def show_cart_screen(self):
        """Show shopping cart"""
        self.clear_window()
        self.current_screen = 'cart'
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['secondary'], height=60)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="🛒 My Shopping Cart",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['secondary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        self.create_button(header, "Back", self.show_customer_dashboard, 
                          'primary', 10).pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        cart_items = OrderService.get_cart_items(self.current_user[0])
        
        if not cart_items:
            tk.Label(
                main_frame,
                text="Your cart is empty! 🛒",
                font=('Segoe UI', 16),
                bg=self.colors['bg'],
                fg=self.colors['text_light']
            ).pack(pady=100)
            
            self.create_button(
                main_frame,
                "Start Shopping",
                self.show_shop_screen,
                'primary'
            ).pack()
            return
        
        # Cart items list
        items_frame = tk.Frame(main_frame, bg=self.colors['card'])
        items_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        total_amount = 0
        
        for item in cart_items:
            cart_id, product_id, name, image, price, quantity, subtotal, stock, discount = item
            
            item_card = tk.Frame(items_frame, bg=self.colors['card'], relief=tk.SOLID, borderwidth=1)
            item_card.pack(fill=tk.X, padx=10, pady=5)
            
            # Product info
            info_frame = tk.Frame(item_card, bg=self.colors['card'])
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            tk.Label(
                info_frame,
                text=name,
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['card'],
                fg=self.colors['text']
            ).pack(anchor='w')
            
            tk.Label(
                info_frame,
                text=f"₹{price:.2f} × {quantity} = ₹{subtotal:.2f}",
                font=('Segoe UI', 11),
                bg=self.colors['card'],
                fg=self.colors['text_light']
            ).pack(anchor='w', pady=5)
            
            # Controls
            control_frame = tk.Frame(item_card, bg=self.colors['card'])
            control_frame.pack(side=tk.RIGHT, padx=10, pady=10)
            
            # Quantity update
            qty_frame = tk.Frame(control_frame, bg=self.colors['card'])
            qty_frame.pack(side=tk.LEFT, padx=10)
            
            tk.Button(
                qty_frame,
                text="-",
                command=lambda cid=cart_id, q=quantity: self.update_cart(cid, q-1),
                bg=self.colors['secondary'],
                fg='white',
                width=2,
                cursor='hand2'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                qty_frame,
                text=str(quantity),
                font=('Segoe UI', 11, 'bold'),
                bg=self.colors['card'],
                fg=self.colors['text'],
                width=3
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Button(
                qty_frame,
                text="+",
                command=lambda cid=cart_id, q=quantity: self.update_cart(cid, q+1),
                bg=self.colors['secondary'],
                fg='white',
                width=2,
                cursor='hand2'
            ).pack(side=tk.LEFT)
            
            # Remove button
            tk.Button(
                control_frame,
                text="🗑️ Remove",
                command=lambda cid=cart_id: self.remove_cart_item(cid),
                bg=self.colors['danger'],
                fg='white',
                font=('Segoe UI', 9),
                relief=tk.FLAT
            ).pack(side=tk.LEFT, padx=10)
            
            total_amount += subtotal
        
        # Total and checkout
        total_frame = self.create_card(main_frame)
        total_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            total_frame,
            text=f"Total Amount: ₹{total_amount:.2f}",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['primary']
        ).pack(pady=20)
        
        self.create_button(
            total_frame,
            "Proceed to Checkout",
            self.show_checkout_screen,
            'success',
            25
        ).pack(pady=(0, 20))
    
    def update_cart(self, cart_id, new_quantity):
        """Update cart item quantity"""
        if new_quantity <= 0:
            self.remove_cart_item(cart_id)
        else:
            update_cart_quantity(cart_id, new_quantity)
            self.show_cart_screen()
    
    def remove_cart_item(self, cart_id):
        """Remove item from cart"""
        remove_from_cart(cart_id)
        self.show_cart_screen()
    
    def show_checkout_screen(self):
        """Show checkout form"""
        self.clear_window()
        self.current_screen = 'checkout'
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['success'], height=60)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="✅ Checkout",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['success'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        self.create_button(header, "Back to Cart", self.show_cart_screen, 
                          'secondary', 12).pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Main content - simple frame without canvas
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        # Content card
        card = self.create_card(main_frame)
        card.pack()
        
        tk.Label(
            card,
            text="Delivery Information",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(pady=20)
        
        # Get user info
        user_info = UserService.get_user_info(self.current_user[0])
        
        # Form
        form_frame = tk.Frame(card, bg=self.colors['card'])
        form_frame.pack(padx=40, pady=10)
        
        tk.Label(form_frame, text="Delivery Address", bg=self.colors['card'],
                fg=self.colors['text'], font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=10)
        address_text = tk.Text(form_frame, height=4, width=50, font=('Segoe UI', 10),
                              bg=self.colors['input_bg'], fg=self.colors['text'], insertbackground=self.colors['text'])
        address_text.grid(row=0, column=1, padx=10, pady=10)
        if user_info and user_info[6]:
            address_text.insert('1.0', user_info[6])
        
        tk.Label(form_frame, text="Phone Number", bg=self.colors['card'],
                fg=self.colors['text'], font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=10)
        phone_entry = tk.Entry(form_frame, width=50, font=('Segoe UI', 11),
                              bg=self.colors['input_bg'], fg=self.colors['text'], insertbackground=self.colors['text'])
        phone_entry.grid(row=1, column=1, padx=10, pady=10)
        if user_info and user_info[5]:
            phone_entry.insert(0, user_info[5])
        
        tk.Label(form_frame, text="Payment Method", bg=self.colors['card'],
                fg=self.colors['text'], font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=10)
        payment_var = tk.StringVar(value='cash')
        payment_frame = tk.Frame(form_frame, bg=self.colors['card'])
        payment_frame.grid(row=2, column=1, sticky='w', padx=10, pady=10)
        
        for method in ['cash', 'card', 'online']:
            tk.Radiobutton(
                payment_frame,
                text=method.title(),
                variable=payment_var,
                value=method,
                bg=self.colors['card'],
                fg=self.colors['text'],
                selectcolor=self.colors['input_bg'],
                font=('Segoe UI', 10)
            ).pack(side=tk.LEFT, padx=10)
        
        # Place order button
        def do_place_order():
            address = address_text.get('1.0', tk.END).strip()
            phone = phone_entry.get().strip()
            payment = payment_var.get()
            
            if not address or not phone:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            success, msg = OrderService.place_order(self.current_user[0], address, phone, payment)
            if success:
                messagebox.showinfo("Success", msg)
                self.show_customer_dashboard()
            else:
                messagebox.showerror("Error", msg)
        
        # Button frame
        button_frame = tk.Frame(card, bg=self.colors['card'])
        button_frame.pack(pady=30)
        
        # Create the button
        place_order_btn = self.create_button(
            button_frame,
            "Place Order",
            do_place_order,
            'success',
            25
        )
        place_order_btn.pack()
    
    def show_order_history(self):
        """Show customer order history"""
        self.clear_window()
        self.current_screen = 'orders'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['accent'], height=60)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="📦 My Orders",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['accent'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        self.create_button(header, "Back", self.show_customer_dashboard, 
                          'primary', 10).pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        orders = OrderService.get_user_orders(self.current_user[0])
        
        if not orders:
            tk.Label(
                main_frame,
                text="No orders yet!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['text_light']
            ).pack(pady=100)
            return
        
        # Orders list with scrollbar
        canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        orders_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        orders_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=orders_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Display orders
        for order in orders:
            order_id, order_number, total, discount, final_amount, payment, pay_status, order_status, address, order_date, delivered_at = order
            
            order_card = self.create_card(orders_frame)
            order_card.pack(fill=tk.X, pady=10, padx=10)
            
            # Order header
            header_frame = tk.Frame(order_card, bg=self.colors['card'])
            header_frame.pack(fill=tk.X, padx=15, pady=10)
            
            tk.Label(
                header_frame,
                text=f"Order #{order_number}",
                font=('Segoe UI', 14, 'bold'),
                bg=self.colors['card'],
                fg=self.colors['primary']
            ).pack(side=tk.LEFT)
            
            status_colors = {
                'pending': 'accent',
                'confirmed': 'secondary',
                'processing': 'secondary',
                'shipped': 'success',
                'delivered': 'success',
                'cancelled': 'danger'
            }
            
            tk.Label(
                header_frame,
                text=order_status.upper(),
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors.get(status_colors.get(order_status, 'secondary')),
                fg='white',
                padx=10,
                pady=5
            ).pack(side=tk.RIGHT)
            
            # Order details
            details_frame = tk.Frame(order_card, bg=self.colors['card'])
            details_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
            
            tk.Label(
                details_frame,
                text=f"Date: {order_date}",
                font=('Segoe UI', 10),
                bg=self.colors['card'],
                fg=self.colors['text_light']
            ).pack(anchor='w')
            
            tk.Label(
                details_frame,
                text=f"Amount: ₹{final_amount:.2f}",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['card'],
                fg=self.colors['primary']
            ).pack(anchor='w', pady=5)
    
    def show_notifications(self):
        """Show user notifications"""
        self.clear_window()
        self.current_screen = 'notifications'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['accent'], height=60)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="🔔 Notifications",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['accent'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        self.create_button(header, "Back", self.show_customer_dashboard, 
                          'primary', 10).pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        notifications = OrderService.get_user_notifications(self.current_user[0])
        
        if not notifications:
            tk.Label(
                main_frame,
                text="No notifications",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['text_light']
            ).pack(pady=100)
            return
        
        # Notifications list
        for notif in notifications:
            notif_id, notif_type, title, message, order_id, is_read, created_at = notif
            
            notif_card = self.create_card(main_frame)
            notif_card.pack(fill=tk.X, pady=5)
            
            bg_color = self.colors['card'] if is_read else '#e3f2fd'
            notif_card.config(bg=bg_color)
            
            frame = tk.Frame(notif_card, bg=bg_color)
            frame.pack(fill=tk.BOTH, padx=15, pady=10)
            
            tk.Label(
                frame,
                text=title,
                font=('Segoe UI', 12, 'bold'),
                bg=bg_color
            ).pack(anchor='w')
            
            tk.Label(
                frame,
                text=message,
                font=('Segoe UI', 10),
                bg=bg_color,
                fg=self.colors['text_light']
            ).pack(anchor='w', pady=5)
            
            tk.Label(
                frame,
                text=str(created_at),
                font=('Segoe UI', 9),
                bg=bg_color,
                fg=self.colors['text_light']
            ).pack(anchor='w')
            
            if not is_read:
                mark_notification_read(notif_id)
    
    def show_profile_screen(self):
        """Show user profile - editable details"""
        self.clear_window()
        self.current_screen = 'profile'
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Header with back button
        header = tk.Frame(self.root, bg='white', height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='white')
        header_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=15)
        
        # Back button
        back_btn = tk.Label(
            header_content,
            text="← Back to Dashboard",
            font=('Segoe UI', 12),
            bg='white',
            fg=self.colors['primary'],
            cursor='hand2'
        )
        back_btn.pack(side=tk.LEFT)
        back_btn.bind('<Button-1>', lambda e: self.show_customer_dashboard())
        
        # Title
        tk.Label(
            header_content,
            text="My Profile",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg=self.colors['text']
        ).pack(side=tk.LEFT, padx=20)
        
        # Logout button on right
        logout_btn = tk.Button(
            header_content,
            text="🚪 Logout",
            command=self.logout,
            bg='#E53935',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor='hand2',
            borderwidth=0
        )
        logout_btn.pack(side=tk.RIGHT)
        logout_btn.bind('<Enter>', lambda e: logout_btn.config(bg='#C62828'))
        logout_btn.bind('<Leave>', lambda e: logout_btn.config(bg='#E53935'))
        
        # Divider
        tk.Frame(self.root, bg=self.colors['border'], height=1).pack(fill=tk.X)
        
        # Main content area with scrollbar
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(content_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Profile form container
        form_container = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        form_container.pack(padx=60, pady=40, fill=tk.BOTH, expand=True)
        
        # Profile card
        profile_card = tk.Frame(form_container, bg='white', relief=tk.FLAT, borderwidth=0,
                               highlightthickness=1, highlightbackground=self.colors['border'])
        profile_card.pack(fill=tk.BOTH, expand=True)
        
        # Card content
        card_content = tk.Frame(profile_card, bg='white')
        card_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        tk.Label(
            card_content,
            text="Edit Your Profile",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 30))
        
        # Get current user info
        current_info = UserService.get_user_info(self.current_user[0])
        
        entries = {}
        
        # ===== SECTION 1: BASIC INFO =====
        tk.Label(
            card_content,
            text="Basic Information",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg=self.colors['primary']
        ).pack(anchor='w', pady=(0, 20))
        
        # Form fields - Basic Info
        basic_fields = [
            ("Username", current_info[1] if current_info else "", False),  # Read-only
            ("Email", current_info[3] if current_info else "", False),      # Read-only
            ("Full Name", current_info[4] if current_info else "", True),
            ("Phone Number", current_info[5] if current_info else "", True),
            ("Address", current_info[6] if current_info else "", True),
        ]
        
        for label, value, editable in basic_fields:
            # Label
            tk.Label(
                card_content,
                text=label,
                font=('Segoe UI', 11, 'bold'),
                bg='white',
                fg=self.colors['text']
            ).pack(anchor='w', pady=(10, 5))
            
            # Entry field
            entry = tk.Entry(
                card_content,
                font=('Segoe UI', 11),
                relief=tk.SOLID,
                borderwidth=1,
                bg='white' if editable else '#F5F5F5',
                fg=self.colors['text']
            )
            entry.pack(fill=tk.X, ipady=10, pady=(0, 5))
            entry.insert(0, value)
            entry.config(state=tk.NORMAL if editable else tk.DISABLED)
            
            if label not in ["Username", "Email"]:
                entries[label] = entry
        
        # Divider
        tk.Frame(card_content, bg=self.colors['border'], height=1).pack(fill=tk.X, pady=25)
        
        # ===== SECTION 2: CHANGE USERNAME =====
        tk.Label(
            card_content,
            text="Change Username",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg=self.colors['primary']
        ).pack(anchor='w', pady=(0, 20))
        
        # New Username
        tk.Label(
            card_content,
            text="New Username",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['text']
        ).pack(anchor='w', pady=(10, 5))
        
        new_username_entry = tk.Entry(
            card_content,
            font=('Segoe UI', 11),
            relief=tk.SOLID,
            borderwidth=1,
            bg='white',
            fg=self.colors['text']
        )
        new_username_entry.pack(fill=tk.X, ipady=10, pady=(0, 5))
        entries['new_username'] = new_username_entry
        
        # Divider
        tk.Frame(card_content, bg=self.colors['border'], height=1).pack(fill=tk.X, pady=25)
        
        # ===== SECTION 3: CHANGE PASSWORD =====
        tk.Label(
            card_content,
            text="Change Password",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg=self.colors['primary']
        ).pack(anchor='w', pady=(0, 20))
        
        # Current Password
        tk.Label(
            card_content,
            text="Current Password",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['text']
        ).pack(anchor='w', pady=(10, 5))
        
        current_password_entry = tk.Entry(
            card_content,
            font=('Segoe UI', 11),
            relief=tk.SOLID,
            borderwidth=1,
            bg='white',
            fg=self.colors['text'],
            show='●'
        )
        current_password_entry.pack(fill=tk.X, ipady=10, pady=(0, 5))
        entries['current_password'] = current_password_entry
        
        # New Password
        tk.Label(
            card_content,
            text="New Password",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['text']
        ).pack(anchor='w', pady=(10, 5))
        
        new_password_entry = tk.Entry(
            card_content,
            font=('Segoe UI', 11),
            relief=tk.SOLID,
            borderwidth=1,
            bg='white',
            fg=self.colors['text'],
            show='●'
        )
        new_password_entry.pack(fill=tk.X, ipady=10, pady=(0, 5))
        entries['new_password'] = new_password_entry
        
        # Confirm Password
        tk.Label(
            card_content,
            text="Confirm New Password",
            font=('Segoe UI', 11, 'bold'),
            bg='white',
            fg=self.colors['text']
        ).pack(anchor='w', pady=(10, 5))
        
        confirm_password_entry = tk.Entry(
            card_content,
            font=('Segoe UI', 11),
            relief=tk.SOLID,
            borderwidth=1,
            bg='white',
            fg=self.colors['text'],
            show='●'
        )
        confirm_password_entry.pack(fill=tk.X, ipady=10, pady=(0, 5))
        entries['confirm_password'] = confirm_password_entry
        
        # Button container
        button_frame = tk.Frame(card_content, bg='white')
        button_frame.pack(fill=tk.X, pady=(30, 0))
        
        def save_profile():
            try:
                full_name = entries["Full Name"].get()
                phone = entries["Phone Number"].get()
                address = entries["Address"].get()
                new_username = entries['new_username'].get()
                current_password = entries['current_password'].get()
                new_password = entries['new_password'].get()
                confirm_password = entries['confirm_password'].get()
                
                # Validate basic info
                if not full_name or not phone or not address:
                    messagebox.showwarning("Validation", "Please fill all basic information fields")
                    return
                
                # Update basic profile info
                UserService.update_user_profile(self.current_user[0], full_name, phone, address)
                
                # Update username if provided
                if new_username and new_username.strip():
                    success, msg = UserService.update_username(self.current_user[0], new_username)
                    if not success:
                        messagebox.showwarning("Username Error", msg)
                        return
                    # Update current_user with new username
                    self.current_user = list(self.current_user)
                    self.current_user[1] = new_username
                
                # Update password if provided
                if current_password and new_password:
                    if new_password != confirm_password:
                        messagebox.showwarning("Password Error", "New passwords do not match")
                        return
                    
                    if len(new_password) < 6:
                        messagebox.showwarning("Password Error", "Password must be at least 6 characters")
                        return
                    
                    success, msg = change_password('customer', self.current_user[0], current_password, new_password)
                    if not success:
                        messagebox.showwarning("Password Error", msg)
                        return
                
                messagebox.showinfo("Success", "✓ Profile updated successfully!")
                self.show_customer_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profile: {str(e)}")
        
        # Save button
        save_btn = tk.Button(
            button_frame,
            text="💾 Save Changes",
            command=save_profile,
            bg=self.colors['primary'],
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            padx=40,
            pady=12,
            cursor='hand2',
            borderwidth=0
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 15))
        save_btn.bind('<Enter>', lambda e: save_btn.config(bg=self.darken_color(self.colors['primary'])))
        save_btn.bind('<Leave>', lambda e: save_btn.config(bg=self.colors['primary']))
        
        # Cancel button
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.show_customer_dashboard,
            bg='#E0E0E0',
            fg=self.colors['text'],
            font=('Segoe UI', 12, 'bold'),
            relief=tk.FLAT,
            padx=40,
            pady=12,
            cursor='hand2',
            borderwidth=0
        )
        cancel_btn.pack(side=tk.LEFT)
        cancel_btn.bind('<Enter>', lambda e: cancel_btn.config(bg='#D0D0D0'))
        cancel_btn.bind('<Leave>', lambda e: cancel_btn.config(bg='#E0E0E0'))
    
    # ==================== ADMIN DASHBOARD ====================
    
    def show_admin_dashboard(self):
        """Show admin dashboard"""
        self.clear_window()
        self.current_screen = 'admin_dashboard'
        
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        header.pack(fill=tk.X)
        
        # Header content
        header_left = tk.Frame(header, bg=self.colors['primary'])
        header_left.pack(side=tk.LEFT, padx=30, pady=25)
        
        tk.Label(
            header_left,
            text="👨‍💼 Admin Panel",
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(anchor=tk.W)
        
        tk.Label(
            header_left,
            text=f"Welcome, {self.current_staff[4]}",
            font=('Segoe UI', 11),
            bg=self.colors['primary'],
            fg='#E0E0E0'
        ).pack(anchor=tk.W, pady=(5, 0))
        
        self.create_button(header, "🚪 Logout", self.logout, 'danger', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Quick stats section
        stats_label = tk.Label(
            main_frame,
            text="📊 Quick Stats",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        stats_label.pack(anchor=tk.W, pady=(0, 15))
        
        # Stats cards - simplified
        stats_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        stats_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Get statistics
        inv_stats = InventoryService.get_inventory_stats()
        
        stats = [
            ("🔢\nTotal Items", self.show_items_by_category, self.colors['secondary']),
            ("⚠️\nExpiring Soon", self.show_expiring_soon_screen, self.colors['accent']),
            ("❌\nExpired", self.show_expired_items_screen, self.colors['danger']),
        ]
        
        for title, command, color in stats:
            card = self.create_card(stats_frame, width=200, height=140)
            card.pack(side=tk.LEFT, padx=15)
            card.pack_propagate(False)
            card.config(cursor='hand2')
            card.config(bg=color)
            
            # Bind click
            card.bind('<Button-1>', lambda e, cmd=command: cmd())
            
            # Title label
            title_label = tk.Label(
                card,
                text=title,
                font=('Segoe UI', 13, 'bold'),
                bg=color,
                fg='white',
                cursor='hand2'
            )
            title_label.pack(pady=20)
            title_label.bind('<Button-1>', lambda e, cmd=command: cmd())
            
            # Bind click events to all child widgets
            for widget in card.winfo_children():
                widget.bind('<Button-1>', lambda e, cmd=command: cmd())
        
        # Main menu section
        menu_label = tk.Label(
            main_frame,
            text="🎯 Main Menu",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        menu_label.pack(anchor=tk.W, pady=(20, 15))
        
        # Menu options in grid layout
        menu_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        menu_frame.pack(fill=tk.BOTH, expand=True)
        
        menus = [
            ("📝\nAdd Product", self.show_add_product_screen, self.colors['success']),
            ("📋\nManage Products", self.show_manage_products_screen, self.colors['primary']),
            ("📊\nInventory", self.show_inventory_screen, self.colors['secondary']),
            ("📦\nView Orders", self.show_admin_orders_screen, self.colors['accent']),
        ]
        
        # Create 2x2 grid
        for i, (title, command, color) in enumerate(menus):
            # Create row frame if needed
            if i % 2 == 0:
                row_frame = tk.Frame(menu_frame, bg=self.colors['bg'])
                row_frame.pack(fill=tk.X, pady=10)
            
            # Create menu card
            card = self.create_card(row_frame, width=280, height=120)
            card.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.BOTH)
            card.pack_propagate(False)
            card.config(cursor='hand2')
            
            # Card background with color
            card_inner = tk.Frame(card, bg=color)
            card_inner.pack(fill=tk.BOTH, expand=True)
            
            # Title with emoji on multiple lines
            title_label = tk.Label(
                card_inner,
                text=title,
                font=('Segoe UI', 12, 'bold'),
                bg=color,
                fg='white',
                justify=tk.CENTER,
                cursor='hand2'
            )
            title_label.pack(expand=True, pady=10)
            title_label.bind('<Button-1>', lambda e, cmd=command: cmd())
            
            # Bind card click
            card.bind('<Button-1>', lambda e, cmd=command: cmd())
            card_inner.bind('<Button-1>', lambda e, cmd=command: cmd())
            for widget in card_inner.winfo_children():
                widget.bind('<Button-1>', lambda e, cmd=command: cmd())
    
    def show_add_product_screen(self):
        """Show add product screen with image upload"""
        self.clear_window()
        self.current_screen = 'add_product'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['success'], height=60)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="📝 Add New Product",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['success'],
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        self.create_button(header, "Back", self.show_admin_dashboard, 
                          'primary', 10).pack(side=tk.RIGHT, padx=20, pady=15)
        
        # Main content with scrollbar
        canvas = tk.Canvas(self.root, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        main_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        main_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=main_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        card = self.create_card(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
        
        # Image upload section
        image_frame = tk.Frame(card, bg=self.colors['card'])
        image_frame.pack(pady=20)
        
        image_label = tk.Label(
            image_frame,
            text="📸\nNo Image",
            font=('Segoe UI', 14),
            bg='#E5E7EB',
            fg='#6B7280',
            width=20,
            height=10
        )
        image_label.pack()
        
        selected_image_path = {"path": None}
        selected_image_label = tk.Label(image_frame, text="", bg=self.colors['card'], 
                                       font=('Segoe UI', 9), fg=self.colors['success'])
        
        def select_image():
            path = ImageService.browse_image()
            print(f"\n{'='*80}")
            print(f"SELECT IMAGE DEBUG:")
            print(f"  browse_image() returned: '{path}'")
            print(f"  Type: {type(path)}")
            print(f"  Is None: {path is None}")
            print(f"  Is empty: {path == ''}")
            print(f"  Bool value: {bool(path)}")
            
            if path and path.strip():  # Check for non-empty string
                import os
                print(f"  File exists: {os.path.exists(path)}")
                selected_image_path["path"] = path
                print(f"  ✓ Stored in dict: {selected_image_path['path']}")
                
                try:
                    img = ImageService.load_image_for_display(path, (200, 200))
                    self.image_cache['new_product'] = img
                    image_label.config(image=img, text="")
                    selected_image_label.config(text=f"✓ Image selected: {os.path.basename(path)}")
                    print(f"  ✓ Image loaded and displayed")
                except Exception as e:
                    print(f"  ✗ Error loading image: {e}")
                    messagebox.showerror("Error", f"Failed to load image: {e}")
            else:
                print(f"  ✗ No valid path (user cancelled or error)")
                selected_image_label.config(text="")
            print("="*80 + "\n")
        
        self.create_button(image_frame, "📷 Select Image", select_image, 
                          'secondary', 15).pack(pady=10)
        selected_image_label.pack(pady=5)
        
        # Form
        form_frame = tk.Frame(card, bg=self.colors['card'])
        form_frame.pack(padx=40, pady=10)
        
        fields = {}
        
        # Product Name
        tk.Label(form_frame, text="Product Name *", bg=self.colors['card'], fg=self.colors['text'],
                font=('Segoe UI', 11, 'bold')).grid(row=0, column=0, sticky='w', pady=10)
        fields['name'] = self.create_entry(form_frame, width=50)
        fields['name'].grid(row=0, column=1, padx=10, pady=10)
        
        # Category
        tk.Label(form_frame, text="Category *", bg=self.colors['card'], fg=self.colors['text'],
                font=('Segoe UI', 11, 'bold')).grid(row=1, column=0, sticky='w', pady=10)
        categories = ProductService.get_all_categories()
        category_var = tk.StringVar()
        category_dropdown = ttk.Combobox(
            form_frame,
            textvariable=category_var,
            values=[f"{c[1]}" for c in categories],
            state='readonly',
            width=47,
            font=('Segoe UI', 11)
        )
        category_dropdown.grid(row=1, column=1, padx=10, pady=10)
        if categories:
            category_dropdown.set(categories[0][1])
        
        # Description
        tk.Label(form_frame, text="Description", bg=self.colors['card'], fg=self.colors['text'],
                font=('Segoe UI', 11, 'bold')).grid(row=2, column=0, sticky='w', pady=10)
        fields['description'] = tk.Text(form_frame, height=4, width=50, 
                                       font=('Segoe UI', 10),
                                       bg=self.colors['input_bg'], fg=self.colors['text'],
                                       insertbackground=self.colors['text'])
        fields['description'].grid(row=2, column=1, padx=10, pady=10)
        
        # Unit Price
        tk.Label(form_frame, text="Unit Price (₹) *", bg=self.colors['card'], fg=self.colors['text'],
                font=('Segoe UI', 11, 'bold')).grid(row=3, column=0, sticky='w', pady=10)
        fields['price'] = self.create_entry(form_frame, width=50)
        fields['price'].grid(row=3, column=1, padx=10, pady=10)
        
        # Unit
        tk.Label(form_frame, text="Unit *", bg=self.colors['card'], fg=self.colors['text'],
                font=('Segoe UI', 11, 'bold')).grid(row=4, column=0, sticky='w', pady=10)
        unit_var = tk.StringVar(value='unit')
        unit_frame = tk.Frame(form_frame, bg=self.colors['card'])
        unit_frame.grid(row=4, column=1, sticky='w', padx=10, pady=10)
        for unit in ['unit', 'kg', 'liter', 'pack', 'dozen']:
            tk.Radiobutton(
                unit_frame,
                text=unit.title(),
                variable=unit_var,
                value=unit,
                bg=self.colors['card'],
                fg=self.colors['text'],
                selectcolor=self.colors['input_bg'],
                activebackground=self.colors['card'],
                activeforeground=self.colors['text'],
                font=('Segoe UI', 10)
            ).pack(side=tk.LEFT, padx=10)
        
        # Stock Quantity
        tk.Label(form_frame, text="Stock Quantity *", bg=self.colors['card'], fg=self.colors['text'],
                font=('Segoe UI', 11, 'bold')).grid(row=5, column=0, sticky='w', pady=10)
        fields['stock'] = self.create_entry(form_frame, width=50)
        fields['stock'].grid(row=5, column=1, padx=10, pady=10)
        
        # Min Stock Level
        tk.Label(form_frame, text="Min Stock Level", bg=self.colors['card'], fg=self.colors['text'],
                font=('Segoe UI', 11, 'bold')).grid(row=6, column=0, sticky='w', pady=10)
        fields['min_stock'] = self.create_entry(form_frame, width=50)
        fields['min_stock'].insert(0, '5')
        fields['min_stock'].grid(row=6, column=1, padx=10, pady=10)
        
        # Manufactured Date
        tk.Label(form_frame, text="Manufactured Date", bg=self.colors['card'], fg=self.colors['text'],
                font=('Segoe UI', 11, 'bold')).grid(row=7, column=0, sticky='w', pady=10)
        
        manufactured_date_frame = tk.Frame(form_frame, bg=self.colors['card'])
        manufactured_date_frame.grid(row=7, column=1, padx=10, pady=10, sticky='w')
        
        fields['manufactured_date'] = self.create_entry(manufactured_date_frame, width=35)
        fields['manufactured_date'].pack(side=tk.LEFT, padx=(0, 5))
        
        def open_manufactured_calendar():
            self.open_calendar_picker(fields['manufactured_date'])
        
        tk.Button(
            manufactured_date_frame,
            text="📅 Pick Date",
            command=open_manufactured_calendar,
            bg=self.colors['secondary'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT)
        
        # Expiry Date
        tk.Label(form_frame, text="Expiry Date (Required)", bg=self.colors['card'], fg=self.colors['text'],
                font=('Segoe UI', 11, 'bold')).grid(row=8, column=0, sticky='w', pady=10)
        
        expiry_date_frame = tk.Frame(form_frame, bg=self.colors['card'])
        expiry_date_frame.grid(row=8, column=1, padx=10, pady=10, sticky='w')
        
        fields['expiry_date'] = self.create_entry(expiry_date_frame, width=35)
        fields['expiry_date'].pack(side=tk.LEFT, padx=(0, 5))
        
        def open_expiry_calendar():
            self.open_calendar_picker(fields['expiry_date'])
        
        tk.Button(
            expiry_date_frame,
            text="📅 Pick Date",
            command=open_expiry_calendar,
            bg=self.colors['danger'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT)
        
        # Submit button
        def submit_product():
            try:
                name = fields['name'].get().strip()
                category_name = category_var.get()
                description = fields['description'].get('1.0', tk.END).strip()
                price = float(fields['price'].get())
                unit = unit_var.get()
                stock = int(fields['stock'].get())
                min_stock = int(fields['min_stock'].get())
                manufactured_date = fields['manufactured_date'].get().strip() or None
                expiry_date = fields['expiry_date'].get().strip()
                
                if not all([name, category_name, price, stock, expiry_date]):
                    messagebox.showerror("Error", "Please fill in all required fields marked with *")
                    return
                
                # Validate date format
                from datetime import datetime
                try:
                    if manufactured_date:
                        datetime.strptime(manufactured_date, '%Y-%m-%d')
                    datetime.strptime(expiry_date, '%Y-%m-%d')
                except ValueError:
                    messagebox.showerror("Error", "Please use YYYY-MM-DD format for dates")
                    return
                
                # Get category ID
                category_id = next((c[0] for c in categories if c[1] == category_name), None)
                if not category_id:
                    messagebox.showerror("Error", "Invalid category")
                    return
                
                # Save image
                image_filename = None
                if selected_image_path["path"]:
                    print(f"DEBUG submit: Saving image from: {selected_image_path['path']}")
                    image_filename = ImageService.save_product_image(selected_image_path["path"], name)
                    print(f"DEBUG submit: Image filename returned: {image_filename}")
                    if image_filename is None:
                        print("ERROR: save_product_image returned None!")
                else:
                    print("DEBUG submit: No image selected (path is None)")
                
                # Add product with dates
                print(f"DEBUG submit: Calling add_product with:")
                print(f"  name={name}")
                print(f"  category_id={category_id}")
                print(f"  description={description[:50]}...")
                print(f"  image_path={image_filename}")
                print(f"  unit_price={price}")
                print(f"  unit={unit}")
                print(f"  stock_quantity={stock}")
                print(f"  min_stock_level={min_stock}")
                print(f"  manufactured_date={manufactured_date}")
                print(f"  expiry_date={expiry_date}")
                
                product_id = ProductService.add_product(name, category_id, description, image_filename,
                                        price, unit, stock, min_stock)
                
                # Update with dates
                if product_id:
                    db = connect_db()
                    cursor = db.cursor()
                    update_query = "UPDATE products SET manufactured_date = %s, expiry_date = %s WHERE product_id = %s"
                    cursor.execute(update_query, (manufactured_date, expiry_date, product_id))
                    db.commit()
                    db.close()
                
                print(f"DEBUG submit: Product added with ID: {product_id}")
                
                messagebox.showinfo("Success", f"Product added successfully! ID: {product_id}")
                self.show_admin_dashboard()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price and stock")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add product: {str(e)}")
        
        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(pady=20)
        
        self.create_button(btn_frame, "Add Product", submit_product, 
                          'success', 20).pack(pady=5)
        self.create_button(btn_frame, "Cancel", self.show_admin_dashboard, 
                          'danger', 20).pack(pady=5)
    
    def show_manage_products_screen(self):
        """Show manage products screen - category selection"""
        self.clear_window()
        self.current_screen = 'manage_products'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="📋 Manage Products",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=25)
        
        self.create_button(header, "← Back", self.show_admin_dashboard, 'secondary', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get categories with count
        categories = ProductService.get_categories_with_count()
        
        if not categories:
            tk.Label(
                main_frame,
                text="✅ No categories available!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['success']
            ).pack(pady=50)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Display categories
            for cat_id, cat_name, item_count in categories:
                card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT, bd=1)
                card.pack(fill=tk.X, pady=8, padx=10)
                card.config(cursor='hand2')
                
                # Bind click
                card.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_manage_category_products(cid, cname))
                
                # Category info frame
                info_frame = tk.Frame(card, bg=self.colors['card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)
                
                # Category name
                cat_label = tk.Label(
                    info_frame,
                    text=f"📁 {cat_name}",
                    font=('Segoe UI', 13, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['primary'],
                    cursor='hand2'
                )
                cat_label.pack(anchor=tk.W)
                cat_label.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_manage_category_products(cid, cname))
                
                # Item count
                count_label = tk.Label(
                    info_frame,
                    text=f"{item_count} item{'s' if item_count != 1 else ''}",
                    font=('Segoe UI', 10),
                    bg=self.colors['card'],
                    fg=self.colors['text_light'],
                    cursor='hand2'
                )
                count_label.pack(anchor=tk.W, pady=(3, 0))
                count_label.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_manage_category_products(cid, cname))
                
                # Arrow
                arrow_frame = tk.Frame(card, bg=self.colors['card'])
                arrow_frame.pack(side=tk.RIGHT, padx=20)
                
                arrow_label = tk.Label(
                    arrow_frame,
                    text="✏️",
                    font=('Segoe UI', 16),
                    bg=self.colors['card'],
                    fg=self.colors['primary'],
                    cursor='hand2'
                )
                arrow_label.pack()
                arrow_label.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_manage_category_products(cid, cname))
    
    def show_manage_category_products(self, category_id, category_name):
        """Show products in selected category for editing"""
        self.clear_window()
        self.current_screen = 'manage_category_products'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=f"✏️ Manage {category_name}",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=25)
        
        self.create_button(header, "← Back", self.show_manage_products_screen, 'secondary', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get products in category
        products = ProductService.get_products_in_category(category_id)
        
        if not products:
            tk.Label(
                main_frame,
                text=f"✅ No products in {category_name}!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['success']
            ).pack(pady=50)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Display products
            for product_id, name, stock, price, unit, expiry_date in products:
                card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT, bd=1)
                card.pack(fill=tk.X, pady=8, padx=10)
                
                # Product info
                info_frame = tk.Frame(card, bg=self.colors['card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=12)
                
                # Product name
                tk.Label(
                    info_frame,
                    text=f"📦 {name}",
                    font=('Segoe UI', 11, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['text']
                ).pack(anchor=tk.W)
                
                # Product details
                expiry_text = f"Expires: {expiry_date}" if expiry_date else "No expiry"
                details_text = f"Stock: {stock} {unit} | Price: ₹{price} | {expiry_text}"
                
                tk.Label(
                    info_frame,
                    text=details_text,
                    font=('Segoe UI', 9),
                    bg=self.colors['card'],
                    fg=self.colors['text_light']
                ).pack(anchor=tk.W, pady=(3, 0))
                
                # Action button
                btn_frame = tk.Frame(card, bg=self.colors['card'])
                btn_frame.pack(side=tk.RIGHT, padx=15, pady=12)
                
                tk.Button(
                    btn_frame,
                    text="✏️ Edit",
                    command=lambda pid=product_id, pname=name, pstock=stock, pprice=price, punit=unit, pexp=expiry_date, cid=category_id: self.show_edit_product_screen(pid, pname, pstock, pprice, punit, pexp, cid, category_name),
                    bg=self.colors['primary'],
                    fg='white',
                    font=('Segoe UI', 9, 'bold'),
                    relief=tk.FLAT,
                    padx=10,
                    pady=8,
                    cursor='hand2'
                ).pack(side=tk.LEFT, padx=5)
                
                tk.Button(
                    btn_frame,
                    text="🗑️ Delete",
                    command=lambda pid=product_id, pname=name, cid=category_id, cname=category_name: self.delete_product(pid, pname, cid, cname),
                    bg=self.colors['danger'],
                    fg='white',
                    font=('Segoe UI', 9, 'bold'),
                    relief=tk.FLAT,
                    padx=10,
                    pady=8,
                    cursor='hand2'
                ).pack(side=tk.LEFT, padx=5)
    
    def show_edit_product_screen(self, product_id, product_name, stock, price, unit, expiry_date, category_id, category_name):
        """Show edit product form"""
        self.clear_window()
        self.current_screen = 'edit_product'
        
        # Get full product details from database
        product_data = ProductService.get_product_by_id_full(product_id)
        if product_data:
            _, _, db_price, db_stock, db_unit, manufactured_date, db_expiry_date = product_data
        else:
            manufactured_date = ""
            db_expiry_date = expiry_date
        
        # Header with back button
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Back button
        back_btn = tk.Button(
            header,
            text="← Back",
            command=lambda: self.show_manage_category_products(category_id, category_name),
            bg=self.colors['primary_dark'],
            fg='white',
            font=('Segoe UI', 10, 'bold'),
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        back_btn.pack(side=tk.LEFT, padx=15, pady=15)
        
        title_label = tk.Label(
            header,
            text=f"✏️ Edit Product",
            font=('Segoe UI', 24, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            header,
            text=f"Category: {category_name} | Product: {product_name}",
            font=('Segoe UI', 10),
            fg=self.colors['text_light'],
            bg=self.colors['primary']
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Main container with scroll
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create canvas for scrolling
        canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields
        form_data = {}
        
        # Product Name
        tk.Label(
            scrollable_frame,
            text="Product Name",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=(10, 5), anchor='w')
        
        product_name_entry = tk.Entry(
            scrollable_frame,
            font=('Segoe UI', 11),
            width=40,
            relief=tk.FLAT,
            bg='white',
            fg=self.colors['text']
        )
        product_name_entry.insert(0, product_name)
        product_name_entry.pack(pady=(0, 15), fill=tk.X)
        form_data['name'] = product_name_entry
        
        # Unit Price
        tk.Label(
            scrollable_frame,
            text="Unit Price (₹)",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=(10, 5), anchor='w')
        
        price_entry = tk.Entry(
            scrollable_frame,
            font=('Segoe UI', 11),
            width=40,
            relief=tk.FLAT,
            bg='white',
            fg=self.colors['text']
        )
        price_entry.insert(0, str(price))
        price_entry.pack(pady=(0, 15), fill=tk.X)
        form_data['price'] = price_entry
        
        # Stock Quantity
        tk.Label(
            scrollable_frame,
            text="Stock Quantity",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=(10, 5), anchor='w')
        
        stock_entry = tk.Entry(
            scrollable_frame,
            font=('Segoe UI', 11),
            width=40,
            relief=tk.FLAT,
            bg='white',
            fg=self.colors['text']
        )
        stock_entry.insert(0, str(stock))
        stock_entry.pack(pady=(0, 15), fill=tk.X)
        form_data['stock'] = stock_entry
        
        # Unit (Dropdown)
        tk.Label(
            scrollable_frame,
            text="Unit",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=(10, 5), anchor='w')
        
        unit_var = tk.StringVar(value=unit)
        unit_dropdown = tk.OptionMenu(
            scrollable_frame,
            unit_var,
            "unit", "kg", "liter", "pack", "dozen"
        )
        unit_dropdown.config(
            font=('Segoe UI', 11),
            bg='white',
            fg=self.colors['text'],
            relief=tk.FLAT,
            highlightthickness=0,
            width=37
        )
        unit_dropdown.pack(pady=(0, 15), fill=tk.X)
        form_data['unit'] = unit_var
        
        # Manufactured Date (READ-ONLY) - Display section
        tk.Label(
            scrollable_frame,
            text="📅 Manufactured Date (Read-Only)",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=(15, 8), anchor='w')
        
        manu_date_display_frame = tk.Frame(scrollable_frame, bg=self.colors['input_bg'], relief=tk.FLAT)
        manu_date_display_frame.pack(pady=(0, 15), fill=tk.X, ipady=10, ipadx=10)
        
        manu_display = str(manufactured_date) if manufactured_date else "Not set"
        tk.Label(
            manu_date_display_frame,
            text=manu_display,
            font=('Segoe UI', 11),
            bg=self.colors['input_bg'],
            fg=self.colors['text_light']
        ).pack(anchor='w')
        form_data['manu_date'] = manufactured_date
        
        # Current/Old Expiry Date (READ-ONLY) - Display section
        tk.Label(
            scrollable_frame,
            text="📅 Current Expiry Date (Read-Only)",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=(15, 8), anchor='w')
        
        old_exp_date_display_frame = tk.Frame(scrollable_frame, bg=self.colors['input_bg'], relief=tk.FLAT)
        old_exp_date_display_frame.pack(pady=(0, 15), fill=tk.X, ipady=10, ipadx=10)
        
        old_exp_display = str(db_expiry_date) if db_expiry_date else "Not set"
        tk.Label(
            old_exp_date_display_frame,
            text=old_exp_display,
            font=('Segoe UI', 11),
            bg=self.colors['input_bg'],
            fg=self.colors['text_light']
        ).pack(anchor='w')
        
        # New Expiry Date (EDITABLE)
        tk.Label(
            scrollable_frame,
            text="📅 Set New Expiry Date",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(pady=(15, 8), anchor='w')
        
        exp_date_var = tk.StringVar(value="")
        exp_date_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        exp_date_frame.pack(pady=(0, 20), fill=tk.X)
        
        exp_date_entry = tk.Entry(
            exp_date_frame,
            textvariable=exp_date_var,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bg='white',
            fg=self.colors['text'],
            width=32,
            state=tk.DISABLED
        )
        exp_date_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(
            exp_date_frame,
            text="📅",
            command=lambda: self.open_calendar_picker(exp_date_entry),
            bg=self.colors['primary'],
            fg='white',
            relief=tk.FLAT,
            padx=12,
            pady=8,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=(5, 0))
        form_data['exp_date'] = exp_date_var
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        def save_product():
            try:
                from datetime import datetime
                
                new_name = form_data['name'].get().strip()
                new_price = float(form_data['price'].get().strip())
                new_stock = int(form_data['stock'].get().strip())
                new_unit = form_data['unit'].get()
                new_exp_date = form_data['exp_date'].get() or None
                
                if not new_name:
                    messagebox.showerror("Error", "Product name cannot be empty!")
                    return
                
                if new_price <= 0:
                    messagebox.showerror("Error", "Price must be greater than 0!")
                    return
                
                if new_stock < 0:
                    messagebox.showerror("Error", "Stock cannot be negative!")
                    return
                
                # Validate expiry date vs manufactured date
                if new_exp_date and manufactured_date:
                    try:
                        new_exp_date_obj = datetime.strptime(new_exp_date, '%Y-%m-%d').date()
                        manu_date_obj = datetime.strptime(str(manufactured_date), '%Y-%m-%d').date()
                        
                        if new_exp_date_obj < manu_date_obj:
                            messagebox.showerror(
                                "Error",
                                f"Expiry date ({new_exp_date}) cannot be before\nmanufactured date ({manufactured_date})!"
                            )
                            return
                    except ValueError:
                        pass  # If date parsing fails, let database handle validation
                
                # Update product (manufactured date stays unchanged)
                success, msg = ProductService.update_product(product_id, new_name, new_price, new_stock, new_unit, new_exp_date, None)
                if success:
                    messagebox.showinfo("Success", f"Product '{new_name}' updated successfully!")
                    self.show_manage_category_products(category_id, category_name)
                else:
                    messagebox.showerror("Error", "Failed to update product!")
            except ValueError as e:
                messagebox.showerror("Error", "Please enter valid values!")
        
        tk.Button(
            button_frame,
            text="💾 Save Changes",
            command=save_product,
            bg=self.colors['success'],
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="❌ Cancel",
            command=lambda: self.show_manage_category_products(category_id, category_name),
            bg=self.colors['text_muted'],
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)
    
    def delete_product(self, product_id, product_name, category_id, category_name):
        """Delete a product with confirmation"""
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{product_name}'?\n\nThis action cannot be undone."
        )
        
        if result:
            success, msg = ProductService.delete_product(product_id)
            if success:
                messagebox.showinfo("Success", f"Product '{product_name}' has been deleted!")
                # Refresh the current category's products
                self.show_manage_category_products(category_id, category_name)
            else:
                messagebox.showerror("Error", "Failed to delete product!")
    
    def show_inventory_screen(self):
        """Show inventory management screen - category selection"""
        self.clear_window()
        self.current_screen = 'inventory'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['secondary'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="📊 Inventory Management",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['secondary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=25)
        
        self.create_button(header, "← Back", self.show_admin_dashboard, 'primary', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get categories with count
        categories = ProductService.get_categories_with_count()
        
        if not categories:
            tk.Label(
                main_frame,
                text="✅ No categories available!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['success']
            ).pack(pady=50)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Display categories
            for cat_id, cat_name, item_count in categories:
                card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT, bd=1)
                card.pack(fill=tk.X, pady=8, padx=10)
                card.config(cursor='hand2')
                
                # Bind click
                card.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_inventory_category_products(cid, cname))
                
                # Category info frame
                info_frame = tk.Frame(card, bg=self.colors['card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)
                
                # Category name
                cat_label = tk.Label(
                    info_frame,
                    text=f"📁 {cat_name}",
                    font=('Segoe UI', 13, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['secondary'],
                    cursor='hand2'
                )
                cat_label.pack(anchor=tk.W)
                cat_label.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_inventory_category_products(cid, cname))
                
                # Item count
                count_label = tk.Label(
                    info_frame,
                    text=f"{item_count} item{'s' if item_count != 1 else ''}",
                    font=('Segoe UI', 10),
                    bg=self.colors['card'],
                    fg=self.colors['text_light'],
                    cursor='hand2'
                )
                count_label.pack(anchor=tk.W, pady=(3, 0))
                count_label.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_inventory_category_products(cid, cname))
                
                # Arrow
                arrow_frame = tk.Frame(card, bg=self.colors['card'])
                arrow_frame.pack(side=tk.RIGHT, padx=20)
                
                arrow_label = tk.Label(
                    arrow_frame,
                    text="→",
                    font=('Segoe UI', 16),
                    bg=self.colors['card'],
                    fg=self.colors['secondary'],
                    cursor='hand2'
                )
                arrow_label.pack()
                arrow_label.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_inventory_category_products(cid, cname))
    
    def show_inventory_category_products(self, category_id, category_name):
        """Show inventory items in selected category"""
        self.clear_window()
        self.current_screen = 'inventory_category'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['secondary'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=f"📦 {category_name} Inventory",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['secondary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=25)
        
        self.create_button(header, "← Back", self.show_inventory_screen, 'primary', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get products in category
        products = ProductService.get_products_in_category(category_id)
        
        if not products:
            tk.Label(
                main_frame,
                text=f"✅ No products in {category_name}!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['success']
            ).pack(pady=50)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Display products
            for product_id, name, stock, price, unit, expiry_date in products:
                card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT, bd=1)
                card.pack(fill=tk.X, pady=8, padx=10)
                
                # Product info
                info_frame = tk.Frame(card, bg=self.colors['card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=12)
                
                # Product name
                tk.Label(
                    info_frame,
                    text=f"📦 {name}",
                    font=('Segoe UI', 11, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['text']
                ).pack(anchor=tk.W)
                
                # Product details with stock highlight
                stock_color = self.colors['danger'] if stock < 10 else self.colors['success']
                expiry_text = f"Expires: {expiry_date}" if expiry_date else "No expiry"
                details_text = f"Stock: {stock} {unit} | Price: ₹{price} | {expiry_text}"
                
                tk.Label(
                    info_frame,
                    text=details_text,
                    font=('Segoe UI', 9),
                    bg=self.colors['card'],
                    fg=stock_color if stock < 10 else self.colors['text_light']
                ).pack(anchor=tk.W, pady=(3, 0))
    
    def show_admin_orders_screen(self):
        """Show all orders for admin"""
        self.clear_window()
        self.current_screen = 'admin_orders'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['accent'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="📦 Customer Orders",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['accent'],
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=25)
        
        self.create_button(header, "← Back", self.show_admin_dashboard, 'primary', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get all orders
        orders = OrderService.get_all_admin_orders()
        
        if not orders:
            tk.Label(
                main_frame,
                text="✅ No orders yet!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['success']
            ).pack(pady=50)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Display orders
            for order_id, user_id, customer_name, phone, order_date, total_amount, delivery_address, item_count in orders:
                card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT, bd=1)
                card.pack(fill=tk.X, pady=8, padx=10)
                card.config(cursor='hand2')
                
                # Bind click
                card.bind('<Button-1>', lambda e, oid=order_id: self.show_order_details_screen(oid))
                
                # Order info
                info_frame = tk.Frame(card, bg=self.colors['card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=12)
                
                # Order header
                tk.Label(
                    info_frame,
                    text=f"📋 Order #{order_id} • Customer ID: {user_id}",
                    font=('Segoe UI', 11, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['text'],
                    cursor='hand2'
                ).pack(anchor=tk.W)
                
                # Customer info
                tk.Label(
                    info_frame,
                    text=f"👤 {customer_name} | 📞 {phone}",
                    font=('Segoe UI', 9),
                    bg=self.colors['card'],
                    fg=self.colors['text_light'],
                    cursor='hand2'
                ).pack(anchor=tk.W, pady=(3, 0))
                
                # Order details
                order_date_str = order_date.strftime('%d-%m-%Y %H:%M') if hasattr(order_date, 'strftime') else str(order_date)
                details_text = f"📅 {order_date_str} | 🛒 {item_count} items | 💰 ₹{total_amount}"
                
                tk.Label(
                    info_frame,
                    text=details_text,
                    font=('Segoe UI', 9),
                    bg=self.colors['card'],
                    fg=self.colors['text_light'],
                    cursor='hand2'
                ).pack(anchor=tk.W, pady=(3, 0))
                
                # Arrow
                arrow_frame = tk.Frame(card, bg=self.colors['card'])
                arrow_frame.pack(side=tk.RIGHT, padx=20)
                
                arrow_label = tk.Label(
                    arrow_frame,
                    text="→",
                    font=('Segoe UI', 16),
                    bg=self.colors['card'],
                    fg=self.colors['accent'],
                    cursor='hand2'
                )
                arrow_label.pack()
                arrow_label.bind('<Button-1>', lambda e, oid=order_id: self.show_order_details_screen(oid))
    
    def show_order_details_screen(self, order_id):
        """Show detailed items in an order"""
        self.clear_window()
        self.current_screen = 'order_details'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['accent'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=f"📦 Order #{order_id} Details",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['accent'],
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=25)
        
        self.create_button(header, "← Back", self.show_admin_orders_screen, 'primary', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get order details
        order_info, items = OrderService.get_order_details(order_id)
        
        if not order_info:
            tk.Label(
                main_frame,
                text="❌ Order not found!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['danger']
            ).pack(pady=50)
            return
        
        order_id_val, user_id, customer_name, phone, order_date, total_amount, delivery_address = order_info
        
        # Order info section
        info_card = self.create_card(main_frame, width=600, height=150)
        info_card.pack(fill=tk.X, pady=10)
        
        order_date_str = order_date.strftime('%d-%m-%Y %H:%M') if hasattr(order_date, 'strftime') else str(order_date)
        
        info_text = f"""
        Order #: {order_id_val}  |  Customer ID: {user_id}
        Customer: {customer_name}  |  Phone: {phone}
        Order Date: {order_date_str}
        Delivery Address: {delivery_address}
        Total Amount: ₹{total_amount}
        """
        
        tk.Label(
            info_card,
            text=info_text.strip(),
            font=('Segoe UI', 10),
            bg=self.colors['card'],
            fg=self.colors['text'],
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=20, pady=15)
        
        # Items section
        items_label = tk.Label(
            main_frame,
            text="📦 Ordered Items",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        items_label.pack(anchor=tk.W, pady=(20, 10))
        
        if not items:
            tk.Label(
                main_frame,
                text="No items in this order",
                font=('Segoe UI', 10),
                bg=self.colors['bg'],
                fg=self.colors['text_light']
            ).pack(pady=20)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0, height=300)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Display items
            for item_id, product_name, quantity, unit_price, total_price in items:
                card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT, bd=1)
                card.pack(fill=tk.X, pady=5, padx=10)
                
                # Item info
                info_frame = tk.Frame(card, bg=self.colors['card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)
                
                tk.Label(
                    info_frame,
                    text=f"📦 {product_name}",
                    font=('Segoe UI', 10, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['text']
                ).pack(anchor=tk.W)
                
                details_text = f"Qty: {quantity} | Price: ₹{unit_price}/unit | Total: ₹{total_price}"
                tk.Label(
                    info_frame,
                    text=details_text,
                    font=('Segoe UI', 9),
                    bg=self.colors['card'],
                    fg=self.colors['text_light']
                ).pack(anchor=tk.W, pady=(2, 0))
    
    def show_expiring_soon_screen(self):
        """Show items expiring soon with delete option"""
        self.clear_window()
        self.current_screen = 'expiring_soon'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['accent'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="⚠️ Items Expiring Soon (Next 7 Days)",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['accent'],
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=25)
        
        self.create_button(header, "← Back", self.show_admin_dashboard, 'secondary', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get expiring soon items
        items = ProductService.get_expiring_soon_items()
        
        if not items:
            tk.Label(
                main_frame,
                text="✅ No items expiring soon!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['success']
            ).pack(pady=50)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Display items
            for product_id, name, stock, expiry_date, price in items:
                card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT, bd=1)
                card.pack(fill=tk.X, pady=10)
                
                # Product info
                info_frame = tk.Frame(card, bg=self.colors['card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
                
                tk.Label(
                    info_frame,
                    text=f"📦 {name}",
                    font=('Segoe UI', 12, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['text']
                ).pack(anchor=tk.W)
                
                tk.Label(
                    info_frame,
                    text=f"Stock: {stock} | Expiry: {expiry_date} | Price: ₹{price}",
                    font=('Segoe UI', 10),
                    bg=self.colors['card'],
                    fg=self.colors['text_light']
                ).pack(anchor=tk.W, pady=(5, 0))
                
                # Action button
                def remove_item(pid=product_id, pname=name):
                    if messagebox.askyesno("Confirm", f"Remove {pname} from inventory?"):
                        remove_expired_item(pid)
                        messagebox.showinfo("Success", f"{pname} removed from inventory")
                        self.show_expiring_soon_screen()
                
                btn_frame = tk.Frame(card, bg=self.colors['card'])
                btn_frame.pack(side=tk.RIGHT, padx=15, pady=15)
                
                tk.Button(
                    btn_frame,
                    text="🗑️ Remove from Inventory",
                    command=remove_item,
                    bg=self.colors['danger'],
                    fg='white',
                    font=('Segoe UI', 9, 'bold'),
                    relief=tk.FLAT,
                    padx=10,
                    pady=8,
                    cursor='hand2'
                ).pack()
    
    def show_expired_items_screen(self):
        """Show expired items with delete option"""
        self.clear_window()
        self.current_screen = 'expired_items'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['danger'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="❌ Expired Items",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['danger'],
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=25)
        
        self.create_button(header, "← Back", self.show_admin_dashboard, 'secondary', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get expired items
        items = ProductService.get_expired_items()
        
        if not items:
            tk.Label(
                main_frame,
                text="✅ No expired items!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['success']
            ).pack(pady=50)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Display items
            for product_id, name, stock, expiry_date, price in items:
                card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT, bd=1)
                card.pack(fill=tk.X, pady=10)
                
                # Product info
                info_frame = tk.Frame(card, bg=self.colors['card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
                
                tk.Label(
                    info_frame,
                    text=f"📦 {name}",
                    font=('Segoe UI', 12, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['text']
                ).pack(anchor=tk.W)
                
                tk.Label(
                    info_frame,
                    text=f"Stock: {stock} | Expired on: {expiry_date} | Price: ₹{price}",
                    font=('Segoe UI', 10),
                    bg=self.colors['card'],
                    fg=self.colors['text_light']
                ).pack(anchor=tk.W, pady=(5, 0))
                
                # Action button
                def remove_item(pid=product_id, pname=name):
                    if messagebox.askyesno("Confirm", f"Remove {pname} from inventory?"):
                        remove_expired_item(pid)
                        messagebox.showinfo("Success", f"{pname} removed from inventory")
                        self.show_expired_items_screen()
                
                btn_frame = tk.Frame(card, bg=self.colors['card'])
                btn_frame.pack(side=tk.RIGHT, padx=15, pady=15)
                
                tk.Button(
                    btn_frame,
                    text="🗑️ Remove from Inventory",
                    command=remove_item,
                    bg=self.colors['danger'],
                    fg='white',
                    font=('Segoe UI', 9, 'bold'),
                    relief=tk.FLAT,
                    padx=10,
                    pady=8,
                    cursor='hand2'
                ).pack()
    
    def show_items_by_category(self):
        """Show categories list for admin to select"""
        self.clear_window()
        self.current_screen = 'categories_list'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text="📁 Categories",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=25)
        
        self.create_button(header, "← Back", self.show_admin_dashboard, 'secondary', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get categories with count
        categories = ProductService.get_categories_with_count()
        
        if not categories:
            tk.Label(
                main_frame,
                text="✅ No categories available!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['success']
            ).pack(pady=50)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Display categories
            for cat_id, cat_name, item_count in categories:
                card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT, bd=1)
                card.pack(fill=tk.X, pady=8, padx=10)
                card.config(cursor='hand2')
                
                # Click handler
                def on_category_click(cid=cat_id, cname=cat_name):
                    self.show_category_products(cid, cname)
                
                # Bind click to card
                card.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_category_products(cid, cname))
                
                # Category info frame
                info_frame = tk.Frame(card, bg=self.colors['card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)
                
                # Category name
                cat_label = tk.Label(
                    info_frame,
                    text=f"📁 {cat_name}",
                    font=('Segoe UI', 13, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['primary'],
                    cursor='hand2'
                )
                cat_label.pack(anchor=tk.W)
                cat_label.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_category_products(cid, cname))
                
                # Item count
                count_label = tk.Label(
                    info_frame,
                    text=f"{item_count} item{'s' if item_count != 1 else ''}",
                    font=('Segoe UI', 10),
                    bg=self.colors['card'],
                    fg=self.colors['text_light'],
                    cursor='hand2'
                )
                count_label.pack(anchor=tk.W, pady=(3, 0))
                count_label.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_category_products(cid, cname))
                
                # Arrow
                arrow_frame = tk.Frame(card, bg=self.colors['card'])
                arrow_frame.pack(side=tk.RIGHT, padx=20)
                
                arrow_label = tk.Label(
                    arrow_frame,
                    text="→",
                    font=('Segoe UI', 16),
                    bg=self.colors['card'],
                    fg=self.colors['primary'],
                    cursor='hand2'
                )
                arrow_label.pack()
                arrow_label.bind('<Button-1>', lambda e, cid=cat_id, cname=cat_name: self.show_category_products(cid, cname))
    
    def show_category_products(self, category_id, category_name):
        """Show products in selected category"""
        self.clear_window()
        self.current_screen = 'category_products'
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header.pack(fill=tk.X)
        
        tk.Label(
            header,
            text=f"📦 {category_name}",
            font=('Segoe UI', 16, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        ).pack(side=tk.LEFT, padx=30, pady=25)
        
        self.create_button(header, "← Back to Categories", self.show_items_by_category, 'secondary', 10).pack(
            side=tk.RIGHT, padx=20, pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Get products in category
        products = ProductService.get_products_in_category(category_id)
        
        if not products:
            tk.Label(
                main_frame,
                text=f"✅ No products in {category_name}!",
                font=('Segoe UI', 14),
                bg=self.colors['bg'],
                fg=self.colors['success']
            ).pack(pady=50)
        else:
            # Create scrollable frame
            canvas = tk.Canvas(main_frame, bg=self.colors['bg'], highlightthickness=0)
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bind mousewheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Display products
            for product_id, name, stock, price, unit, expiry_date in products:
                card = tk.Frame(scrollable_frame, bg=self.colors['card'], relief=tk.FLAT, bd=1)
                card.pack(fill=tk.X, pady=8, padx=10)
                
                # Product info
                info_frame = tk.Frame(card, bg=self.colors['card'])
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=12)
                
                # Product name
                tk.Label(
                    info_frame,
                    text=f"📦 {name}",
                    font=('Segoe UI', 11, 'bold'),
                    bg=self.colors['card'],
                    fg=self.colors['text']
                ).pack(anchor=tk.W)
                
                # Product details
                expiry_text = f"Expires: {expiry_date}" if expiry_date else "No expiry"
                details_text = f"Stock: {stock} {unit} | Price: ₹{price} | {expiry_text}"
                
                tk.Label(
                    info_frame,
                    text=details_text,
                    font=('Segoe UI', 9),
                    bg=self.colors['card'],
                    fg=self.colors['text_light']
                ).pack(anchor=tk.W, pady=(3, 0))
    
    def logout(self):
        """Logout user"""
        self.current_user = None
        self.current_staff = None
        self.user_type = None
        self.show_login_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernGroceryApp(root)
    root.mainloop()
