import cv2
import numpy as np
import pygame
import time
import os
import math
from datetime import datetime
from tkinter import filedialog
import tkinter as tk
from pygame import gfxdraw
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import random

# Initialize Pygame
pygame.init()

# Configure display settings
WINDOW_WIDTH = 1150  # Increased width to prevent overlap
WINDOW_HEIGHT = 800  # Further increased height to prevent overlap
DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PCB Thermal Anomaly Detection")

# Load and set application icon
icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'thermal_icon.png')
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

# Configure colors with professional palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 53, 69)
GREEN = (40, 167, 69)
BLUE = (0, 123, 255)
DARK_BLUE = (0, 52, 102)
LIGHT_BLUE = (240, 248, 255)
NAVY = (0/255, 31/255, 63/255)
GOLD = (255, 193, 7)
TABLE_BG = (20, 20, 40)  # Darker background for table
TABLE_BORDER = (100, 149, 237)  # Cornflower blue border

# Configure storage settings
SAVE_DIR = "anomaly_captures"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
def show_welcome_animation():
    # Create welcome screen surface
    welcome_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    welcome_font = pygame.font.Font(None, 64)
    creator_font = pygame.font.Font(None, 32)
    
    # Load creator photo
    photo_path = os.path.join(os.path.dirname(__file__), 'assets', 'creator_photo.jpg')
    try:
        creator_photo = pygame.image.load(photo_path)
        creator_photo = pygame.transform.scale(creator_photo, (150, 150))  # Adjust size as needed
    except:
        creator_photo = None
    
    # Animation parameters
    alpha = 0
    text_pos_y = WINDOW_HEIGHT
    done = False
    clock = pygame.time.Clock()
    
    while not done:
        welcome_surface.fill(NAVY)
        
        # Animate text position and opacity
        if text_pos_y > WINDOW_HEIGHT/2 - 50:
            text_pos_y -= 2
        if alpha < 255:
            alpha += 3
            
        # Render welcome text with current alpha
        welcome_text = welcome_font.render("Welcome to", True, WHITE)
        system_text = welcome_font.render("PCB Anomaly Detection System", True, WHITE)
        creator_text = creator_font.render("Created by Manish Dhatrak", True, WHITE)
        
        # Set text transparency
        welcome_text.set_alpha(alpha)
        system_text.set_alpha(alpha)
        creator_text.set_alpha(alpha)
        
        # Calculate text positions
        welcome_rect = welcome_text.get_rect(center=(WINDOW_WIDTH/2, text_pos_y))
        system_rect = system_text.get_rect(center=(WINDOW_WIDTH/2, text_pos_y + 70))
        
        # Draw texts
        welcome_surface.blit(welcome_text, welcome_rect)
        welcome_surface.blit(system_text, system_rect)
        
        # Draw creator photo if available
        if creator_photo:
            photo_rect = creator_photo.get_rect(center=(WINDOW_WIDTH/2, text_pos_y + 200))
            creator_photo.set_alpha(alpha)
            welcome_surface.blit(creator_photo, photo_rect)
            
        # Draw creator text below photo
        creator_rect = creator_text.get_rect(center=(WINDOW_WIDTH/2, text_pos_y + 300))
        welcome_surface.blit(creator_text, creator_rect)
        
        # Draw loading animation below creator text
        time_val = pygame.time.get_ticks()
        for i in range(8):
            angle = time_val * 0.001 + i * 0.8
            x = WINDOW_WIDTH/2 + math.cos(angle) * 30
            y = text_pos_y + 350 + math.sin(angle) * 30
            pygame.draw.circle(welcome_surface, BLUE, (int(x), int(y)), 5)
        
        DISPLAY.blit(welcome_surface, (0,0))
        pygame.display.flip()
        
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                done = True
                
        if alpha >= 255 and text_pos_y <= WINDOW_HEIGHT/2 - 50:
            time.sleep(1)
            done = True
            
        clock.tick(60)
    
    # Fade out
    for i in range(255, 0, -5):
        welcome_surface.set_alpha(i)
        DISPLAY.fill(NAVY)
        DISPLAY.blit(welcome_surface, (0,0))
        pygame.display.flip()
        clock.tick(60)

# Sparkle class for animation
class Sparkle:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(-50, 0)
        self.speed = random.uniform(2, 5)
        self.size = random.randint(2, 4)
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        
    def update(self):
        self.y += self.speed
        if self.y > WINDOW_HEIGHT:
            self.y = random.randint(-50, 0)
            self.x = random.randint(0, WINDOW_WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

class ModernButton:
    def __init__(self, x, y, width, height, text, color, icon=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.icon = icon
        self.font = pygame.font.Font(None, 32)
        self.hover = False
        self.active = False
        
    def draw(self, surface):
        # Create modern gradient effect
        if self.hover:
            color = tuple(min(c + 20, 255) for c in self.color)
        else:
            color = self.color
            
        # Draw button with smooth corners
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        
        # Add glossy effect
        highlight = pygame.Surface((self.rect.width, self.rect.height//2), pygame.SRCALPHA)
        pygame.draw.rect(highlight, (255, 255, 255, 30), highlight.get_rect(), border_radius=15)
        surface.blit(highlight, (self.rect.x, self.rect.y))
        
        # Draw icon if provided
        if self.icon:
            icon_rect = self.icon.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
            surface.blit(self.icon, icon_rect)
            
        # Draw text with shadow
        text_surface = self.font.render(self.text, True, WHITE)
        text_shadow = self.font.render(self.text, True, (0, 0, 0, 128))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
        surface.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
        
    def update_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)

class PCBAnomaly:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.temp_threshold = 50
        self.font = pygame.font.Font(None, 24)
        self.analyzing = False
        self.hot_spots_count = 0
        self.max_temp = 0
        self.current_image = None
        self.results_window = False
        self.recording = False
        self.accuracy_data = []
        self.show_graph = False
        self.thermal_intensity_data = []  # New data for second graph
        self.in_graph_view = False  # New flag for graph view
        self.sparkles = [Sparkle() for _ in range(50)]  # Create sparkles
        self.parameters = {
            'Threshold': self.temp_threshold,
            'Hot Spots': self.hot_spots_count,
            'Max Temp': self.max_temp,
            'Status': 'Inactive'
        }
        self.outcomes = {
            'Anomalies': 0,
            'Accuracy': 0,
            'Intensity': 0,
            'Risk Level': 'Low'
        }
        
    def detect_pcb(self, frame):
        return True
        
    def process_frame(self, frame):
        if not self.detect_pcb(frame):
            return frame, 0, 0
            
        # Convert to HSV to detect orange-red thermal regions
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Define orange-red color range
        lower_thermal = np.array([0, 120, 70])
        upper_thermal = np.array([20, 255, 255])
        
        # Create mask for thermal regions
        thermal_mask = cv2.inRange(hsv, lower_thermal, upper_thermal)
        
        # Find contours of thermal regions
        contours, _ = cv2.findContours(thermal_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create black background
        result = np.zeros_like(frame)
        
        # Draw only the thermal regions with enhanced visualization
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            roi = frame[y:y+h, x:x+w]
            result[y:y+h, x:x+w] = roi
            
            # Add glowing effect around thermal regions
            cv2.rectangle(result, (x-2, y-2), (x+w+2, y+h+2), (0, 255, 255), 2)
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)
            
        # Save frame only if recording is active and thermal regions detected
        if self.recording and len(contours) > 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"thermal_{timestamp}.jpg"
            cv2.imwrite(os.path.join(SAVE_DIR, filename), result)
            
        self.hot_spots_count = len(contours)
        self.max_temp = np.max(thermal_mask)
        
        # Calculate and store accuracy data
        accuracy = (len(contours) / max(1, np.sum(thermal_mask > 0))) * 100
        self.accuracy_data.append(min(100, accuracy))  # Cap at 100%
        if len(self.accuracy_data) > 50:  # Keep last 50 points
            self.accuracy_data.pop(0)
            
        # Calculate and store thermal intensity data
        thermal_intensity = np.mean(thermal_mask) / 255.0 * 100  # Normalize to percentage
        self.thermal_intensity_data.append(min(100, thermal_intensity))  # Cap at 100%
        if len(self.thermal_intensity_data) > 50:  # Keep last 50 points
            self.thermal_intensity_data.pop(0)
            
        # Update parameters and outcomes with accurate values
        self.parameters.update({
            'Threshold': f"{self.temp_threshold}°C",
            'Hot Spots': str(self.hot_spots_count),
            'Max Temp': f"{round(self.max_temp/255.0 * 100, 1)}°C",
            'Status': 'Active' if self.recording else 'Inactive'
        })
        
        self.outcomes.update({
            'Anomalies': str(len(contours)),
            'Accuracy': f"{round(min(100, accuracy), 1)}%",
            'Intensity': f"{round(min(100, thermal_intensity), 1)}%",
            'Risk Level': 'High' if thermal_intensity > 70 else 'Medium' if thermal_intensity > 40 else 'Low'
        })
        
        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result = np.rot90(result)
        result = pygame.surfarray.make_surface(result)
        return result, self.hot_spots_count, self.max_temp

    def get_frame(self):
        success, frame = self.camera.read()
        if success:
            processed_frame, _, _ = self.process_frame(frame)
            return processed_frame
        return None

    def analyze_image(self, image_path):
        frame = cv2.imread(image_path)
        if frame is not None:
            self.current_image = frame
            return self.process_frame(frame)
        return None, 0, 0
        
    def generate_accuracy_plot(self):
        # Create figure with adjusted size
        fig = plt.figure(figsize=(5, 3.5), facecolor=NAVY)
        ax = fig.add_subplot(111)
        
        # Plot data with improved visibility
        ax.plot(range(len(self.accuracy_data)), self.accuracy_data, 
                color='cyan', linewidth=2, marker='o', markersize=4)
        
        # Customize plot appearance
        ax.set_facecolor(NAVY)
        ax.set_title('Detection Accuracy Over Time', color='white', pad=10, fontsize=10)
        ax.set_xlabel('Time (frames)', color='white', fontsize=8)
        ax.set_ylabel('Accuracy %', color='white', fontsize=8)
        ax.tick_params(colors='white', labelsize=6)
        ax.grid(True, linestyle='--', alpha=0.3, color='white')
        
        # Set y-axis range from 0 to 100
        ax.set_ylim(0, 100)
        
        # Add padding to prevent cutoff
        plt.tight_layout(pad=1.5)
        
        # Convert plot to pygame surface
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        
        # Convert to pygame surface
        graph_surface = pygame.image.fromstring(raw_data, size, "RGB")
        plt.close(fig)
        
        return graph_surface
        
    def generate_thermal_intensity_plot(self):
        # Create figure with adjusted size
        fig = plt.figure(figsize=(5, 3.5), facecolor=NAVY)
        ax = fig.add_subplot(111)
        
        # Plot data with improved visibility
        ax.plot(range(len(self.thermal_intensity_data)), self.thermal_intensity_data,
                color='red', linewidth=2, marker='o', markersize=4)
        
        # Customize plot appearance
        ax.set_facecolor(NAVY)
        ax.set_title('Thermal Intensity Analysis', color='white', pad=10, fontsize=10)
        ax.set_xlabel('Time (frames)', color='white', fontsize=8)
        ax.set_ylabel('Intensity %', color='white', fontsize=8)
        ax.tick_params(colors='white', labelsize=6)
        ax.grid(True, linestyle='--', alpha=0.3, color='white')
        
        # Set y-axis range from 0 to 100
        ax.set_ylim(0, 100)
        
        # Add padding to prevent cutoff
        plt.tight_layout(pad=1.5)
        
        # Convert plot to pygame surface
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        
        # Convert to pygame surface
        graph_surface = pygame.image.fromstring(raw_data, size, "RGB")
        plt.close(fig)
        
        return graph_surface

def draw_modern_background(surface):
    # Create a more sophisticated gradient background
    for y in range(WINDOW_HEIGHT):
        progress = y / WINDOW_HEIGHT
        color = (
            int(DARK_BLUE[0] * (1-progress) + LIGHT_BLUE[0] * progress),
            int(DARK_BLUE[1] * (1-progress) + LIGHT_BLUE[1] * progress),
            int(DARK_BLUE[2] * (1-progress) + LIGHT_BLUE[2] * progress)
        )
        pygame.draw.line(surface, color, (0, y), (WINDOW_WIDTH, y))
        
    # Add subtle pattern overlay
    pattern = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for x in range(0, WINDOW_WIDTH, 20):
        for y in range(0, WINDOW_HEIGHT, 20):
            pygame.draw.circle(pattern, (255, 255, 255, 5), (x, y), 1)
    surface.blit(pattern, (0, 0))

def draw_header(surface):
    # Draw header background
    header_rect = pygame.Rect(0, 0, WINDOW_WIDTH, 80)
    pygame.draw.rect(surface, (0, 31, 63), header_rect)
    
    # Draw animated scanning lines
    scan_height = 60
    scan_y = 10 + (pygame.time.get_ticks() % 1000) / 1000 * scan_height
    for i in range(3):
        y = scan_y + i * 20
        if y < scan_height + 10:
            alpha = int(255 * (1 - abs(scan_height/2 - (y-10))/scan_height))
            line_surface = pygame.Surface((200, 2), pygame.SRCALPHA)
            line_surface.fill((0, 255, 255, alpha))
            surface.blit(line_surface, (WINDOW_WIDTH//2 - 150, y))

    # Draw pulsing circles
    circle_size = 30 + math.sin(pygame.time.get_ticks() / 500) * 10
    for i in range(3):
        alpha = int(255 * (1 - i/3))
        circle_surface = pygame.Surface((circle_size*2, circle_size*2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (*BLUE[:3], alpha), 
                         (circle_size, circle_size), circle_size-(i*5))
        surface.blit(circle_surface, 
                    (WINDOW_WIDTH//2 - circle_size + 150, 40 - circle_size))

    # Draw title text with glowing effect
    title_font = pygame.font.Font(None, 48)
    glow_amount = int(abs(math.sin(pygame.time.get_ticks() / 1000)) * 50)
    
    # Draw glow - ensure color values stay within valid range
    glow_color = (min(255, BLUE[0]+glow_amount), 
                 min(255, BLUE[1]+glow_amount),
                 min(255, BLUE[2]+glow_amount))
    glow_text = title_font.render("PCB Thermal Analysis System", True, glow_color)
    glow_rect = glow_text.get_rect(center=(WINDOW_WIDTH//2, 40))
    surface.blit(glow_text, glow_rect)
    
    # Draw main text
    title_text = "PCB Thermal Analysis System"
    title_surface = title_font.render(title_text, True, WHITE)
    title_rect = title_surface.get_rect(center=(WINDOW_WIDTH//2, 40))
    surface.blit(title_surface, title_rect)

def draw_footer(surface):
    # Draw footer background
    footer_rect = pygame.Rect(0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40)
    pygame.draw.rect(surface, (0, 31, 63), footer_rect)
    
    # Draw footer text
    footer_font = pygame.font.Font(None, 24)
    footer_text = "Created by Manish Dhatrak | PCB Anomaly Detection System | © 2024"
    footer_surface = footer_font.render(footer_text, True, WHITE)
    footer_rect = footer_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 20))
    surface.blit(footer_surface, footer_rect)

def draw_table(surface, data, title, x, y, width, height):
    # Draw table background
    pygame.draw.rect(surface, NAVY, (x, y, width, height))
    pygame.draw.rect(surface, WHITE, (x, y, width, height), 2)
    
    # Draw title with emoji
    title_font = pygame.font.Font(None, 32)
    if title == "Parameters":
        title_text = f"{title}"
    else:
        title_text = f"{title}"
    title_surface = title_font.render(title_text, True, WHITE)
    title_rect = title_surface.get_rect(center=(x + width//2, y + 20))
    surface.blit(title_surface, title_rect)
    
    # Draw table content
    font = pygame.font.Font(None, 24)
    row_height = (height - 50) // (len(data) + 1)
    col_width = width // 2
    
    # Draw headers
    pygame.draw.line(surface, WHITE, (x, y + 40), (x + width, y + 40))
    header_y = y + 45
    headers = ["Parameter", "Value"]
    for i, header in enumerate(headers):
        header_surface = font.render(header, True, WHITE)
        header_rect = header_surface.get_rect(center=(x + col_width * i + col_width//2, header_y))
        surface.blit(header_surface, header_rect)
    
    # Draw data rows
    start_y = y + 70
    for i, (key, value) in enumerate(data.items()):
        # Draw row background
        row_y = start_y + i * row_height
        if i % 2 == 0:
            pygame.draw.rect(surface, (0, 41, 73), (x + 2, row_y, width - 4, row_height))
        
        # Draw key
        key_surface = font.render(str(key), True, WHITE)
        key_rect = key_surface.get_rect(center=(x + col_width//2, row_y + row_height//2))
        surface.blit(key_surface, key_rect)
        
        # Draw value
        value_surface = font.render(str(value), True, WHITE)
        value_rect = value_surface.get_rect(center=(x + col_width + col_width//2, row_y + row_height//2))
        surface.blit(value_surface, value_rect)

def main():
    # Show welcome animation before starting main program
    show_welcome_animation()
    
    detector = PCBAnomaly()
    clock = pygame.time.Clock()
    root = tk.Tk()
    root.withdraw()
    
    # Calculate center positions for buttons with more spacing
    center_x = WINDOW_WIDTH // 2
    button_y = WINDOW_HEIGHT - 100
    button_spacing = 140  # Increased spacing between buttons
    
    # Create modern styled buttons with better spacing
    buttons = {
        'start_stop': ModernButton(center_x - 3*button_spacing, button_y, 120, 40, "Start/Stop", BLUE),
        'threshold_up': ModernButton(center_x - 2*button_spacing, button_y, 40, 40, "+", GREEN),
        'threshold_down': ModernButton(center_x - 2*button_spacing + 50, button_y, 40, 40, "-", RED),
        'upload': ModernButton(center_x - button_spacing, button_y, 120, 40, "Upload", (0, 31, 63)),
        'results': ModernButton(center_x, button_y, 120, 40, "Results", BLUE),
        'record': ModernButton(center_x + button_spacing, button_y, 120, 40, "Record", RED),
        'graph': ModernButton(center_x + 2*button_spacing, button_y, 120, 40, "Graph", GREEN),
        'back': ModernButton(50, 50, 100, 40, "Back", RED),  # Back button
        'exit': ModernButton(WINDOW_WIDTH - 150, 50, 100, 40, "Exit", RED)  # Exit button
    }
    
    # Create modern stats panel with increased size
    stats_panel = pygame.Surface((350, 220))
    stats_panel.set_alpha(200)
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons['exit'].is_clicked(mouse_pos):  # Handle exit button click
                    running = False
                elif detector.in_graph_view and buttons['back'].is_clicked(mouse_pos):
                    detector.in_graph_view = False
                elif not detector.in_graph_view:
                    if buttons['start_stop'].is_clicked(mouse_pos):
                        detector.analyzing = not detector.analyzing
                    elif buttons['threshold_up'].is_clicked(mouse_pos):
                        detector.temp_threshold = min(100, detector.temp_threshold + 5)
                    elif buttons['threshold_down'].is_clicked(mouse_pos):
                        detector.temp_threshold = max(0, detector.temp_threshold - 5)
                    elif buttons['upload'].is_clicked(mouse_pos):
                        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
                        if file_path:
                            detector.analyze_image(file_path)
                    elif buttons['results'].is_clicked(mouse_pos):
                        detector.results_window = not detector.results_window
                    elif buttons['record'].is_clicked(mouse_pos):
                        detector.recording = not detector.recording
                        buttons['record'].color = GREEN if detector.recording else RED
                    elif buttons['graph'].is_clicked(mouse_pos):
                        detector.in_graph_view = True
        
        # Draw modern background
        draw_modern_background(DISPLAY)
        
        # Draw header with symbol
        draw_header(DISPLAY)
        
        if detector.in_graph_view:
            # Draw both graphs in graph view with proper spacing
            if detector.recording or detector.current_image is not None:
                accuracy_graph = detector.generate_accuracy_plot()
                thermal_graph = detector.generate_thermal_intensity_plot()
                
                # Calculate positions for centered graphs with padding
                graph_padding = 40
                total_width = accuracy_graph.get_width() * 2 + graph_padding
                start_x = (WINDOW_WIDTH - total_width) // 2
                
                # Draw graphs side by side with proper spacing
                DISPLAY.blit(accuracy_graph, (start_x, 150))
                DISPLAY.blit(thermal_graph, (start_x + accuracy_graph.get_width() + graph_padding, 150))
                
                # Draw tables below graphs with increased spacing
                table_y = 550  # Increased vertical spacing
                table_height = 200
                draw_table(DISPLAY, detector.parameters, "Parameters", start_x, table_y, accuracy_graph.get_width(), table_height)
                draw_table(DISPLAY, detector.outcomes, "Outcomes", start_x + accuracy_graph.get_width() + graph_padding, table_y, thermal_graph.get_width(), table_height)
            
            # Draw back button
            buttons['back'].draw(DISPLAY)
            
            # Update and draw sparkles
            for sparkle in detector.sparkles:
                sparkle.update()
                sparkle.draw(DISPLAY)
            
        else:
            # Update button hover states
            for button in buttons.values():
                if button != buttons['back']:
                    button.update_hover(mouse_pos)
            
            # Draw main content frame with modern border
            if detector.analyzing and not detector.results_window:
                frame = detector.get_frame()
                if frame is not None:
                    frame = pygame.transform.scale(frame, (640, 480))
                    pygame.draw.rect(DISPLAY, WHITE, (WINDOW_WIDTH//2 - 325, 100, 650, 490), 3)
                    DISPLAY.blit(frame, (WINDOW_WIDTH//2 - 320, 105))
            elif detector.results_window and detector.current_image is not None:
                processed_frame, spots, temp = detector.process_frame(detector.current_image)
                if processed_frame is not None:
                    processed_frame = pygame.transform.scale(processed_frame, (640, 480))
                    pygame.draw.rect(DISPLAY, WHITE, (WINDOW_WIDTH//2 - 325, 100, 650, 490), 3)
                    DISPLAY.blit(processed_frame, (WINDOW_WIDTH//2 - 320, 105))
            
            # Draw modern stats panel
            stats_panel.fill((0, 31, 63))
            pygame.draw.rect(stats_panel, WHITE, stats_panel.get_rect(), 2)
            DISPLAY.blit(stats_panel, (40, 100))
            
            # Draw enhanced stats with emojis
            stats_text = [
                f"Temperature Threshold: {detector.temp_threshold}°C",
                f"Hot Spots Detected: {detector.hot_spots_count}",
                f"Maximum Temperature: {round(detector.max_temp/255.0 * 100, 1)}°C",
                f"Recording Status: {'Active' if detector.recording else 'Inactive'}"
            ]
            
            for i, text in enumerate(stats_text):
                text_surface = detector.font.render(text, True, WHITE)
                DISPLAY.blit(text_surface, (50, 110 + i * 35))
            
            # Draw UI elements
            for button in buttons.values():
                if button != buttons['back']:
                    button.draw(DISPLAY)
        
        # Always draw exit button
        buttons['exit'].draw(DISPLAY)
        
        # Draw footer
        draw_footer(DISPLAY)
        
        pygame.display.flip()
        clock.tick(30)
    
    detector.camera.release()
    pygame.quit()

if __name__ == '__main__':
    main()