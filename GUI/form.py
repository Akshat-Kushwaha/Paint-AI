import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as font
from utils import draw_it

class MyForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint-AI")
        self.root.geometry("500x700")
        
        # Initialize placeholder attribute
        self.placeholder = "e.g., A sunset over mountains"
        self.is_placeholder_active = True
        
        # Configure style for modern look
        self.setup_styles()
        
        # Create main container
        self.main_container = ttk.Frame(root, style='Main.TFrame')
        self.main_container.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Create a card-like frame for the form
        self.card = ttk.Frame(self.main_container, style='Card.TFrame')
        self.card.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Configure grid weights for the card
        self.card.columnconfigure(0, weight=1)
        
        # Title with custom font
        title_font = font.Font(family='Helvetica', size=24, weight='bold')
        title_label = ttk.Label(self.card, text="PAINT-AI", 
                               font=title_font, style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(30, 10))
        
        # Subtitle
        subtitle_font = font.Font(family='Helvetica', size=12)
        subtitle_label = ttk.Label(self.card, text="Transform your ideas into art",
                                  font=subtitle_font, style='Subtitle.TLabel')
        subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Input Section
        input_label = ttk.Label(self.card, text="Describe your drawing:",
                               style='Heading.TLabel')
        input_label.grid(row=2, column=0, sticky='w', padx=40, pady=(0, 5))
        
        # Modern entry
        entry_frame = ttk.Frame(self.card, style='EntryFrame.TFrame')
        entry_frame.grid(row=3, column=0, padx=40, pady=(0, 20), sticky='ew')
        entry_frame.columnconfigure(0, weight=1)
        
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(entry_frame, textvariable=self.input_var,
                                    font=('Helvetica', 11), style='Modern.TEntry')
        self.input_entry.grid(row=0, column=0, sticky='ew', ipady=8)
        
        # Add placeholder effect
        self.add_placeholder()
        
        # Radio Buttons Section
        radio_label = ttk.Label(self.card, text="Select your preference:",
                               style='Heading.TLabel')
        radio_label.grid(row=4, column=0, sticky='w', padx=40, pady=(0, 5))
        
        self.radio_var = tk.StringVar(value="realistic")
        
        # Radio button frame
        radio_container = ttk.Frame(self.card, style='RadioContainer.TFrame')
        radio_container.grid(row=5, column=0, padx=40, pady=(0, 20), sticky='w')
        
        # Modern radio buttons
        self.realistic_radio = ttk.Radiobutton(radio_container, 
                                              text="Realistic",
                                              variable=self.radio_var, 
                                              value="realistic",
                                              style='Modern.TRadiobutton')
        self.realistic_radio.pack(anchor='w', pady=5)
        
        # Add descriptive text for each option
        realistic_desc = ttk.Label(radio_container, 
                                  text="Best for complex scenes and detailed artwork",
                                  style='Description.TLabel')
        realistic_desc.pack(anchor='w', pady=(0, 10))
        
        self.shape_radio = ttk.Radiobutton(radio_container,
                                          text="Shape-based",
                                          variable=self.radio_var, 
                                          value="shape",
                                          style='Modern.TRadiobutton')
        self.shape_radio.pack(anchor='w', pady=5)
        
        shape_desc = ttk.Label(radio_container,
                              text="Optimized for MS Paint style tools and geometric shapes",
                              style='Description.TLabel')
        shape_desc.pack(anchor='w', pady=(0, 10))
        
        # Modern Submit Button
        self.submit_btn = ttk.Button(self.card, text="Generate Art",
                                     command=self.submit_form,
                                     style='Modern.TButton')
        self.submit_btn.grid(row=6, column=0, pady=20)
        
        # Status/Result Card (single card that changes content)
        self.status_card = ttk.Frame(self.card, style='ResultCard.TFrame')
        self.status_card.grid(row=7, column=0, padx=40, pady=(0, 20), sticky='ew')
        self.status_card.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(self.status_card, text="",
                                     style='Result.TLabel', wraplength=350)
        self.status_label.grid(row=0, column=0, padx=15, pady=15)
        
        # Initially hide status card
        self.status_card.grid_remove()
        
        # Bind events
        self.input_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.input_entry.bind('<FocusOut>', self.on_entry_focus_out)
        root.bind('<Return>', lambda event: self.submit_form())
        
        # Set focus to entry
        self.input_entry.focus()
        
    def setup_styles(self):
        """Configure modern styles for ttk widgets"""
        style = ttk.Style()
        
        # Try to use 'clam' theme, fallback to default if not available
        try:
            style.theme_use('clam')
        except tk.TclError:
            pass  # Keep default theme if 'clam' is not available
        
        # Color palette
        self.colors = {
            'bg': '#f5f5f7',
            'card_bg': '#ffffff',
            'primary': '#4361ee',
            'primary_light': '#4895ef',
            'text': '#2b2d42',
            'text_light': '#8d99ae',
            'success': '#06d6a0',
            'border': '#e9ecef',
            'hover': '#3f37c9',
            'warning': '#f72585',
            'success_bg': '#06d6a0'
        }
        
        # Configure colors for different elements
        style.configure('Main.TFrame', background=self.colors['bg'])
        
        style.configure('Card.TFrame', 
                       background=self.colors['card_bg'])
        
        style.configure('Title.TLabel',
                       background=self.colors['card_bg'],
                       foreground=self.colors['primary'])
        
        style.configure('Subtitle.TLabel',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_light'])
        
        style.configure('Heading.TLabel',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text'])
        
        style.configure('EntryFrame.TFrame',
                       background=self.colors['card_bg'],
                       relief='solid',
                       borderwidth=1)
        
        # Configure entry styling
        style.configure('Modern.TEntry',
                       fieldbackground=self.colors['card_bg'],
                       foreground=self.colors['text'],
                       borderwidth=1,
                       relief='solid')
        style.map('Modern.TEntry',
                 fieldbackground=[('focus', self.colors['card_bg'])],
                 foreground=[('focus', self.colors['text'])])
        
        # Radio button styling
        style.configure('Modern.TRadiobutton',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text'])
        style.map('Modern.TRadiobutton',
                 background=[('active', self.colors['card_bg'])])
        
        style.configure('Description.TLabel',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_light'])
        
        # Button styling
        style.configure('Modern.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(30, 12))
        style.map('Modern.TButton',
                 background=[('active', self.colors['hover']),
                           ('pressed', self.colors['primary'])])
        
        # Status card styling (will be dynamically changed)
        style.configure('ResultCard.TFrame',
                       background=self.colors['primary_light'])
        
        style.configure('Result.TLabel',
                       background=self.colors['primary_light'],
                       foreground='white',
                       padding=10)
        
        # Success card styling
        style.configure('Success.TFrame',
                       background=self.colors['success_bg'])
        
        style.configure('Success.TLabel',
                       background=self.colors['success_bg'],
                       foreground='white',
                       padding=10)
        
        # Warning card styling
        style.configure('Warning.TFrame',
                       background=self.colors['warning'])
        
        style.configure('Warning.TLabel',
                       background=self.colors['warning'],
                       foreground='white',
                       padding=10)
    
    def add_placeholder(self):
        """Add placeholder text to entry"""
        self.input_entry.insert(0, self.placeholder)
        self.input_entry.configure(foreground=self.colors['text_light'])
    
    def on_entry_focus_in(self, event):
        """Handle entry focus in event"""
        if self.input_entry.get() == self.placeholder:
            self.input_entry.delete(0, tk.END)
            self.input_entry.configure(foreground=self.colors['text'])
    
    def on_entry_focus_out(self, event):
        """Handle entry focus out event"""
        if not self.input_entry.get().strip():
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, self.placeholder)
            self.input_entry.configure(foreground=self.colors['text_light'])
    
    def update_status(self, message, status_type="progress"):
        """Update the status card with message and appropriate styling"""
        self.status_label.config(text=message)
        
        # Change styling based on status type
        if status_type == "success":
            self.status_card.configure(style='Success.TFrame')
            self.status_label.configure(style='Success.TLabel')
        elif status_type == "error":
            self.status_card.configure(style='Warning.TFrame')
            self.status_label.configure(style='Warning.TLabel')
        else:  # progress/default
            self.status_card.configure(style='ResultCard.TFrame')
            self.status_label.configure(style='Result.TLabel')
        
        # Make sure the card is visible
        self.status_card.grid()
        self.root.update()  # Force update to show changes immediately
    
    def submit_form(self):
        """Handle form submission"""
        prompt = self.input_entry.get().strip()
        
        # Check if placeholder is active
        if prompt == self.placeholder:
            prompt = ""
        
        preference = self.radio_var.get()
        
        if not prompt:
            messagebox.showwarning("Input Required", 
                                  "Please describe what you'd like to draw!",
                                  parent=self.root)
            return
        
        # Map preference values to display text
        preference_text = "Realistic" if preference == "realistic" else "Shape-based"
        
        # Show progress status
        self.update_status("🔄 Generating your artwork... Please wait.", "progress")
        
        try:
            # Start drawing process
            draw_it.draw(prompt, preference)
            
            # Show success status with details
            success_message = f"✓ Generated!\n\nPrompt: {prompt}\nStyle: {preference_text}"
            self.update_status(success_message, "success")
            
            # Show success messagebox (optional - you can remove this if it's redundant)
            messagebox.showinfo("Success!", 
                               f"✨ Your art has been generated successfully!",
                               parent=self.root)
            
        except Exception as e:
            # Show error status
            error_message = f"✗ Error: Failed to generate artwork\n\n{str(e)}"
            self.update_status(error_message, "error")
            
            # Show error messagebox
            messagebox.showerror("Error", 
                               f"Failed to generate artwork: {str(e)}",
                               parent=self.root)
        
        # Optionally clear the entry
        # self.input_entry.delete(0, tk.END)
        # self.on_entry_focus_out(None)

def main():
    # Create the main window
    root = tk.Tk()

    # Set window icon 
    root.iconbitmap('GUI/icon.ico')

    # Center the window on screen
    root.update_idletasks()
    width = 500
    height = 700
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Make window non-resizable
    root.resizable(False, False)
    
    # Create an instance of the form
    app = MyForm(root)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()