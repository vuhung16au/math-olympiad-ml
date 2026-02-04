"""Main application entry point for Rubik's Cube Group Theory Solver."""

import pygame
import sys
import os
import logging
import random
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add project root to path for imports
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.cube_state import CubeState
from core.permutations import apply_move, MOVES
from visualization.flat_renderer import FlatRenderer, COLORS
from visualization.graph_renderer import GraphRenderer
from visualization.cube_3d_renderer import Cube3DRenderer
from solvers.basic_algo import BeginnerSolver
from solvers.two_phase_solver import TwoPhaseSolver


# Default resolution (16:9)
DEFAULT_WIDTH = 1080
DEFAULT_HEIGHT = 608


def setup_logging():
    """Set up logging to both console and file.
    
    Returns:
        Logger instance and log buffer list
    """
    # Create logs directory if it doesn't exist
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Create log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"rubiks_moves_{timestamp}.txt"
    
    # Configure logging
    logger = logging.getLogger("rubiks_solver")
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create a log buffer for UI display
    log_buffer = []
    
    class BufferHandler(logging.Handler):
        """Custom handler that stores log messages in a buffer."""
        def __init__(self, buffer):
            super().__init__()
            self.buffer = buffer
        
        def emit(self, record):
            msg = self.format(record)
            self.buffer.append(msg)
            # Keep only last 20 log entries for display
            if len(self.buffer) > 20:
                self.buffer.pop(0)
    
    # Console handler (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S')
    console_handler.setFormatter(console_format)
    
    # File handler
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_format = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_format)
    
    # Buffer handler for UI display
    buffer_handler = BufferHandler(log_buffer)
    buffer_handler.setLevel(logging.INFO)
    buffer_format = logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S')
    buffer_handler.setFormatter(buffer_format)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(buffer_handler)
    
    # Log session start
    logger.info("=" * 60)
    logger.info(f"Rubik's Cube Solver Session Started")
    logger.info(f"Log file: {log_file}")
    logger.info("=" * 60)
    
    return logger, log_buffer


def scramble_cube(cube: CubeState, num_moves: int = 25):
    """Scramble the cube by applying random moves.
    
    Args:
        cube: CubeState to scramble
        num_moves: Number of random moves to apply (default: 25)
    
    Returns:
        List of moves that were applied
    """
    move_list = list(MOVES.keys())
    applied_moves = []
    
    for _ in range(num_moves):
        move = random.choice(move_list)
        apply_move(cube, move)
        applied_moves.append(move)
    
    return applied_moves


class SolveButton:
    """UI button for triggering the solver."""
    
    def __init__(self, x: int, y: int, width: int = 120, height: int = 40):
        """Initialize button.
        
        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = "Solve"
        self.state = "normal"  # normal, hover, clicked, disabled
        self.font = None
    
    def set_font(self, font):
        """Set font for button text."""
        self.font = font
    
    def update(self, mouse_pos: tuple, mouse_clicked: bool) -> bool:
        """Update button state and return True if clicked.
        
        Args:
            mouse_pos: Current mouse position
            mouse_clicked: Whether mouse button is clicked
        
        Returns:
            True if button was clicked
        """
        if self.state == "disabled":
            return False
        
        if self.rect.collidepoint(mouse_pos):
            if mouse_clicked:
                self.state = "clicked"
                return True
            else:
                self.state = "hover"
        else:
            self.state = "normal"
        
        return False
    
    def draw(self, screen: pygame.Surface):
        """Draw the button.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Background color based on state
        if self.state == "disabled":
            bg_color = COLORS['warmstone']
            text_color = COLORS['deepcharcoal']
        elif self.state == "hover":
            bg_color = COLORS['softivory']
            text_color = COLORS['bookred']
        elif self.state == "clicked":
            bg_color = COLORS['deepcharcoal']
            text_color = COLORS['softivory']
        else:
            bg_color = COLORS['softivory']
            text_color = COLORS['bookpurple']
        
        # Draw button
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, COLORS['deepcharcoal'], self.rect, 2)
        
        # Draw text
        if self.font:
            text_surface = self.font.render(self.text, True, text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)


class RubiksApp:
    """Main application class."""
    
    def __init__(self):
        """Initialize the application."""
        pygame.init()
        
        # Setup logging
        self.logger, self.log_buffer = setup_logging()
        
        # Window setup
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.fullscreen = False
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Rubik's Cube Group Theory Solver")
        
        # Cube state - start with scrambled cube
        self.cube = CubeState()
        scramble_moves = scramble_cube(self.cube, num_moves=25)
        self.logger.info(f"Cube initialized and scrambled with {len(scramble_moves)} random moves")
        self.logger.info(f"Scramble sequence: {' '.join(scramble_moves)}")
        
        # Store scramble for solving (reverse to solve)
        self.scramble_sequence = scramble_moves.copy()
        # Track manual moves made by user
        self.manual_moves = []
        
        # Undo/Redo Stacks
        self.move_history = [] # List of moves, e.g. ['U', "R'"]
        self.redo_stack = []   # List of moves to redo
        
        # 3D Interaction
        self.rotating_3d = False
        self.last_mouse_pos = (0, 0)
        
        # Renderers
        self.flat_renderer = FlatRenderer(self.width, self.height)
        self.graph_renderer = GraphRenderer(self.width, self.height)
        self.cube_3d_renderer = Cube3DRenderer(self.width, self.height)
        self.current_renderer = self.flat_renderer  # Start with flat view
        
        # Helper for efficient move lookup
        self.move_map = {
            pygame.K_u: ('U', "U'"),
            pygame.K_d: ('D', "D'"),
            pygame.K_r: ('R', "R'"),
            pygame.K_l: ('L', "L'"),
            pygame.K_f: ('F', "F'"),
            pygame.K_b: ('B', "B'"),
        }

        # Animation state
        self.animating = False
        self.animation_move_name = None
        self.animation_progress = 0.0
        # Smooth move animation timing (milliseconds per move).
        self.animation_duration_ms = 220
        
        # Overlay state
        self.overlay_text = None
        self.overlay_timer = 0
        self.overlay_duration = 1000 # ms to show overlay
        self.overlay_font = pygame.font.Font(None, 120)
        
        # Solvers and selected mode.
        self.beginner_solver = BeginnerSolver()
        self.two_phase_solver = TwoPhaseSolver()
        self.solver = self.beginner_solver
        self.solver_mode = "reverse"  # "reverse" or "two_phase"
        self.solver_name = "Reverse Sequence"
        self.solving = False
        self.solving_paused = False
        self.step_budget = 0
        self.step_allow_finish_current = False
        self.solution_moves = []
        self.current_move_index = 0
        self.solution_timer = 0
        self.solution_delay = 500  # ms delay between moves (after animation finishes)
        self.solve_start_ms = 0
        self.pause_started_ms = 0
        self.paused_total_ms = 0
        self.active_solution_metrics = None
        self.last_solve_report = None
        self.last_compare_report = None

        
        # UI
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.tiny_font = pygame.font.Font(None, 18)  # For instructions and log
        self.solve_button = SolveButton(self.width - 150, 20, 120, 40)
        self.solve_button.set_font(self.font)
        self.scramble_button = SolveButton(self.width - 150, 70, 120, 40)
        self.scramble_button.set_font(self.font)
        self.scramble_button.text = "Scramble"
        self.reset_view_button = SolveButton(self.width - 150, 270, 120, 40)
        self.reset_view_button.set_font(self.small_font)
        self.reset_view_button.text = "Reset 3D"
        self.view_button = SolveButton(self.width - 150, 120, 120, 40)
        self.view_button.set_font(self.font)
        self.view_button.text = "View"  # Will toggle between "View" and "Graph"
        self.patterns_button = SolveButton(self.width - 150, 170, 120, 40)
        self.patterns_button.set_font(self.font)
        self.patterns_button.text = "Pattern"
        self.solver_button = SolveButton(self.width - 150, 220, 120, 40)
        self.solver_button.set_font(self.small_font)
        self._refresh_solver_button_text()
        self.pause_button = SolveButton(self.width - 150, 320, 120, 40)
        self.pause_button.set_font(self.small_font)
        self.pause_button.text = "Pause"
        self.step_button = SolveButton(self.width - 150, 370, 120, 40)
        self.step_button.set_font(self.small_font)
        self.step_button.text = "Step"
        self.cancel_button = SolveButton(self.width - 150, 420, 120, 40)
        self.cancel_button.set_font(self.small_font)
        self.cancel_button.text = "Cancel"
        
        # Clock
        self.clock = pygame.time.Clock()
    
    def handle_events(self):
        """Handle pygame events."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.VIDEORESIZE:
                self.width = event.w
                self.height = event.h
                # Maintain 16:9 aspect ratio
                target_ratio = 16 / 9
                current_ratio = self.width / self.height
                if current_ratio > target_ratio:
                    self.height = int(self.width / target_ratio)
                else:
                    self.width = int(self.height * target_ratio)
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                self.flat_renderer.set_screen_size(self.width, self.height)
                self.graph_renderer.set_screen_size(self.width, self.height)
                self.cube_3d_renderer.set_screen_size(self.width, self.height)
                self.solve_button.rect.x = self.width - 150
                self.scramble_button.rect.x = self.width - 150
                self.view_button.rect.x = self.width - 150
                self.patterns_button.rect.x = self.width - 150
                self.solver_button.rect.x = self.width - 150
                self.reset_view_button.rect.x = self.width - 150
                self.pause_button.rect.x = self.width - 150
                self.step_button.rect.x = self.width - 150
                self.cancel_button.rect.x = self.width - 150
            
            elif event.type == pygame.KEYDOWN:
                if self.solving:
                    continue  # Ignore input while solving
                
                # Fullscreen toggle
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                
                # Speed control
                elif event.key == pygame.K_LEFTBRACKET: # [ Slower
                    self.animation_duration_ms = min(1200, int(self.animation_duration_ms * 1.25))
                    self.logger.info(f"Speed decreased: {self.animation_duration_ms} ms/move")
                elif event.key == pygame.K_RIGHTBRACKET: # ] Faster
                    self.animation_duration_ms = max(120, int(self.animation_duration_ms / 1.25))
                    self.logger.info(f"Speed increased: {self.animation_duration_ms} ms/move")
                
                # Visualization mode switch
                elif event.key == pygame.K_v:
                    self.toggle_view()
                
                # Cube moves keys
                elif event.key in self.move_map:
                    if self.animating:
                        continue # Ignore inputs while animating manual move
                        
                    cw_move, ccw_move = self.move_map[event.key]
                    if event.mod & pygame.KMOD_SHIFT:
                        move = ccw_move
                    else:
                        move = cw_move
                    
                    # Start animation instead of applying immediately
                    self.start_animation(move)
                    self.manual_moves.append(move)
                    self.move_history.append(move)
                    self.redo_stack.clear() # Clear redo on new move
                    self.logger.info(f"Manual move: {move}")
                
                # Undo/Redo
                elif event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_META):
                    if event.mod & pygame.KMOD_SHIFT: # Redo (Ctrl+Shift+Z)
                        self.input_redo()
                    else: # Undo (Ctrl+Z)
                        self.input_undo()
                elif event.key == pygame.K_y and (event.mod & pygame.KMOD_CTRL or event.mod & pygame.KMOD_META): # Redo (Ctrl+Y)
                    self.input_redo()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    # Check 3D interaction (if in graph view or valid area)
                    # Let's say right half of screen is valid for 3D rotation if in Graph Mode
                    # Or anywhere not on buttons.
                    if self.current_renderer == self.graph_renderer:
                        # Simple check: clicked on right side? or anywhere?
                        # Let's allow anywhere for now as long as not buttons
                        self.rotating_3d = True
                        self.last_mouse_pos = mouse_pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.rotating_3d = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.rotating_3d and self.current_renderer == self.graph_renderer:
                    dx = mouse_pos[0] - self.last_mouse_pos[0]
                    dy = mouse_pos[1] - self.last_mouse_pos[1]
                    
                    # Update rotation
                    # Sensitivity factor
                    sens = 0.5
                    new_ry = self.cube_3d_renderer.rot_y + dx * sens
                    new_rx = self.cube_3d_renderer.rot_x + dy * sens
                    # Constrain pitch to avoid flipping
                    new_rx = max(-90, min(90, new_rx))
                    
                    self.cube_3d_renderer.set_rotation(new_rx, new_ry)
                    self.last_mouse_pos = mouse_pos
        
        # Interruption controls are always available when active.
        if self.pause_button.update(mouse_pos, mouse_clicked):
            self.toggle_pause_resume()
        elif self.step_button.update(mouse_pos, mouse_clicked):
            self.step_once()
        elif self.cancel_button.update(mouse_pos, mouse_clicked):
            self.cancel_current_action()

        # Main controls
        if not self.solving:
            # Re-fetch mouse state because we might have handled events
            # But the update() methed takes mouse_pos
            if self.solve_button.update(mouse_pos, mouse_clicked):
                self.start_solving()
            elif self.scramble_button.update(mouse_pos, mouse_clicked):
                self.scramble_cube()
            elif self.view_button.update(mouse_pos, mouse_clicked):
                self.toggle_view()
            elif self.patterns_button.update(mouse_pos, mouse_clicked):
                self.apply_next_pattern()
            elif self.solver_button.update(mouse_pos, mouse_clicked):
                self.toggle_solver_mode()
            elif self.reset_view_button.update(mouse_pos, mouse_clicked):
                self.cube_3d_renderer.set_rotation(30, -45)
        else:
            # Disable buttons while solving
            self.scramble_button.state = "disabled"
            self.view_button.state = "disabled"
            self.patterns_button.state = "disabled"
            self.solver_button.state = "disabled"

        # Control button availability/status.
        if self.solving or self.animating:
            # Keep current pause label based on state.
            self.pause_button.state = "normal"
        else:
            self.pause_button.state = "disabled"
            self.pause_button.text = "Pause"

        if self.solving and self.solving_paused:
            self.step_button.state = "normal"
        else:
            self.step_button.state = "disabled"

        if self.solving or self.animating:
            self.cancel_button.state = "normal"
        else:
            self.cancel_button.state = "disabled"
        
        return True
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.width, self.height = self.screen.get_size()
        else:
            self.width = DEFAULT_WIDTH
            self.height = DEFAULT_HEIGHT
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        
        self.flat_renderer.set_screen_size(self.width, self.height)
        self.graph_renderer.set_screen_size(self.width, self.height)
        self.cube_3d_renderer.set_screen_size(self.width, self.height)
        self.solve_button.rect.x = self.width - 150
        self.scramble_button.rect.x = self.width - 150
        self.solve_button.rect.x = self.width - 150
        self.scramble_button.rect.x = self.width - 150
        self.view_button.rect.x = self.width - 150
        self.patterns_button.rect.x = self.width - 150
        self.solver_button.rect.x = self.width - 150
        self.reset_view_button.rect.x = self.width - 150
        self.pause_button.rect.x = self.width - 150
        self.step_button.rect.x = self.width - 150
        self.cancel_button.rect.x = self.width - 150

    def _refresh_solver_button_text(self):
        """Update solver label from selected mode."""
        if self.solver_mode == "two_phase":
            self.solver_button.text = "Solver: 2P"
            self.solver_name = "Two-Phase (Kociemba)"
        else:
            self.solver_button.text = "Solver: Rev"
            self.solver_name = "Reverse Sequence"

    def toggle_solver_mode(self):
        """Switch between old and new solver algorithms."""
        if self.solving:
            return
        self.solver_mode = "two_phase" if self.solver_mode == "reverse" else "reverse"
        self._refresh_solver_button_text()
        if self.solver_mode == "two_phase" and not self.two_phase_solver.is_available():
            self.logger.info(
                f"Two-Phase selected but unavailable ({self.two_phase_solver.availability_reason()})"
            )
        else:
            self.logger.info(f"Solver mode changed to: {self.solver_name}")

    def _reset_interruption_state(self):
        """Reset pause/step state."""
        self.solving_paused = False
        self.step_budget = 0
        self.step_allow_finish_current = False
        self.pause_started_ms = 0
        self.pause_button.text = "Pause"

    def toggle_pause_resume(self):
        """Pause or resume queued solving/animation."""
        if not self.solving and not self.animating:
            return
        self.solving_paused = not self.solving_paused
        self.pause_button.text = "Resume" if self.solving_paused else "Pause"
        if self.solving_paused:
            self.pause_started_ms = pygame.time.get_ticks()
        elif self.pause_started_ms:
            self.paused_total_ms += max(0, pygame.time.get_ticks() - self.pause_started_ms)
            self.pause_started_ms = 0
        if not self.solving_paused:
            self.step_allow_finish_current = False
        self.logger.info("Paused solving" if self.solving_paused else "Resumed solving")

    def step_once(self):
        """Advance exactly one queued move while paused."""
        if not self.solving:
            return
        if not self.solving_paused:
            self.solving_paused = True
            self.pause_button.text = "Resume"
            self.pause_started_ms = pygame.time.get_ticks()

        if self.animating:
            # Finish the in-flight move only.
            self.step_allow_finish_current = True
        else:
            # Start exactly one move from queue.
            self.step_budget = 1
            self.solution_timer = self.solution_delay
        self.logger.info("Step requested")

    def cancel_current_action(self):
        """Cancel solving or any in-progress animation."""
        if not self.solving and not self.animating:
            return

        self.solving = False
        self.animating = False
        self.animation_move_name = None
        self.animation_progress = 0.0
        self.solution_moves = []
        self.current_move_index = 0
        self.solution_timer = 0
        self.active_solution_metrics = None
        self.solve_start_ms = 0
        self._reset_interruption_state()

        self.solve_button.state = "normal"
        self.scramble_button.state = "normal"
        self.view_button.state = "normal"
        self.patterns_button.state = "normal"
        self.solver_button.state = "normal"
        self.logger.info("Solve/animation canceled")

    def _start_solve_timer(self):
        """Initialize timing state for the current solve."""
        self.solve_start_ms = pygame.time.get_ticks()
        self.pause_started_ms = 0
        self.paused_total_ms = 0

    def _get_elapsed_solve_seconds(self) -> float:
        """Return elapsed solve time in seconds, excluding paused periods."""
        if not self.solve_start_ms:
            return 0.0
        now = pygame.time.get_ticks()
        paused_now = 0
        if self.solving_paused and self.pause_started_ms:
            paused_now = now - self.pause_started_ms
        elapsed_ms = max(0, now - self.solve_start_ms - self.paused_total_ms - paused_now)
        return elapsed_ms / 1000.0

    def _build_reverse_solution(self):
        """Build reverse-sequence solve path from scramble + manual moves."""
        all_moves = self.scramble_sequence + self.manual_moves
        inverse_moves = {
            'U': "U'", "U'": 'U',
            'D': "D'", "D'": 'D',
            'R': "R'", "R'": 'R',
            'L': "L'", "L'": 'L',
            'F': "F'", "F'": 'F',
            'B': "B'", "B'": 'B',
        }
        return [inverse_moves[move] for move in reversed(all_moves)]

    def _parse_move_amount(self, move: str):
        """Convert a move token to (face, quarter-turn amount mod 4)."""
        if move.endswith("2"):
            return move[0], 2
        if move.endswith("'"):
            return move[0], 3
        return move[0], 1

    def _canonicalize_for_metrics(self, moves):
        """Reduce adjacent same-face moves for HTM/QTM counting."""
        reduced = []
        for move in moves:
            face, amt = self._parse_move_amount(move)
            if reduced and reduced[-1][0] == face:
                prev_face, prev_amt = reduced[-1]
                new_amt = (prev_amt + amt) % 4
                if new_amt == 0:
                    reduced.pop()
                else:
                    reduced[-1] = (prev_face, new_amt)
            else:
                reduced.append((face, amt % 4))

        out = []
        for face, amt in reduced:
            if amt == 1:
                out.append(face)
            elif amt == 2:
                out.append(f"{face}2")
            elif amt == 3:
                out.append(f"{face}'")
        return out

    def _compute_move_metrics(self, moves):
        """Return HTM/QTM metrics for a move list."""
        canonical = self._canonicalize_for_metrics(moves)
        htm = len(canonical)
        qtm = sum(2 if token.endswith("2") else 1 for token in canonical)
        return {"htm": htm, "qtm": qtm}

    def _build_compare_report(self, reverse_moves, two_phase_moves):
        """Build side-by-side algorithm comparison report."""
        reverse_metrics = self._compute_move_metrics(reverse_moves)
        report = {
            "reverse": reverse_metrics,
            "two_phase": None,
            "delta_qtm": None,
            "delta_htm": None,
        }
        if two_phase_moves is not None:
            two_phase_metrics = self._compute_move_metrics(two_phase_moves)
            report["two_phase"] = two_phase_metrics
            report["delta_qtm"] = two_phase_metrics["qtm"] - reverse_metrics["qtm"]
            report["delta_htm"] = two_phase_metrics["htm"] - reverse_metrics["htm"]
        return report
    
    def input_undo(self):
        """Undo last move."""
        if not self.move_history or self.animating:
            return
            
        last_move = self.move_history.pop()
        
        # Inverse move
        invert_map = {
            'U': "U'", "U'": 'U', 'D': "D'", "D'": 'D',
            'R': "R'", "R'": 'R', 'L': "L'", "L'": 'L',
            'F': "F'", "F'": 'F', 'B': "B'", "B'": 'B'
        }
        inv_move = invert_map[last_move]
        
        # Animate
        self.start_animation(inv_move)
        # We don't append this undo-action to move_history
        # But we push the ORIGINAL move to redo_stack
        self.redo_stack.append(last_move)
        self.logger.info(f"Undo: {last_move} -> {inv_move}")

    def input_redo(self):
        """Redo last undone move."""
        if not self.redo_stack or self.animating:
            return
            
        move = self.redo_stack.pop()
        self.start_animation(move)
        self.move_history.append(move)
        self.logger.info(f"Redo: {move}")
    
    def toggle_view(self):
        """Toggle between flat and graph visualization modes."""
        if self.current_renderer == self.flat_renderer:
            self.current_renderer = self.graph_renderer
            self.view_button.text = "Graph"
            self.logger.info("Switched to Graph View (circle/planar graph)")
        else:
            self.current_renderer = self.flat_renderer
            self.view_button.text = "View"
            self.logger.info("Switched to Flat View (unfolded cross)")
    
    def scramble_cube(self):
        """Scramble the cube to a random state."""
        if self.solving:
            return  # Don't scramble while solving
        
        # Reset cube to solved state
        self.cube = CubeState()
        
        # Apply random scramble
        scramble_moves = scramble_cube(self.cube, num_moves=25)
        self.scramble_sequence = scramble_moves.copy()
        self.manual_moves = []  # Reset manual moves
        
        # Reset solver state
        self.solving = False
        self.animating = False
        self.solution_moves = []
        self.current_move_index = 0
        self.solve_button.state = "normal"
        self.solver_button.state = "normal"
        self.active_solution_metrics = None
        self.solve_start_ms = 0
        self._reset_interruption_state()
        
        # Log the scramble
        self.logger.info("=" * 60)
        self.logger.info("Cube scrambled with 25 random moves")
        self.logger.info(f"Scramble sequence: {' '.join(scramble_moves)}")
        self.logger.info("=" * 60)

    def apply_next_pattern(self):
        """Apply a preset pattern."""
        if self.solving:
            return
            
        # Pattern cycle: Checkerboard -> Superflip -> Solved (Scramble to Solved)
        # Actually simplest is just to apply Checkerboard.
        # Let's verify start state.
        
        # Checkerboard algorithm: R2 L2 U2 D2 F2 B2
        # Apply instantly? Or animate?
        # User implies "Presets".
        # Let's just solve first (reset), then apply pattern.
        
        self.cube = CubeState() # Reset to solved
        
        # Use a simple toggle state or random choice?
        # Let's cycle.
        if not hasattr(self, '_pattern_idx'):
            self._pattern_idx = 0
        
        patterns = [
            ("Checkerboard", ["R", "R", "L", "L", "U", "U", "D", "D", "F", "F", "B", "B"]),
            ("Wire", ["R", "L", "F", "B", "U", "D", "R", "L", "F", "B", "U", "D"]), 
             # Superflip is long, maybe skip for now or find shorter
            ("Anaconda", ["L", "U", "B'", "U'", "R", "L'", "B", "R'", "F", "B'", "D", "R", "D'", "F'"]),
        ]
        
        name, moves = patterns[self._pattern_idx]
        self._pattern_idx = (self._pattern_idx + 1) % len(patterns)
        
        self.logger.info(f"Applying pattern: {name}")
        
        # Animate the pattern moves
        # We can reuse the solver logic!
        self.solution_moves = moves
        self.current_move_index = 0
        self.solution_timer = 0
        self.solving = True # This enables the update loop to process moves
        self._reset_interruption_state()
        
        # Disable buttons
        self.solve_button.state = "disabled"
        self.scramble_button.state = "disabled"
        self.patterns_button.state = "disabled"
        self.solver_button.state = "disabled"

    def start_solving(self):
        """Start the solving process."""
        if self.solving:
            return
        
        self.solving = True
        self.solve_button.state = "disabled"
        self.patterns_button.state = "disabled"
        self.solver_button.state = "disabled"
        self._reset_interruption_state()
        
        # Generate solution by reversing all moves (scramble + manual)
        self.logger.info("=" * 60)
        self.logger.info("Starting auto-solver")

        self.solution_moves = []
        reverse_moves = self._build_reverse_solution()
        two_phase_moves = None

        if self.two_phase_solver.is_available():
            try:
                two_phase_moves = self.two_phase_solver.solve(self.cube.copy())
            except Exception as exc:
                if self.solver_mode == "two_phase":
                    self.logger.warning(f"Two-phase solve failed: {exc}")
                    self.solving = False
                    self.solve_button.state = "normal"
                    self.patterns_button.state = "normal"
                    self.solver_button.state = "normal"
                    self.active_solution_metrics = None
                    self.solve_start_ms = 0
                    self._reset_interruption_state()
                    return
                self.logger.info(f"Two-phase comparison unavailable: {exc}")
        elif self.solver_mode == "two_phase":
            self.logger.warning(
                f"Two-Phase unavailable: {self.two_phase_solver.availability_reason()}. "
                "Install with: uv pip install -e \".[fast-solver]\""
            )
            self.solving = False
            self.solve_button.state = "normal"
            self.patterns_button.state = "normal"
            self.solver_button.state = "normal"
            self.active_solution_metrics = None
            self.solve_start_ms = 0
            self._reset_interruption_state()
            return

        if self.solver_mode == "two_phase":
            self.solution_moves = two_phase_moves or []
            self.solver = self.two_phase_solver
            self.logger.info("Using Two-Phase (Kociemba) solver")
        else:
            self.solution_moves = reverse_moves
            self.solver = self.beginner_solver
            self.logger.info("Using Reverse Sequence solver")

        self.active_solution_metrics = self._compute_move_metrics(self.solution_moves)
        self.last_compare_report = self._build_compare_report(reverse_moves, two_phase_moves)
        self._start_solve_timer()

        self.logger.info(f"Solution generated: {len(self.solution_moves)} moves")
        self.logger.info(f"Solution sequence: {' '.join(self.solution_moves)}")
        self.logger.info("=" * 60)
        self.logger.info("=" * 60)
        self.current_move_index = 0
        self.solution_timer = 0
        
    def start_animation(self, move_name: str):
        """Start animating a move."""
        self.animating = True
        self.animation_move_name = move_name
        self.animation_progress = 0.0
        
        # Show overlay
        self.overlay_text = move_name
        self.overlay_timer = self.overlay_duration

    def update_animation(self, dt: int):
        """Update animation progress."""
        if not self.animating:
            return

        if self.animation_duration_ms <= 0:
            self.animation_progress = 1.0
        else:
            self.animation_progress += dt / self.animation_duration_ms
        
        # Finish animation
        if self.animation_progress >= 1.0:
            self.animation_progress = 1.0
            apply_move(self.cube, self.animation_move_name)
            self.animating = False
            self.animation_move_name = None
            self.animation_progress = 0.0
    
    def update_solver(self, dt: int):
        """Update solver logic."""
        if not self.solving or not self.solution_moves:
            return

        # While paused, only allow starting a queued single step.
        if self.solving_paused and self.step_budget <= 0:
            return
            
        # If currently animating a move, just let it finish
        if self.animating:
            return

        # Wait for delay before starting next move
        self.solution_timer += dt
        
        if self.solution_timer >= self.solution_delay:
            # Start next move
            if self.current_move_index < len(self.solution_moves):
                move = self.solution_moves[self.current_move_index]
                self.start_animation(move)
                if self.solving_paused and self.step_budget > 0:
                    self.step_budget -= 1
                    self.step_allow_finish_current = True
                
                step_num = self.current_move_index + 1
                self.logger.info(f"Solver move [{step_num}/{len(self.solution_moves)}]: {move}")
                self.current_move_index += 1
                self.solution_timer = 0
            else:
                # Done solving
                elapsed_s = self._get_elapsed_solve_seconds()
                active = self.active_solution_metrics or {"htm": 0, "qtm": 0}
                qtm = active["qtm"]
                tps = (qtm / elapsed_s) if elapsed_s > 0 else 0.0
                self.last_solve_report = {
                    "algorithm": self.solver_name,
                    "htm": active["htm"],
                    "qtm": qtm,
                    "time_s": elapsed_s,
                    "tps": tps,
                }
                self.logger.info("=" * 60)
                self.logger.info("Solving completed!")
                if self.cube.is_solved():
                    self.logger.info("Cube is now SOLVED!")
                else:
                    self.logger.info("Warning: Cube state indicates not fully solved")
                self.logger.info(
                    f"Metrics [{self.solver_name}]: HTM={active['htm']} "
                    f"QTM={qtm} Time={elapsed_s:.2f}s TPS={tps:.2f}"
                )
                self.logger.info("=" * 60)
                self.solving = False
                self.solve_button.state = "normal"
                self.scramble_button.state = "normal"
                self.view_button.state = "normal"
                self.patterns_button.state = "normal"
                self.solver_button.state = "normal"
                self.solution_moves = []
                self.current_move_index = 0
                self.active_solution_metrics = None
                self._reset_interruption_state()
    
    def draw_instructions(self, screen):
        """Draw usage instructions and algorithm info on the left side."""
        x_start = 20
        y_start = 20
        line_height = 22
        tiny_font = pygame.font.Font(None, 18)
        small_font = pygame.font.Font(None, 20)
        
        instructions = [
            ("HOW TO USE:", COLORS['bookred']),
            ("• Keys: U/D/R/L/F/B (rotations)", COLORS['warmstone']),
            ("• Shift+Key: counter-clockwise", COLORS['warmstone']),
            ("• F11: Fullscreen", COLORS['warmstone']),
            ("• V: Toggle view", COLORS['warmstone']),
            ("", COLORS['softivory']),
            ("ALGORITHM:", COLORS['bookred']),
            (self.solver_name, COLORS['warmstone']),
            ("(Choose via Solver button)", COLORS['warmstone']),
            ("", COLORS['softivory']),
            ("BUTTONS:", COLORS['bookred']),
            ("• Solve: Auto-solve cube", COLORS['warmstone']),
            ("• Scramble: Randomize", COLORS['warmstone']),
            ("• Pattern: Cool designs", COLORS['warmstone']),
            ("• Solver: Switch algorithm", COLORS['warmstone']),
            ("• Pause/Step/Cancel: control queue", COLORS['warmstone']),
            ("• View: Toggle display", COLORS['warmstone']),
            ("", COLORS['softivory']),
            ("SPEED:", COLORS['bookred']),
            ("• [ : Slower", COLORS['warmstone']),
            ("• ] : Faster", COLORS['warmstone']),
        ]
        
        y = y_start
        for line, color in instructions:
            if not line:  # Empty line
                y += line_height // 2
                continue
            if line.endswith(":"):
                text_surface = small_font.render(line, True, color)
            else:
                text_surface = tiny_font.render(line, True, color)
            screen.blit(text_surface, (x_start, y))
            y += line_height

    def draw_metrics_panel(self, screen):
        """Draw move/time metrics and algorithm comparison."""
        x = 20
        y = 430
        w = 340
        h = 115
        panel_rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, COLORS['softivory'], panel_rect)
        pygame.draw.rect(screen, COLORS['deepcharcoal'], panel_rect, 2)

        title_font = pygame.font.Font(None, 20)
        tiny_font = pygame.font.Font(None, 18)
        screen.blit(title_font.render("METRICS:", True, COLORS['bookred']), (x + 8, y + 6))

        line_y = y + 30
        line_h = 18

        if self.solving and self.active_solution_metrics:
            elapsed = self._get_elapsed_solve_seconds()
            moved_qtm = self.current_move_index
            live_tps = (moved_qtm / elapsed) if elapsed > 0 else 0.0
            target = self.active_solution_metrics
            lines = [
                f"{self.solver_name}",
                f"Target HTM/QTM: {target['htm']}/{target['qtm']}",
                f"Time: {elapsed:.2f}s  TPS: {live_tps:.2f}",
            ]
        elif self.last_solve_report:
            r = self.last_solve_report
            lines = [
                f"Last: {r['algorithm']}",
                f"HTM/QTM: {r['htm']}/{r['qtm']}",
                f"Time: {r['time_s']:.2f}s  TPS: {r['tps']:.2f}",
            ]
        else:
            lines = ["No solve metrics yet"]

        for line in lines:
            screen.blit(tiny_font.render(line, True, COLORS['deepcharcoal']), (x + 8, line_y))
            line_y += line_h

        if self.last_compare_report:
            rev = self.last_compare_report["reverse"]
            two = self.last_compare_report["two_phase"]
            if two:
                delta_q = self.last_compare_report["delta_qtm"]
                better = "2P better" if delta_q < 0 else "Rev better" if delta_q > 0 else "Equal"
                compare_text = (
                    f"Compare QTM Rev:{rev['qtm']} vs 2P:{two['qtm']} ({better})"
                )
            else:
                compare_text = f"Compare QTM Rev:{rev['qtm']} vs 2P:N/A"
            screen.blit(tiny_font.render(compare_text, True, COLORS['deepcharcoal']), (x + 8, line_y))
    
    def draw_log_display(self, screen):
        """Draw recent log entries at the bottom of the screen."""
        log_y = self.height - 80
        log_height = 70
        tiny_font = pygame.font.Font(None, 18)
        
        # Draw background for log area
        log_rect = pygame.Rect(0, log_y, self.width, log_height)
        pygame.draw.rect(screen, COLORS['deepcharcoal'], log_rect)
        pygame.draw.rect(screen, COLORS['bookpurple'], log_rect, 2)
        
        # Draw log title
        title_font = pygame.font.Font(None, 20)
        title_text = title_font.render("LOG:", True, COLORS['bookred'])
        screen.blit(title_text, (10, log_y + 5))
        
        # Filter and show relevant log entries
        relevant_logs = []
        for log_entry in self.log_buffer[-15:]:  # Check last 15
            if any(keyword in log_entry for keyword in [
                "Scramble sequence", "Solution sequence", "Solver move", 
                "Manual move", "Switched to", "SOLVED", "Solving completed"
            ]):
                relevant_logs.append(log_entry)
        
        # Show last 3 entries (most recent at bottom)
        x_start = 10
        y_offset = log_y + 25
        max_lines = 3
        
        for log_entry in relevant_logs[-max_lines:]:
            # Truncate if too long to fit on screen
            max_width = self.width - 30
            if len(log_entry) > 80:
                log_entry = log_entry[:77] + "..."
            
            text_surface = tiny_font.render(log_entry, True, COLORS['softivory'])
            # Truncate visually if needed
            if text_surface.get_width() > max_width:
                # Simple truncation - could be improved with ellipsis
                truncated = log_entry
                while tiny_font.size(truncated + "...")[0] > max_width and len(truncated) > 10:
                    truncated = truncated[:-1]
                log_entry = truncated + "..."
                text_surface = tiny_font.render(log_entry, True, COLORS['softivory'])
            
            screen.blit(text_surface, (x_start, y_offset))
            y_offset += 18
    
    def draw(self):
        """Draw everything."""
        # Clear screen
        # Keep canvas distinct from white stickers for better contrast.
        self.screen.fill(COLORS['canvasgray'])
        
        # Draw cube (centered, leaving space for UI)
        # Draw cube (centered, leaving space for UI)
        # Construct animation state dict if animating
        anim_state = None
        if self.animating:
            anim_state = {
                'move': self.animation_move_name,
                'progress': self.animation_progress
            }
            
        # Flat renderer supports animation
        if self.current_renderer == self.flat_renderer:
            self.current_renderer.draw(self.screen, self.cube, anim_state)
        else:
            # Graph renderer doesn't support animation yet
            self.current_renderer.draw(self.screen, self.cube)

        
        # Draw 3D cube on right side when in graph view
        if self.current_renderer == self.graph_renderer:
            self.cube_3d_renderer.draw(self.screen, self.cube, anim_state)
        
        # Draw left-side instructions
        self.draw_instructions(self.screen)
        self.draw_metrics_panel(self.screen)
        
        # Draw UI buttons
        self.solve_button.draw(self.screen)
        self.scramble_button.draw(self.screen)
        self.view_button.draw(self.screen)
        self.patterns_button.draw(self.screen)
        self.solver_button.draw(self.screen)
        self.pause_button.draw(self.screen)
        self.step_button.draw(self.screen)
        self.cancel_button.draw(self.screen)
        if self.current_renderer == self.graph_renderer:
            self.reset_view_button.draw(self.screen)
        
        # Draw log display at bottom
        self.draw_log_display(self.screen)
        
        # Draw progress (above log area)
        if self.solving and self.solution_moves:
            # Determine current phase
            if hasattr(self.solver, 'phases'):
                current_phase = "Solving..."
                # Find the last phase that starts before or at current_move_index
                for start_idx, desc in self.solver.phases:
                    if self.current_move_index >= start_idx:
                        current_phase = desc
                
                # Draw phase description
                phase_surface = self.font.render(current_phase, True, COLORS['bookred'])
                self.screen.blit(phase_surface, (20, self.height - 130))

            # Fix: show current_move_index (0-based) + 1, but cap at total moves
            step_num = min(self.current_move_index + 1, len(self.solution_moves))
            progress_text = f"Solving step {step_num}/{len(self.solution_moves)}"
            text_surface = self.small_font.render(progress_text, True, COLORS['softivory'])
            self.screen.blit(text_surface, (20, self.height - 100))
        
        # Draw solved indicator
        if self.cube.is_solved():
            solved_text = "SOLVED!"
            text_surface = self.font.render(solved_text, True, COLORS['bookred'])
            text_rect = text_surface.get_rect(center=(self.width // 2, 50))
            self.screen.blit(text_surface, text_rect)
            
        # Draw move overlay
        if self.overlay_text and self.overlay_timer > 0:
            # Fade out calculation
            alpha = max(0, min(255, int(255 * (self.overlay_timer / self.overlay_duration))))
            if alpha > 0:
                text_surface = self.overlay_font.render(self.overlay_text, True, COLORS['softivory'])
                text_surface.set_alpha(alpha)
                text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
                # Create a shadow/outline for readability
                shadow_surface = self.overlay_font.render(self.overlay_text, True, COLORS['bookblack'])
                shadow_surface.set_alpha(alpha)
                shadow_rect = shadow_surface.get_rect(center=(self.width // 2 + 2, self.height // 2 + 2))
                
                self.screen.blit(shadow_surface, shadow_rect)
                self.screen.blit(text_surface, text_rect)
                
            self.overlay_timer -= 16 # Approx 1 frame at 60fps
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            running = self.handle_events()
            
            if self.animating:
                if (not self.solving_paused) or self.step_allow_finish_current:
                    self.update_animation(dt)
                    if self.step_allow_finish_current and not self.animating:
                        self.step_allow_finish_current = False
            
            if self.solving:
                self.update_solver(dt)
            
            self.draw()
        
        # Log session end
        self.logger.info("=" * 60)
        self.logger.info("Application closing")
        self.logger.info("=" * 60)
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    app = RubiksApp()
    app.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user. Exiting...")
        pygame.quit()
        sys.exit(0)
