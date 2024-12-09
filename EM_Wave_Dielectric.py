import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.font as tkfont

from tkinter import messagebox


# Constants and initial parameters
freq = 1.5e8  # Frequency in Hz
amplitude = 1.0  # Amplitude of the wave
epsilon_r = 1.0  # Relative permittivity of the dielectric
sigma = 0.01  # Conductivity of the dielectric
mu_r = 1.0  # Relative permeability of the dielectric

# Color scheme
DARK_BG = '#1E1E1E'  # Dark gray/black background
DARKER_BG = '#141414'  # Even darker background
ACCENT_COLOR = '#00FF9C'  # Keep mint for accents
TEXT_COLOR = '#FFFFFF'  # Pure white text
BUTTON_BG = '#333333'  # Medium gray button background
BUTTON_ACTIVE_BG = '#CCCCCC'  # Light gray for active state
ENTRY_BG = '#2D2D2D'  # Dark gray entry background


def format_frequency(value):
    if value >= 1e9:
        return f"{value / 1e9:.2f} GHz"
    elif value >= 1e6:
        return f"{value / 1e6:.2f} MHz"
    elif value >= 1e3:
        return f"{value / 1e3:.2f} kHz"
    else:
        return f"{value:.2f} Hz"
def format_distance(value, precision=1):
    if value >= 1:
        return f"{value :.{precision}f} m"
    elif value >= 1e-2:
        return f"{value * 1e2:.{precision}f} cm"
    else:
        return f"{value * 1e3:.{precision}f} mm"
    
def format_scientific(value, precision=1):
    def format_part(part):
        formatted_part = f"{part:.{precision}e}"
        base, exponent = formatted_part.split("e")
        exponent = int(exponent)
        if exponent == 0:
            return f"{float(base):.{precision}f}"
        else:
            return f"{float(base):.{precision}f} x 10^({exponent})"

    if isinstance(value, complex):
        real_part = format_part(value.real)
        imag_part = format_part(value.imag)
        if value.imag > 0: return f"{real_part} + j{imag_part}"
        elif value.imag < 0: return f"{real_part} - j{imag_part[1:]}"
        else: return f"{real_part}"
    else:
        
        return format_part(value)


# Create custom button style
def create_custom_button(parent, text, command):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=BUTTON_BG,
        fg=TEXT_COLOR,
        activebackground=BUTTON_ACTIVE_BG,
        activeforeground=TEXT_COLOR,
        relief='flat',
        bd=0,
        padx=10,
        pady=5,
        font=custom_font
    )
    return button


root = tk.Tk()
root.title("Electromagnetic Waves In Lossy Dielectric")

# Get screen dimensions


# Configure root window
root.configure(bg=DARK_BG)

# Create custom fonts
def create_font(size, weight="normal"):
    return tkfont.Font(family="Segoe UI", size=size, weight=weight)

title_font = create_font(14, "bold")
custom_font = create_font(11)
SUBHEADING_FONT = create_font(12, "bold")

# Create Tkinter window with dark theme

# Apply custom font to all widgets
root.option_add("*Font", custom_font)

# Define the dark theme styles
style = ttk.Style()
style.theme_use('clam')  # Use 'clam' theme as a base

style.configure('Dark.Horizontal.TScale',
    background=DARK_BG,
    troughcolor=DARKER_BG,
    troughrelief='flat',
    sliderlength=30,
    sliderthickness=20,
    sliderrelief='flat'
)

style.configure('Dark.TButton',
    background=BUTTON_BG,
    foreground=TEXT_COLOR,
    padding=(10, 5),
    relief='flat'
)
style.map('Dark.TButton',
    background=[('active', BUTTON_ACTIVE_BG)],
    foreground=[('active', TEXT_COLOR)]
)

# Set up the figure and axis with dark theme
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(13,7))
ax.set_xlim(0, 5)
ax.set_ylim(-1.5, 1.5)
ax.set_title(f"Electromagnetic Wave in Lossy Dielectric (f={format_frequency(freq)})", color='white')
ax.set_xlabel("Distance (m)", color='white')
ax.set_ylabel("Field Amplitude", color='white')
ax.tick_params(colors='white')


def setup_cursor():
    annot = ax.annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                        bbox=dict(boxstyle='round,pad=0.5', fc=DARKER_BG, alpha=0.8),
                        color=TEXT_COLOR,
                        arrowprops=dict(arrowstyle="->", color=ACCENT_COLOR),
                        zorder=1000)
    annot.set_visible(False)

    def find_nearest_curve_point(event):
        if not hasattr(event, 'xdata') or not hasattr(event, 'ydata'):
            return None, None, float('inf')
            
        mouse_x = event.xdata
        mouse_y = event.ydata
        
        # Get current line data
        x_data1 = e_line1.get_xdata()
        y_data1 = e_line1.get_ydata()
        x_data2 = e_line2.get_xdata()
        y_data2 = e_line2.get_ydata()
        
        # Combine data from both lines
        x_data = np.concatenate((x_data1, x_data2))
        y_data = np.concatenate((y_data1, y_data2))
        
        if len(x_data) == 0 or len(y_data) == 0:
            return None, None, float('inf')
            
        # Calculate distances to all points
        distances = np.sqrt((x_data - mouse_x)**2 + (y_data - mouse_y)**2)
        min_idx = np.argmin(distances)
        
        return x_data[min_idx], y_data[min_idx], distances[min_idx]

    def hover(event):
        if event.inaxes == ax:
            x, y, dist = find_nearest_curve_point(event)
            if x is not None and y is not None and dist < 0.1:  # Threshold for showing coordinates
                annot.xy = (x, y)
                text = f'x={x:.2f}\ny={y:.2f}'
                annot.set_text(text)
                annot.set_visible(True)
            else:
                annot.set_visible(False)
            fig.canvas.draw_idle()

    def on_leave(event):
        annot.set_visible(False)
        fig.canvas.draw_idle()

    # Connect events
    fig.canvas.mpl_connect('motion_notify_event', hover)
    fig.canvas.mpl_connect('axes_leave_event', on_leave)

    return annot

# Call setup_cursor after creating the animation
annot = setup_cursor()


# Create the initial lines with visibility set to True
e_line1, = ax.plot([], [], lw=2, color='cyan', label='E-field (Air)', visible=True)
e_line2, = ax.plot([], [], lw=2, color='orange', label='E-field (Lossy Dielectric)', visible=True)
b_line1, = ax.plot([], [], lw=2, color='green', label='B-field (Air)', visible=True)
b_line2, = ax.plot([], [], lw=2, color='red', label='B-field (Lossy Dielectric)', visible=True)
attenuation_line, = ax.plot([], [], lw=2, color='magenta', label='Attenuated Amplitude', linestyle='--')
skin_depth_line, = ax.plot([], [], lw=2, color='yellow', linestyle='--', label='Skin Depth')
boundary_line, = ax.plot([], [], lw=2, color='white', linestyle='--', label='Boundary')  # Boundary line
ax.legend()

# Function to calculate wave parameters
def calculate_wave_params():
    omega = 2 * np.pi * freq
    epsilon = epsilon_r * 8.854e-12  # Permittivity of the dielectric
    mu = mu_r * 4 * np.pi * 1e-7  # Permeability of the dielectric
    
    try:
        # Complex permittivity
        epsilon_complex = epsilon - 1j * sigma / omega
        
        # Complex wavenumber
        k = -1.j * omega * np.sqrt(mu * epsilon_complex)
        if k.real <= 0: 
            k = -k  # Getting the root whose alpha is positive
        
        # Phase Constant
        beta = k.imag #might be wrong
        # Phase Velocity
        v_p = omega/beta if beta != 0 else float('inf') #might be wrong
        #eta
        eta=1j*omega*mu/k
        # Attenuation constant
        alpha = k.real
        
        # Transition frequency
        ft = sigma / (2 * np.pi * epsilon) if epsilon != 0 else float('inf')
        
        # Skin depth
        skin_depth = 1 / alpha if alpha != 0 else float('inf')
        
        return omega, beta, alpha, epsilon_complex, ft, skin_depth, v_p,eta
        
    except (ZeroDivisionError, ValueError):
        return None, None, None, None, None, None, None, None

# Initialize the wave
def init():
    e_line1.set_data([], [])
    e_line2.set_data([], [])
    b_line1.set_data([], [])
    b_line2.set_data([], [])
    e_line1.set_visible(True)
    e_line2.set_visible(True)
    b_line1.set_visible(True)
    b_line2.set_visible(True)
    return e_line1, e_line2, b_line1, b_line2, attenuation_line, skin_depth_line, boundary_line

# Animation function
def animate(frame_number):
    params = calculate_wave_params()
    if params is None or None in params:
        return e_line1, e_line2, b_line1, b_line2, attenuation_line, skin_depth_line, boundary_line
    
    omega, beta, alpha, epsilon_complex, ft, skin_depth, v_p,eta = params
    x = np.linspace(0, 5, 1000)
    time = frame_number * 1e-10  # Convert frame number to time (seconds)
    
    # Create a wave with constant amplitude from x=0 to x=1
    beta_medium1 = np.sqrt(8.854e-12*4 * np.pi * 1e-7 )*omega
    eta_medium1=376.73
    y_e1 = amplitude * np.cos(omega * time - beta_medium1 * (x[x <= 1]-1))
    y_b1 = 40*y_e1 / eta_medium1  # Calculate B-field for medium 1
    
    phase=omega * time - beta * (x[x > 1] - 1)
    # Define attenuated amplitude starting from x=1
    attenuated_amplitude = amplitude * np.exp(-alpha * (x[x >= 1] - 1))
    k1=1/eta
    # Create the second wave segment with continuity at x=1
    y_e2 = attenuated_amplitude * np.cos(phase)
    # Calculate B-field for lossy dielectric
    y_b2 =40*( attenuated_amplitude * np.cos(phase)*k1.real + attenuated_amplitude * np.sin(phase)*k1.imag)
    
    # Update line data while preserving visibility
    current_e_visible = e_line1.get_visible()
    current_b_visible = b_line1.get_visible()
    
    # Update data for all lines
    e_line1.set_data(x[x <= 1], y_e1)
    e_line2.set_data(x[x > 1], y_e2)
    b_line1.set_data(x[x <= 1], y_b1)
    b_line2.set_data(x[x > 1], y_b2)
    attenuation_line.set_data(x[x >= 1], attenuated_amplitude)
    skin_depth_line.set_data([1 + skin_depth, 1 + skin_depth], [-1.5, 1.5])
    boundary_line.set_data([1, 1], [-1.5, 1.5])
    
    # Restore visibility states
    e_line1.set_visible(current_e_visible)
    e_line2.set_visible(current_e_visible)
    b_line1.set_visible(current_b_visible)
    b_line2.set_visible(current_b_visible)
    
    return e_line1, e_line2, b_line1, b_line2, attenuation_line, skin_depth_line, boundary_line

# Create the animation 
anim = FuncAnimation(fig, animate, init_func=init, frames=1000, interval=10, blit=False)

# Create main frame
main_frame = tk.Frame(root, bg=DARK_BG)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create plot frame
plot_frame = tk.Frame(main_frame, bg=DARK_BG)
plot_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Add the plot to the plot frame
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

# Add developers section at the bottom of plot frame
dev_frame = tk.Frame(plot_frame, bg=DARK_BG)
dev_frame.pack(fill='x', pady=(0,10))

# Add separator line
separator = tk.Frame(dev_frame, height=1, bg=ACCENT_COLOR)
separator.pack(fill='x', pady=(0,10))

# Add developers section
developers = tk.Label(
    dev_frame,
    text="Developers",
    bg=DARK_BG,
    fg=ACCENT_COLOR,
    font=('Segoe UI', 11, 'bold')
)
developers.pack(pady=(0,5))

# Add developer names with larger font
dev_names = tk.Label(
    dev_frame,
    text="Karan Pattanaik • Nenavath Hari Naik • Davu Vishwanth Reddy",
    bg=DARK_BG,
    fg=TEXT_COLOR,
    font=('Segoe UI', 12)  # Increased from 10 to 12
)
dev_names.pack(pady=(0,5))

# Add affiliation
affiliation = tk.Label(
    dev_frame,
    text="@IIT Bhubaneswar",
    bg=DARK_BG,
    fg=TEXT_COLOR,
    font=('Segoe UI', 10, 'italic')
)
affiliation.pack(pady=(0,5))

# Create control frame
control_frame = tk.Frame(main_frame, bg=DARKER_BG, padx=20, pady=20)
control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Add a title to the control frame
title_label = tk.Label(control_frame, text="Wave Parameters", bg=DARKER_BG, fg=ACCENT_COLOR, font=title_font)
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 5),padx=(0, 20), sticky="e")

# Add reset button (modified to be smaller and in top-right)
def reset_to_default():
    # Reset all sliders to their default values
    freq_slider.set(np.log10(1.5e8))  # Default frequency in log scale
    amp_slider.set(1.0)
    epsilon_slider.set(1.0)
    sigma_slider.set(np.log10(0.01))  # Default sigma in log scale
    mu_slider.set(1.0)
    
    # Reset field visibility
    e_line1.set_visible(True)
    e_line2.set_visible(True)
    b_line1.set_visible(True)
    b_line2.set_visible(True)
    
    # Reset field buttons appearance
    e_field_button.config(bg=BUTTON_ACTIVE_BG, fg=DARKER_BG, relief='sunken')
    b_field_button.config(bg=BUTTON_ACTIVE_BG, fg=DARKER_BG, relief='sunken')
    
    update_params()
    update_legend()
    fig.canvas.draw_idle()

reset_button = create_custom_button(control_frame, "Reset all", reset_to_default)
reset_button.config(width=2, padx=5)  # Make button smaller
reset_button.grid(row=0, column=2, pady=(2,10), padx=(19, 0), sticky="ew")

def create_slider_with_value(parent, label, from_, to, initial_value, row, precision=2):
    tk.Label(parent, text=label, bg=DARKER_BG, fg=TEXT_COLOR).grid(row=row+1, column=0, padx=5, pady=7, sticky="w")
    
    slider = ttk.Scale(
        parent, 
        from_=from_,
        to=to,
        orient="horizontal", 
        length=200, 
        style='Dark.Horizontal.TScale'
    )
    slider.set(initial_value)
    slider.grid(row=row+1, column=1, padx=5, pady=5, sticky="ew")
    
    value_entry = tk.Entry(
        parent, 
        width=10, 
        justify='right', 
        bg=ENTRY_BG, 
        fg=TEXT_COLOR, 
        insertbackground=TEXT_COLOR, 
        relief='flat', 
        bd=0
    )
    
    # Set initial value with appropriate formatting
    if label.startswith("Frequency"):
        value_entry.insert(0, format_frequency(initial_value))
    else:
        value_entry.insert(0, f"{initial_value:.{precision}f}")
    
    def on_entry_change(event):
        try:
            text = value_entry.get()
            if label.startswith("Frequency"):
                # Parse frequency with units
                text = text.upper()
                if "GHZ" in text:
                    value = float(text.replace("GHZ", "")) * 1e9
                elif "MHZ" in text:
                    value = float(text.replace("MHZ", "")) * 1e6
                elif "KHZ" in text:
                    value = float(text.replace("KHZ", "")) * 1e3
                else:
                    value = float(text.replace("HZ", ""))
            else:
                value = float(text)
            
            #Clamp value between from_ and to_
            if value < from_:
                value = from_
            elif value > to:
                value = to
                
            slider.set(value)
            update_params()
        except ValueError:
            # Restore previous value if input is invalid
            value = slider.get()
            value_entry.delete(0, tk.END)
            if label.startswith("Frequency"):
                value_entry.insert(0, format_frequency(value))
            else:
                value_entry.insert(0, f"{value:.{precision}f}")
    
    def on_slider_change(event):
        value = slider.get()
        value_entry.delete(0, tk.END)
        if label.startswith("Frequency"):
            value_entry.insert(0, format_frequency(value))
        else:
            value_entry.insert(0, f"{value:.{precision}f}")
        update_params()
    
    value_entry.bind('<Return>', on_entry_change)
    value_entry.bind('<FocusOut>', on_entry_change)
    slider.bind('<Motion>', on_slider_change)
    slider.bind('<ButtonRelease-1>', on_slider_change)
    
    value_entry.grid(row=row+1, column=2, padx=5, pady=5, sticky="w")
    return slider, value_entry

def create_log_slider_with_value(parent, label, from_, to, initial_value, row, precision=2):
    tk.Label(parent, text=label, bg=DARKER_BG, fg=TEXT_COLOR).grid(row=row+1, column=0, padx=5, pady=7, sticky="w")
    
    # Convert to log space for slider
    log_from = np.log10(from_)
    log_to = np.log10(to)
    log_initial = np.log10(initial_value)
    
    slider = ttk.Scale(
        parent, 
        from_=log_from,
        to=log_to,
        orient="horizontal", 
        length=200, 
        style='Dark.Horizontal.TScale'
    )
    
    # Modify the get method to return actual value instead of log value
    original_get = slider.get
    def get_value():
        return 10 ** float(original_get())
    slider.get = get_value
    
    slider.set(log_initial)
    slider.grid(row=row+1, column=1, padx=5, pady=5, sticky="ew")
    
    value_entry = tk.Entry(
        parent, 
        width=10, 
        justify='right', 
        bg=ENTRY_BG, 
        fg=TEXT_COLOR, 
        insertbackground=TEXT_COLOR, 
        relief='flat', 
        bd=0
    )
    
    # Set initial value with appropriate formatting
    if label.startswith("Frequency"):
        value_entry.insert(0, format_frequency(initial_value))
    else:
        value_entry.insert(0, f"{initial_value:.{precision}f}")
    
    def on_entry_change(event):
        try:
            text = value_entry.get()
            if label.startswith("Frequency"):
                # Parse frequency with units
                text = text.upper()
                if "GHZ" in text:
                    value = float(text.replace("GHZ", "")) * 1e9
                elif "MHZ" in text:
                    value = float(text.replace("MHZ", "")) * 1e6
                elif "KHZ" in text:
                    value = float(text.replace("KHZ", "")) * 1e3
                else:
                    value = float(text.replace("HZ", ""))
            else:
                value = float(text)
            
            # Clamp value between from_ and to_
            # if value < from_:
            #     value = from_
            # elif value > to:
            #     value = to
            if value>from_ and value<to:
                slider.set(np.log10(value))
            update_params()
        except ValueError:
            # Restore previous value if input is invalid
            value = slider.get()
            value_entry.delete(0, tk.END)
            if label.startswith("Frequency"):
                value_entry.insert(0, format_frequency(value))
            else:
                value_entry.insert(0, f"{value:.{precision}f}")
    
    def on_slider_change(event):
        value = slider.get()
        value_entry.delete(0, tk.END)
        if label.startswith("Frequency"):
            value_entry.insert(0, format_frequency(value))
        else:
            value_entry.insert(0, f"{value:.{precision}f}")
        update_params()
    
    value_entry.bind('<Return>', on_entry_change)
    value_entry.bind('<FocusOut>', on_entry_change)
    slider.bind('<Motion>', on_slider_change)
    slider.bind('<ButtonRelease-1>', on_slider_change)
    
    value_entry.grid(row=row+1, column=2, padx=5, pady=5, sticky="w")
    return slider, value_entry

# Function to start/pause the animation
def toggle_animation():
    if pause_button.config('text')[-1] == 'Pause':
        anim.event_source.stop()
        pause_button.config(text='Start')
    else:
        anim.event_source.start()
        pause_button.config(text='Pause')




# Create sliders
freq_slider, freq_value = create_log_slider_with_value(control_frame, "Frequency (Hz)", 1e7, 2e9, freq, 0)
amp_slider, amp_value = create_slider_with_value(control_frame, "Amplitude (V/m)", 0.1, 3, amplitude, 1)
epsilon_slider, epsilon_value = create_slider_with_value(control_frame, "Relative Permittivity", 1.0, 10, epsilon_r, 2)
sigma_slider, sigma_value = create_log_slider_with_value(control_frame, "Conductivity (S/m)", 1e-5, 0.100001, sigma, 3, precision=5)
mu_slider, mu_value = create_slider_with_value(control_frame, "Relative Permeability", 0.1, 2.0, mu_r, 4)

# Create start/pause button
pause_button = create_custom_button(control_frame, "Pause", toggle_animation)
pause_button.grid(row=6, column=0, columnspan=3, pady=15)



def show_transition_frequency_complex_effects():
    transition_freq = calculate_wave_params()[4]
    if transition_freq == np.inf:
        messagebox.showerror("Error", "Transition frequency is infinite; cannot plot graphs.")
        return
    if transition_freq < 1e7:
        messagebox.showerror("Error", "Transition frequency is too low; cannot plot graphs.")
        return
    elif transition_freq > 2e9:
        messagebox.showerror("Error", "Transition frequency is too high; cannot plot graphs.")
        return
    
    # Frequency range around the transition frequency
    freq_range = np.linspace(transition_freq * 0.5, transition_freq * 2, 200)

    # Initialize arrays for storing real and imaginary parts of the wavenumber (beta and alpha)
    betas = []
    alphas = []

    for f in freq_range:
        global freq
        freq = f
        _, beta, alpha, _, _, _, _,_ = calculate_wave_params()
        
        betas.append(beta)  # Phase shift per distance
        alphas.append(alpha)  # Attenuation per distance

    # Plot the results in a new window with vertical lines marking transition frequency
    if not hasattr(show_transition_frequency_complex_effects, 'window') or not show_transition_frequency_complex_effects.window.winfo_exists():
        show_transition_frequency_complex_effects.window = tk.Toplevel(root)
    new_window = show_transition_frequency_complex_effects.window
    new_window.title("Complex Effects around Transition Frequency")
    
    fig, axs = plt.subplots(2, 1, figsize=(8, 10))
    
    # Plot beta (phase shift per distance) vs Frequency
    axs[0].plot(freq_range, betas, color="cyan")
    axs[0].set_xscale('log')
    axs[0].axvline(transition_freq, color="red", linestyle="--", label="Transition Frequency")
    axs[0].legend()
    axs[0].set_title("Phase Shift per Distance (Beta) vs Frequency")
    axs[0].set_xlabel(f"Frequency ({format_frequency(freq)})")
    axs[0].set_ylabel("Beta (rad/m)")

    # Plot alpha (attenuation per distance) vs Frequency
    axs[1].plot(freq_range, alphas, color="magenta")
    axs[1].set_xscale('log')
    axs[1].axvline(transition_freq, color="red", linestyle="--", label="Transition Frequency")
    axs[1].legend()
    axs[1].set_title("Attenuation per Distance (Alpha) vs Frequency")
    axs[1].set_xlabel(f"Frequency ({format_frequency(freq)})")
    axs[1].set_ylabel("Alpha (Np/m)")


    fig.tight_layout()
    # Embed the plot into the new Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Add button to control frame for new complex effect plots
complex_effects_button = create_custom_button(
    control_frame, 
    "Show Complex Effects Around Transition Frequency", 
    show_transition_frequency_complex_effects
)
complex_effects_button.grid(row=7, column=0, columnspan=3, pady=10)


def set_to_transition_frequency():
    transition_freq = calculate_wave_params()[4]
    if transition_freq == np.inf:
        messagebox.showerror("Error", "Transition frequency is infinite; cannot plot graphs.")
        return
    if transition_freq < 1e7:
        messagebox.showerror("Error", "Transition frequency is too low; cannot plot graphs.")
        return
    elif transition_freq > 2e9:
        messagebox.showerror("Error", "Transition frequency is too high; cannot plot graphs.")
        return
    else:
        # Convert to log space for the slider
        log_transition_freq = np.log10(transition_freq)
        freq_slider.set(log_transition_freq)
        # Update the display and parameters
        freq_value.delete(0, tk.END)
        freq_value.insert(0, format_frequency(transition_freq))
        update_params()

# Button to set frequency to transition frequency
set_transition_freq_button = create_custom_button(
    control_frame, 
    "Set to Transition Frequency", 
    set_to_transition_frequency
)
set_transition_freq_button.grid(row=8, column=0, columnspan=3, pady=10)


# Function to toggle E-field visibility and button state
def show_e_field():
    is_visible = not e_line1.get_visible()
    e_line1.set_visible(is_visible)
    e_line2.set_visible(is_visible)
    # Update button appearance with light gray active state
    if is_visible:
        e_field_button.config(
            bg=BUTTON_ACTIVE_BG,
            fg=DARKER_BG,  # Dark text on light background when active
            relief='sunken'
        )
    else:
        e_field_button.config(
            bg=BUTTON_BG,
            fg=TEXT_COLOR,  # White text on dark background when inactive
            relief='flat'
        )
    update_legend()
    fig.canvas.draw_idle()

# Function to toggle B-field visibility and button state
def show_b_field():
    is_visible = not b_line1.get_visible()
    b_line1.set_visible(is_visible)
    b_line2.set_visible(is_visible)
    # Update button appearance with light gray active state
    if is_visible:
        b_field_button.config(
            bg=BUTTON_ACTIVE_BG,
            fg=DARKER_BG,  # Dark text on light background when active
            relief='sunken'
        )
    else:
        b_field_button.config(
            bg=BUTTON_BG,
            fg=TEXT_COLOR,  # White text on dark background when inactive
            relief='flat'
        )
    update_legend()
    fig.canvas.draw_idle()

# Function to update the legend based on line visibility
def update_legend():
    # Remove existing legend
    if ax.get_legend():
        ax.get_legend().remove()
    
    # Create lists for visible lines and their labels
    lines = []
    labels = []
    
    # Add E-field lines if visible
    if e_line1.get_visible():
        lines.extend([e_line1, e_line2])
        labels.extend(['E-field (air)', 'E-field (Lossy Dielectric)'])
    
    # Add B-field lines if visible
    if b_line1.get_visible():
        lines.extend([b_line1, b_line2])
        labels.extend(['B-field (air)', 'B-field (Lossy Dielectric)'])
    
    # Always include these lines in the legend
    lines.extend([attenuation_line, skin_depth_line, boundary_line])
    labels.extend(['Attenuated Amplitude', 'Skin Depth', 'Boundary'])
    
    # Create new legend if there are lines to show
    if lines:
        

        ax.legend(lines, labels, loc='upper right')

    # Update the canvas
    fig.canvas.draw_idle()


    # Force update the plot
    
# Create buttons to show E-field and B-field
e_field_button = create_custom_button(control_frame, "Show E-field", show_e_field)
e_field_button.grid(row=9, column=0, padx=(20, 5), pady=10, sticky="ew")
e_field_button.config(bg=BUTTON_ACTIVE_BG, fg=DARKER_BG, relief='sunken')


b_field_button = create_custom_button(control_frame, "Show B-field", show_b_field)
b_field_button.grid(row=9, column=2, padx=5, pady=10, sticky="ew")
b_field_button.config(bg=BUTTON_ACTIVE_BG, fg=DARKER_BG, relief='sunken')

# Add 3D plot button
def show_3d_plot():
    # Pause 2D animation
    anim.event_source.stop()
    pause_button.config(text='Start')
    
    # Check if window already exists and destroy it if it does
    if hasattr(show_3d_plot, 'window') and show_3d_plot.window.winfo_exists():
        # Stop animation if it exists
        if hasattr(show_3d_plot, 'anim_3d') and show_3d_plot.anim_3d and show_3d_plot.anim_3d.event_source:
            show_3d_plot.anim_3d.event_source.stop()
        show_3d_plot.window.destroy()
    
    # Create new window for 3D plot
    show_3d_plot.window = tk.Toplevel(root)
    plot_window = show_3d_plot.window
    plot_window.title("3D Electromagnetic Wave Visualization")
    plot_window.attributes('-topmost', True)
    
    # Store figure and axis references
    show_3d_plot.fig_3d = plt.figure(figsize=(10, 8))
    show_3d_plot.ax_3d = show_3d_plot.fig_3d.add_subplot(111, projection='3d')
    
    # Create canvas first
    show_3d_plot.canvas_3d = FigureCanvasTkAgg(show_3d_plot.fig_3d, master=plot_window)
    show_3d_plot.canvas_3d.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Now do the initial plot setup
    update_3d_plot()
    
    def on_close():
        if hasattr(show_3d_plot, 'anim_3d') and show_3d_plot.anim_3d and show_3d_plot.anim_3d.event_source:
            show_3d_plot.anim_3d.event_source.stop()
        plot_window.destroy()
        # Resume 2D animation when 3D window is closed
        anim.event_source.start()
        pause_button.config(text='Pause')
    
    plot_window.protocol("WM_DELETE_WINDOW", on_close)

def update_3d_plot():
    if not (hasattr(show_3d_plot, 'window') and show_3d_plot.window.winfo_exists()):
        return
        
    ax_3d = show_3d_plot.ax_3d
    ax_3d.clear()  # Clear existing plot
    
    # Get current wave parameters
    params = calculate_wave_params()
    if params is None or None in params:
        return
    
    omega, beta, alpha, epsilon_complex, ft, skin_depth, v_p, eta = params
    beta_medium1 = np.sqrt(8.854e-12 * 4 * np.pi * 1e-7) * omega
    eta_medium1 = 376.73
    
    # Create boundary plane
    xx, zz = np.meshgrid(np.linspace(-3, 3, 10), np.linspace(-3, 3, 10))
    yy = np.ones_like(xx)
    ax_3d.plot_surface(yy, xx, zz, alpha=0.3, color='gray', 
                      edgecolor='white', linewidth=0.5)
    
    # Create static elements
    att_x = np.linspace(1, 5, 100)
    att_amp = amplitude * np.exp(-alpha * (att_x - 1))
    ax_3d.plot(att_x, np.zeros_like(att_x), att_amp, 'magenta', 
              label='Attenuated Amplitude', linestyle='--', linewidth=2)
    
    if not np.isinf(skin_depth):
        sd_x = np.array([1 + skin_depth, 1 + skin_depth])
        sd_y = np.array([-1.5, 1.5])
        sd_z = np.array([-1.5, 1.5])
        ax_3d.plot(sd_x, sd_y, sd_z, 'yellow', linestyle='--', 
                  label='Skin Depth', linewidth=2)
    
    x1 = np.linspace(0, 1, 100)
    x2 = np.linspace(1, 5, 100)
    
    # Initialize lines with empty data
    show_3d_plot.e_line1_3d, = ax_3d.plot([], [], [], color='cyan', label='E-field (Air)', linewidth=2)
    show_3d_plot.e_line2_3d, = ax_3d.plot([], [], [], color='orange', label='E-field (Lossy Dielectric)', linewidth=2)
    show_3d_plot.b_line1_3d, = ax_3d.plot([], [], [], color='green', label='B-field (Air)', linewidth=2)
    show_3d_plot.b_line2_3d, = ax_3d.plot([], [], [], color='red', label='B-field (Lossy Dielectric)', linewidth=2)
    
    # Set initial visibility based on 2D plot
    show_3d_plot.e_line1_3d.set_visible(e_line1.get_visible())
    show_3d_plot.e_line2_3d.set_visible(e_line2.get_visible())
    show_3d_plot.b_line1_3d.set_visible(b_line1.get_visible())
    show_3d_plot.b_line2_3d.set_visible(b_line2.get_visible())

    def update_3d(frame):
        time = frame *3e-9 # Remove the multiplication factor to make animation smoother
        
        # Calculate wave values for both E and B fields
        z1 = amplitude * np.cos(omega * time - beta_medium1 * (x1 - 1))
        phase = omega * time - beta * (x2 - 1)
        attenuated_amplitude = amplitude * np.exp(-alpha * (x2 - 1))
        z2 = attenuated_amplitude * np.cos(phase)
        
        y1 = 40 * amplitude * np.cos(omega * time - beta_medium1 * (x1 - 1)) / eta_medium1
        k1 = 1/eta
        y2 = 40 * (attenuated_amplitude * np.cos(phase)*k1.real + attenuated_amplitude * np.sin(phase)*k1.imag)
        
        # Update E-field lines if visible
        show_3d_plot.e_line1_3d.set_data(x1, np.zeros_like(x1))
        show_3d_plot.e_line1_3d.set_3d_properties(z1)
        show_3d_plot.e_line2_3d.set_data(x2, np.zeros_like(x2))
        show_3d_plot.e_line2_3d.set_3d_properties(z2)
        
        # Update B-field lines if visible
        show_3d_plot.b_line1_3d.set_data(x1, y1)
        show_3d_plot.b_line1_3d.set_3d_properties(np.zeros_like(x1))
        show_3d_plot.b_line2_3d.set_data(x2, y2)
        show_3d_plot.b_line2_3d.set_3d_properties(np.zeros_like(x2))
        
        return [show_3d_plot.e_line1_3d, show_3d_plot.e_line2_3d, 
                show_3d_plot.b_line1_3d, show_3d_plot.b_line2_3d]
    
    # Set up the plot appearance
    ax_3d.set_xlabel('X (Distance)')
    ax_3d.set_ylabel('Y (B-field)')
    ax_3d.set_zlabel('Z (E-field)')
    ax_3d.set_title(f'3D Electromagnetic Wave (f={format_frequency(freq)})')
    
    ax_3d.set_box_aspect([4, 2, 2])
    ax_3d.view_init(elev=30, azim=-120)
    ax_3d.set_xlim(0, 5)
    ax_3d.set_ylim(-3, 3)
    ax_3d.set_zlim(-3, 3)
    ax_3d.grid(True, linestyle='--', alpha=0.3)
    ax_3d.legend(loc='upper right')
    
    # Stop existing animation if it exists
    if hasattr(show_3d_plot, 'anim_3d') and show_3d_plot.anim_3d is not None:
        if hasattr(show_3d_plot.anim_3d, 'event_source') and show_3d_plot.anim_3d.event_source is not None:
            show_3d_plot.anim_3d.event_source.stop()
    
    # Create new animation
    show_3d_plot.anim_3d = FuncAnimation(
        show_3d_plot.fig_3d,
        update_3d,
        frames=np.linspace(0, 2*np.pi, 100),  # Reduced number of frames
        interval=20,  # Shorter interval for smoother animation
        blit=True,
        repeat=True  # Ensure continuous looping
    )
    
    
    if hasattr(show_3d_plot, 'canvas_3d'):
        show_3d_plot.canvas_3d.draw()

# Update the button creation 
plot_3d_button = create_custom_button(control_frame, "Show 3D Plot", show_3d_plot)
plot_3d_button.grid(row=9, column=1, pady=10, sticky="ew")

# Create a canvas and scrollbar for scrolling
value_canvas = tk.Canvas(control_frame, bg=DARKER_BG, highlightthickness=0)
value_canvas.grid(row=10, column=0, columnspan=3, pady=(20,10), sticky="nsew")  # Reduced bottom padding


# Add scrollbar
value_scrollbar = ttk.Scrollbar(control_frame, orient="vertical", command=value_canvas.yview)
value_scrollbar.grid(row=10, column=3, sticky="ns")

# Configure canvas
value_canvas.configure(yscrollcommand=value_scrollbar.set)

# Create main frame for values inside canvas
value_frame = tk.Frame(value_canvas, bg=DARKER_BG)
value_canvas.create_window((0, 0), window=value_frame, anchor="nw")

# Modify create_value_display to add more spacing between sections
def create_value_display(row, name):
    name_labels[name] = tk.Label(value_frame, text=f"{name}:", bg=DARKER_BG, fg=TEXT_COLOR, anchor="e", width=20)
    name_labels[name].grid(row=row, column=0, padx=(0,10), pady=2, sticky="e")
    
    value_labels[name] = tk.Label(value_frame, text="", bg=DARKER_BG, fg=ACCENT_COLOR, anchor="w", width=40)
    value_labels[name].grid(row=row, column=1, padx=(10,0), pady=2, sticky="w")

# Add function to update scroll region
def update_scroll_region(event=None):
    value_canvas.configure(scrollregion=value_canvas.bbox("all"))
    
# Bind the update function to the frame
value_frame.bind("<Configure>", update_scroll_region)

# Set a fixed height for the canvas
value_canvas.configure(height=2)  # Adjust this value as needed

# Configure grid weights for the control frame
control_frame.grid_rowconfigure(10, weight=1)
control_frame.grid_columnconfigure(0, weight=1)

# Create labels for names and values
name_labels = {}
value_labels = {}
create_value_display(0, "B-field Magnitude")
create_value_display(1, "Transition Frequency")
create_value_display(2, "Behavior")
create_value_display(3, "Skin Depth")
create_value_display(4, "Phase Velocity")

other_params_label = tk.Label(
    value_frame,
    text="Other Parameters",
    bg=DARKER_BG,
    fg=TEXT_COLOR,
    font=SUBHEADING_FONT
)
other_params_label.grid(row=5, column=0, columnspan=2, pady=15, sticky="ew")  # Moved down one row

# Shift all other parameters down by one row
create_value_display(6, "Complex ε")
create_value_display(7, "Wavelength(λ)")
create_value_display(8, "Intrinsic Impedance(η)")
create_value_display(9, "Propagation constant(γ)")
create_value_display(10, "Attenuation constant(α)")
create_value_display(11, "Phase constant(β)")
create_value_display(12, "E-B Phase Difference")

# Add smooth scrolling functionality
class SmoothScroll:
    def __init__(self, canvas):
        self.canvas = canvas
        self.target_y = 0.0
        self.current_y = 0.0
        self.smooth_factor = 0.25  # Increased from 0.15 for faster response
        self.is_scrolling = False
        
    def start_scroll(self):
        if not self.is_scrolling:
            self.is_scrolling = True
            self.scroll_loop()
    
    def scroll_loop(self):
        if abs(self.current_y - self.target_y) > 0.01:
            # Smoothly interpolate between current and target position
            self.current_y += (self.target_y - self.current_y) * self.smooth_factor
            self.canvas.yview_moveto(self.current_y)
            self.canvas.after(8, self.scroll_loop)  # Decreased from 10ms for more frequent updates
        else:
            self.is_scrolling = False
    
    def on_mousewheel(self, event):
        # Get the current scroll position
        current_pos = self.canvas.yview()[0]
        
        # Calculate scroll amount based on delta
        scroll_amount = event.delta / 120 * 0.12  # Increased from 0.08 for faster scrolling
        
        # Update target position with bounds checking
        self.target_y = max(0, min(1, current_pos - scroll_amount))
        
        # Start the smooth scroll animation
        self.start_scroll()

# Create smooth scroll handler
smooth_scroll = SmoothScroll(value_canvas)

# Bind mouse wheel to smooth scroll
value_canvas.bind_all("<MouseWheel>", smooth_scroll.on_mousewheel)

# Update all wave parameters and displays
def update_params(*args):
    global freq, amplitude, epsilon_r, sigma, mu_r
    
    # Get current values from sliders
    freq = freq_slider.get()
    amplitude = float(amp_value.get())
    epsilon_r = epsilon_slider.get()
    sigma = float(sigma_value.get())
    mu_r = mu_slider.get()
    
    # Update plot title and labels
    ax.set_title(f"Electromagnetic Wave in Lossy Dielectric (f={format_frequency(freq)})", 
                color=TEXT_COLOR)
    ax.set_xlabel("Distance (m)", color=TEXT_COLOR)
    ax.set_ylabel("Field Amplitude", color=TEXT_COLOR)
    ax.tick_params(colors=TEXT_COLOR)
    
    # Update 3D visualization if active
    if hasattr(show_3d_plot, 'window') and show_3d_plot.window.winfo_exists():
        update_3d_plot()
    
    fig.canvas.draw_idle()
    update_param_display()

# Make sure the sliders are bound to update_params
freq_slider.config(command=update_params)
amp_slider.config(command=update_params)
epsilon_slider.config(command=update_params)
sigma_slider.config(command=update_params)
mu_slider.config(command=update_params)

# Function to update parameter display
def update_param_display():
    # Update slider value displays
    freq_value.delete(0, tk.END)
    freq_value.insert(0, format_frequency(freq))
    amp_value.delete(0, tk.END)
    amp_value.insert(0, f"{amplitude:.2f}")
    epsilon_value.delete(0, tk.END)
    epsilon_value.insert(0, f"{epsilon_r:.2f}")
    sigma_value.delete(0, tk.END)
    sigma_value.insert(0, f"{sigma:.5f}")
    mu_value.delete(0, tk.END)
    mu_value.insert(0, f"{mu_r:.2f}")
    
    # Calculate and display new parameters
    omega, beta, alpha, epsilon_complex, ft, skin_depth, v_p,eta = calculate_wave_params()
    
    # Calculate complex propagation constant (gamma)
    gamma = alpha + 1j * beta
    wavelength = 2 * np.pi / beta

    k1=1/eta
    # Calculate phase difference
    
    phase_difference = np.arctan2(k1.imag, k1.real)
    phase_difference_degrees = np.degrees(phase_difference)

    
    b_magnitude = amplitude / abs(eta)
    b_magnitude_text = format_scientific(b_magnitude, 3) + " T"
    
    
    # Update B-field magnitude display
    value_labels["B-field Magnitude"].config(text=b_magnitude_text + " (Increased 40 times for \nbetter visibility)")
    
    # Update all parameter displays
    value_labels["Transition Frequency"].config(text=format_frequency(ft))
    value_labels["Behavior"].config(text='Dielectric' if freq > ft else 'Conductor')
    value_labels["Skin Depth"].config(text="∞ m" if np.isinf(skin_depth) else format_distance(skin_depth, 3))
    value_labels["Phase Velocity"].config(text="∞ m/s" if np.isinf(v_p) else format_scientific(v_p, 3) + " m/s")
    value_labels["Complex ε"].config(text=format_scientific(epsilon_complex, 3))
    value_labels["Propagation constant(γ)"].config(text=format_scientific(gamma, 3) + " m⁻¹")
    value_labels["Attenuation constant(α)"].config(text=format_scientific(alpha, 3) + " Np/m")
    value_labels["Phase constant(β)"].config(text=format_scientific(beta, 3) + " rad/m")
    value_labels["Wavelength(λ)"].config(text=format_distance(wavelength, 3))
    value_labels["Intrinsic Impedance(η)"].config(text=f"{eta:.2f}" + " Ω")
    value_labels["E-B Phase Difference"].config( text=f"{phase_difference_degrees:.2f}° ({phase_difference:.2f} rad)")

    

    
   
    
# Initial parameter display
update_param_display()

# Configure grid weights
main_frame.grid_columnconfigure(0, weight=3)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

# Start the animation

anim.event_source.start()
def on_closing():
    root.quit()
    root.destroy()
root.protocol("WM_DELETE_WINDOW", on_closing)
# Start the Tkinter main loop
root.mainloop()