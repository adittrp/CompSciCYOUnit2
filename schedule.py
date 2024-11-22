import pygame
from queuemodule import Queue
from stack import Stack
from linklist import LinkedList
import sys


class Schedule:
    def __init__(self, screen, back_function):
        self.screen = screen
        self.back_function = back_function
        self.linked_list = LinkedList()
        self.task_queue = Queue()
        self.task_stack = Stack()
        self.show_add_popup = False
        self.new_description = ""
        self.new_time = ""
        self.priority = "Regular"
        self.abbreviation = "AM"
        self.focused_box = None
        self.font = pygame.font.Font(None, 40)

    def add_task(self):
        if self.new_description.strip() and self.new_time.strip():
            full_time = f"{self.new_time} {self.abbreviation}"
            new_node = self.linked_list.addNode(
                self.new_description, self.priority, full_time
            )

            if self.priority == "Urgent":
                self.task_stack.push(new_node)
            else:
                self.task_queue.enqueue(new_node)

            # Reset fields
            self.new_description = ""
            self.new_time = ""
            self.priority = "Regular"
            self.abbreviation = "AM"
            self.focused_box = None
            self.show_add_popup = False

    def complete_task(self):
        try:
            # Check for urgent tasks
            urgent_task = self.task_stack.pop()
            self.linked_list.removeNode(desc=urgent_task.description)
        except IndexError:
            try:
                # Fallback to regular tasks
                regular_task = self.task_queue.dequeue()
                self.linked_list.removeNode(desc=regular_task.description)
            except IndexError:
                print("No tasks to complete!")

    def draw_ui(self):
        self.screen.fill((20, 25, 92))

        # Back button
        back_button = pygame.Rect(50, 50, 150, 100)
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        back_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, (85, 85))

        # Complete Task button
        complete_button = pygame.Rect(1500, 950, 250, 75)
        pygame.draw.rect(self.screen, (50, 168, 82), complete_button)
        complete_text = self.font.render("Complete Task", True, (255, 255, 255))
        self.screen.blit(complete_text, (1525, 970))

        # Add Task button
        add_button = pygame.Rect(50, 950, 200, 75)
        pygame.draw.rect(self.screen, (0, 128, 255), add_button)
        add_text = self.font.render("Add Task", True, (255, 255, 255))
        self.screen.blit(add_text, (75, 970))

        # Table Background
        bg_rect = pygame.Rect(400, 150, 1000, 700)
        pygame.draw.rect(self.screen, (200, 200, 200), bg_rect)

        # Table Headers
        header_rect = pygame.Rect(400, 150, 1000, 50)
        pygame.draw.rect(self.screen, (100, 100, 100), header_rect)
        headers = ["Description", "Priority", "Time"]
        header_x_positions = [510, 860, 1210]

        for idx, header in enumerate(headers):
            header_text = self.font.render(header, True, (255, 255, 255))
            self.screen.blit(header_text, (header_x_positions[idx], 160))

        # Task List Display
        y_offset = 210
        node = self.linked_list.head
        while node:
            task_details = [node.description, node.priority, node.scheduled_time]
            x_positions = [510, 860, 1210]
            for idx, detail in enumerate(task_details):
                task_text = self.font.render(detail, True, (0, 0, 0))
                self.screen.blit(task_text, (x_positions[idx], y_offset))
            y_offset += 50
            node = node.next

        return back_button, add_button, complete_button

    def draw_add_popup(self):
        popup_rect = pygame.Rect(660, 340, 600, 400)
        pygame.draw.rect(self.screen, (150, 150, 150), popup_rect)

        # Description input
        desc_box = pygame.Rect(680, 390, 560, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), desc_box)
        if self.focused_box == "description":
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (desc_box.x + 10 + self.font.size(self.new_description)[0], desc_box.y + 5),
                (desc_box.x + 10 + self.font.size(self.new_description)[0], desc_box.y + 45),
                2,
            )
        desc_text = self.font.render(self.new_description, True, (0, 0, 0))
        self.screen.blit(desc_text, (690, 400))

        # Time input
        time_box = pygame.Rect(680, 465, 400, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), time_box)
        if self.focused_box == "time":
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (time_box.x + 10 + self.font.size(self.new_time)[0], time_box.y + 5),
                (time_box.x + 10 + self.font.size(self.new_time)[0], time_box.y + 45),
                2,
            )
        time_text = self.font.render(self.new_time, True, (0, 0, 0))
        self.screen.blit(time_text, (690, 475))

        # AM/PM button
        ampm_button = pygame.Rect(1100, 465, 100, 50)
        pygame.draw.rect(self.screen, (0, 128, 255), ampm_button)
        ampm_text = self.font.render(self.abbreviation, True, (255, 255, 255))
        self.screen.blit(ampm_text, (1120, 475))

        # Priority buttons
        urgent_button = pygame.Rect(680, 540, 200, 50)
        regular_button = pygame.Rect(900, 540, 200, 50)
        pygame.draw.rect(
            self.screen, (255, 0, 0) if self.priority == "Urgent" else (200, 200, 200), urgent_button
        )
        pygame.draw.rect(
            self.screen, (0, 128, 255) if self.priority == "Regular" else (200, 200, 200), regular_button
        )

        urgent_text = self.font.render("Urgent", True, (255, 255, 255))
        regular_text = self.font.render("Regular", True, (255, 255, 255))
        self.screen.blit(urgent_text, (700, 550))
        self.screen.blit(regular_text, (920, 550))

        # Add and Close buttons
        add_button = pygame.Rect(680, 620, 200, 50)
        close_button = pygame.Rect(900, 620, 200, 50)
        pygame.draw.rect(self.screen, (0, 128, 255), add_button)
        pygame.draw.rect(self.screen, (255, 0, 0), close_button)

        add_text = self.font.render("Add Task", True, (255, 255, 255))
        close_text = self.font.render("X", True, (255, 255, 255))
        self.screen.blit(add_text, (700, 630))
        self.screen.blit(close_text, (980, 630))

        return desc_box, time_box, ampm_button, urgent_button, regular_button, add_button, close_button

    def run(self):
        """Main loop for the Schedule screen."""
        while True:
            mouse_pos = pygame.mouse.get_pos()
            if self.show_add_popup:
                desc_box, time_box, ampm_button, urgent_button, regular_button, add_button, close_button = self.draw_add_popup()
            else:
                back_button, add_button, complete_button = self.draw_ui()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_add_popup:
                        if desc_box.collidepoint(mouse_pos):
                            self.focused_box = "description"
                        elif time_box.collidepoint(mouse_pos):
                            self.focused_box = "time"
                        elif ampm_button.collidepoint(mouse_pos):
                            self.abbreviation = "PM" if self.abbreviation == "AM" else "AM"
                        elif urgent_button.collidepoint(mouse_pos):
                            self.priority = "Urgent"
                        elif regular_button.collidepoint(mouse_pos):
                            self.priority = "Regular"
                        elif add_button.collidepoint(mouse_pos):
                            self.add_task()
                        elif close_button.collidepoint(mouse_pos):
                            self.show_add_popup = False
                    else:
                        if back_button.collidepoint(mouse_pos):
                            return self.back_function()
                        elif add_button.collidepoint(mouse_pos):
                            self.show_add_popup = True
                        elif complete_button.collidepoint(mouse_pos):
                            self.complete_task()
                elif event.type == pygame.KEYDOWN:
                    if self.focused_box == "description":
                        if event.key == pygame.K_BACKSPACE:
                            self.new_description = self.new_description[:-1]
                        else:
                            self.new_description += event.unicode
                    elif self.focused_box == "time":
                        if event.key == pygame.K_BACKSPACE:
                            self.new_time = self.new_time[:-1]
                        elif event.unicode in "0123456789:" and len(self.new_time) < 5:
                            self.new_time += event.unicode

            pygame.display.flip()
