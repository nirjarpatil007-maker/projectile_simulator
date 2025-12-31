import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import math


class ProjectileSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Projectile Motion Simulator")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f4f8")

        # Animation variables
        self.animation_running = False
        self.animation_id = None
        self.current_time = 0

        self.setup_ui()

    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(
            main_frame,
            text="🎯 Projectile Motion Simulator",
            font=("Helvetica", 28, "bold"),
            bg="#f0f4f8",
            fg="#1e3a8a"
        )
        title_label.pack(pady=(0, 20))

        # Content container
        content_frame = tk.Frame(main_frame, bg="#f0f4f8")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel - Input controls
        left_panel = tk.Frame(content_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=0)
        left_panel.configure(width=350)
        left_panel.pack_propagate(False)

        self.create_input_section(left_panel)

        # Right panel - Graph and results
        right_panel = tk.Frame(content_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=0)

        self.create_graph_section(right_panel)

    def create_input_section(self, parent):
        # Input section header
        input_header = tk.Label(
            parent,
            text="Input Parameters",
            font=("Helvetica", 18, "bold"),
            bg="#ffffff",
            fg="#1e3a8a"
        )
        input_header.pack(pady=(20, 15))

        # Input fields container
        inputs_container = tk.Frame(parent, bg="#ffffff")
        inputs_container.pack(padx=20, pady=10, fill=tk.BOTH)

        # Velocity input
        self.create_input_field(
            inputs_container,
            "Initial Velocity (m/s):",
            "velocity",
            "50"
        )

        # Angle input
        self.create_input_field(
            inputs_container,
            "Angle of Projection (°):",
            "angle",
            "45"
        )

        # Gravity input
        self.create_input_field(
            inputs_container,
            "Gravitational Acceleration (m/s²):",
            "gravity",
            "9.8"
        )

        # Buttons container
        buttons_frame = tk.Frame(parent, bg="#ffffff")
        buttons_frame.pack(pady=20)

        # Calculate button
        calc_button = tk.Button(
            buttons_frame,
            text="Calculate & Simulate",
            command=self.calculate_and_simulate,
            font=("Helvetica", 12, "bold"),
            bg="#3b82f6",
            fg="white",
            activebackground="#2563eb",
            activeforeground="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        calc_button.pack(pady=5)

        # Reset button
        reset_button = tk.Button(
            buttons_frame,
            text="Reset",
            command=self.reset_simulation,
            font=("Helvetica", 12),
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10
        )
        reset_button.pack(pady=5)

        # Results section
        results_header = tk.Label(
            parent,
            text="Results",
            font=("Helvetica", 18, "bold"),
            bg="#ffffff",
            fg="#1e3a8a"
        )
        results_header.pack(pady=(20, 15))

        # Results container
        self.results_container = tk.Frame(parent, bg="#f8fafc", relief=tk.GROOVE, bd=2)
        self.results_container.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Initial results text
        initial_text = tk.Label(
            self.results_container,
            text="Enter parameters and\nclick Calculate",
            font=("Helvetica", 11),
            bg="#f8fafc",
            fg="#64748b",
            justify=tk.CENTER
        )
        initial_text.pack(expand=True)

    def create_input_field(self, parent, label_text, var_name, default_value):
        field_frame = tk.Frame(parent, bg="#ffffff")
        field_frame.pack(pady=10, fill=tk.X)

        label = tk.Label(
            field_frame,
            text=label_text,
            font=("Helvetica", 11),
            bg="#ffffff",
            fg="#334155"
        )
        label.pack(anchor=tk.W, pady=(0, 5))

        entry = tk.Entry(
            field_frame,
            font=("Helvetica", 12),
            relief=tk.SOLID,
            bd=1,
            highlightthickness=2,
            highlightbackground="#e2e8f0",
            highlightcolor="#3b82f6"
        )
        entry.insert(0, default_value)
        entry.pack(fill=tk.X, ipady=5)

        setattr(self, f"{var_name}_entry", entry)

    def create_graph_section(self, parent):
        # Graph header
        graph_header = tk.Label(
            parent,
            text="Projectile Motion Trajectory",
            font=("Helvetica", 18, "bold"),
            bg="#ffffff",
            fg="#1e3a8a"
        )
        graph_header.pack(pady=(20, 10))

        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 6), dpi=100, facecolor='white')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("Range (m)", fontsize=12, fontweight='bold')
        self.ax.set_ylabel("Height (m)", fontsize=12, fontweight='bold')
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_facecolor('#f8fafc')

        # Canvas for matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    def calculate_and_simulate(self):
        try:
            # Get input values
            velocity = float(self.velocity_entry.get())
            angle = float(self.angle_entry.get())
            gravity = float(self.gravity_entry.get())

            # Validate inputs
            if velocity <= 0:
                messagebox.showerror("Error", "Velocity must be positive!")
                return
            if angle <= 0 or angle >= 90:
                messagebox.showerror("Error", "Angle must be between 0 and 90 degrees!")
                return
            if gravity <= 0:
                messagebox.showerror("Error", "Gravity must be positive!")
                return

            # Convert angle to radians
            angle_rad = math.radians(angle)

            # Calculate projectile motion parameters
            time_of_flight = (2 * velocity * math.sin(angle_rad)) / gravity
            max_height = (velocity ** 2 * math.sin(angle_rad) ** 2) / (2 * gravity)
            range_distance = (velocity ** 2 * math.sin(2 * angle_rad)) / gravity

            # Store for animation
            self.velocity = velocity
            self.angle_rad = angle_rad
            self.gravity = gravity
            self.time_of_flight = time_of_flight

            # Display results
            self.display_results(max_height, time_of_flight, range_distance)

            # Start animation
            self.animate_projectile()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values!")

    def display_results(self, max_height, time_of_flight, range_distance):
        # Clear previous results
        for widget in self.results_container.winfo_children():
            widget.destroy()

        results_data = [
            ("Maximum Height:", f"{max_height:.2f} m", "#10b981"),
            ("Time of Flight:", f"{time_of_flight:.2f} s", "#f59e0b"),
            ("Range:", f"{range_distance:.2f} m", "#8b5cf6"),
        ]

        for label_text, value_text, color in results_data:
            result_frame = tk.Frame(self.results_container, bg="#ffffff", relief=tk.SOLID, bd=1)
            result_frame.pack(pady=8, padx=15, fill=tk.X)

            label = tk.Label(
                result_frame,
                text=label_text,
                font=("Helvetica", 11, "bold"),
                bg="#ffffff",
                fg="#334155"
            )
            label.pack(anchor=tk.W, padx=10, pady=(8, 2))

            value = tk.Label(
                result_frame,
                text=value_text,
                font=("Helvetica", 16, "bold"),
                bg="#ffffff",
                fg=color
            )
            value.pack(anchor=tk.W, padx=10, pady=(2, 8))

    def animate_projectile(self):
        # Stop any existing animation
        if self.animation_id:
            self.root.after_cancel(self.animation_id)

        self.current_time = 0
        self.animation_running = True

        # Clear previous plot
        self.ax.clear()
        self.ax.set_xlabel("Range (m)", fontsize=12, fontweight='bold')
        self.ax.set_ylabel("Height (m)", fontsize=12, fontweight='bold')
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_facecolor('#f8fafc')

        # Calculate full trajectory for background
        t_full = np.linspace(0, self.time_of_flight, 100)
        x_full = self.velocity * np.cos(self.angle_rad) * t_full
        y_full = self.velocity * np.sin(self.angle_rad) * t_full - 0.5 * self.gravity * t_full ** 2

        # Plot full trajectory in light color
        self.ax.plot(x_full, y_full, 'b--', alpha=0.3, linewidth=1, label='Full Trajectory')

        # Initialize animated line and point
        self.animated_line, = self.ax.plot([], [], 'b-', linewidth=2.5, label='Current Path')
        self.animated_point, = self.ax.plot([], [], 'ro', markersize=10, label='Projectile')

        self.ax.legend(loc='upper right', fontsize=10)

        # Start animation loop
        self.update_animation()

    def update_animation(self):
        if not self.animation_running or self.current_time > self.time_of_flight:
            self.animation_running = False
            return

        # Calculate current position
        t_current = np.linspace(0, self.current_time, 50)
        x_current = self.velocity * np.cos(self.angle_rad) * t_current
        y_current = self.velocity * np.sin(self.angle_rad) * t_current - 0.5 * self.gravity * t_current ** 2

        # Update animated elements
        self.animated_line.set_data(x_current, y_current)
        if len(x_current) > 0:
            self.animated_point.set_data([x_current[-1]], [y_current[-1]])

        self.canvas.draw()

        # Increment time
        self.current_time += self.time_of_flight / 50

        # Schedule next update
        self.animation_id = self.root.after(50, self.update_animation)

    def reset_simulation(self):
        # Stop animation
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
        self.animation_running = False

        # Reset input fields
        self.velocity_entry.delete(0, tk.END)
        self.velocity_entry.insert(0, "50")

        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(0, "45")

        self.gravity_entry.delete(0, tk.END)
        self.gravity_entry.insert(0, "9.8")

        # Clear results
        for widget in self.results_container.winfo_children():
            widget.destroy()

        initial_text = tk.Label(
            self.results_container,
            text="Enter parameters and\nclick Calculate",
            font=("Helvetica", 11),
            bg="#f8fafc",
            fg="#64748b",
            justify=tk.CENTER
        )
        initial_text.pack(expand=True)

        # Clear graph
        self.ax.clear()
        self.ax.set_xlabel("Range (m)", fontsize=12, fontweight='bold')
        self.ax.set_ylabel("Height (m)", fontsize=12, fontweight='bold')
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.set_facecolor('#f8fafc')
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = ProjectileSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
