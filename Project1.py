import tkinter as tk
import winsound
import pyglet
import customtkinter
from PIL import Image, ImageTk
import threading

class ClassroomAttendanceSystem:
    def __init__(self, root):  # Fixed __init__ method
        self.students = {
            "C23173": "FCC52-SAI S DASH",
            "C23029": "FCC36 - LOKESH LANJEWAR",
            "C23200": "FCC41-PRINCE OSTWAL",
            "C23223": "FCC24-HARSH SHARMA",
            "C23105": "FCC63-SPANDAN THUL",
        }
        self.root = root
        self.root.title("Classroom Attendance System")
        self.root.geometry("585x300")
        self.root.configure(bg="#f0f0f0")

        # Load and play background music
        self.music_player = pyglet.media.Player()
        self.music = pyglet.media.load("thunder.mp3")
        self.music_player.queue(self.music)
        self.music_player.volume = 0.01
        self.music_player.play()

        # Load animated background
        self.animation = Image.open("coder.gif")
        self.frames = []
        try:
            while True:
                self.frames.append(ImageTk.PhotoImage(self.animation.copy()))
                self.animation.seek(self.animation.tell() + 1)
        except EOFError:
            pass

        self.index = 0
        self.image = self.frames[self.index]
        self.background = tk.Label(self.root, image=self.image, bg="#f0f0f0")
        self.background.place(x=0, y=0, relwidth=1, relheight=1)

        # Start updating the background
        self.update_background()

        self.attendance_list = []

        # Create a frame for the student ID label and entry
        self.student_id_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.student_id_frame.pack(pady=20)

        self.label = customtkinter.CTkLabel(
            self.student_id_frame,
            text="Scan Student ID:",
            font=("Segoe UI", 14),
            fg_color="#f0f0f0",
            text_color="black",
        )
        self.label.grid(row=0, column=0, padx=(20, 10), pady=5)

        self.entry = customtkinter.CTkEntry(self.student_id_frame, font=("Arial", 14))
        self.entry.grid(row=0, column=1, padx=(0, 20), pady=5, sticky="we")
        self.entry.bind("<Return>", self.mark_attendance)  # Bind Enter key to submit

        # Create a frame for the submit button and status label
        self.control_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.control_frame.pack(pady=10)

        self.button = customtkinter.CTkButton(
            self.control_frame,
            text="Submit",
            command=self.mark_attendance,
            font=("Segoe UI", 14),
            fg_color="#4caf50",
            text_color="white",
            hover_color="#43a047",
        )
        self.button.grid(row=0, column=0, padx=(20, 0), pady=5)

        self.status_label = customtkinter.CTkLabel(
            self.control_frame, text="", font=("Arial", 14), fg_color="#f0f0f0", text_color="#4caf50"
        )
        self.status_label.grid(row=0, column=1, padx=(10, 20), pady=5)

        # Create a frame for the attendance list
        self.attendance_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.attendance_frame.pack(pady=10)

        self.attendance_label = customtkinter.CTkLabel(
            self.attendance_frame, text="Attendance List:", font=("Arial", 14), fg_color="#f0f0f0", text_color="black"
        )
        self.attendance_label.grid(row=0, column=0, padx=(20, 0), pady=5)

        self.attendance_text = customtkinter.CTkTextbox(
            self.attendance_frame, font=("Arial", 12), state="disabled", width=300, height=100
        )
        self.attendance_text.grid(row=1, column=0, padx=(20, 0), pady=5)

    def mark_attendance(self, event=None):
        student_id = self.entry.get().strip()
        if student_id in self.students:
            if student_id not in self.attendance_list:
                self.attendance_list.append(student_id)
                self.status_label.configure(
                    text=f"Attendance marked for {self.students[student_id]}",
                    text_color="#4caf50",
                )
                self.play_sound()
                self.update_attendance_list()
            else:
                self.status_label.configure(
                    text=f"{self.students[student_id]} is already marked.",
                    text_color="#f44336",
                )
        else:
            self.status_label.configure(
                text="Invalid student ID. Try again.",
                text_color="#f44336",
            )
        self.entry.delete(0, "end")

    def play_sound(self):
        winsound.Beep(1000, 200)

    def update_background(self):
        self.index += 1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[self.index]
        self.background.config(image=self.image)
        self.root.after(100, self.update_background)

    def update_attendance_list(self):
        self.attendance_text.configure(state="normal")
        self.attendance_text.delete("1.0", "end")

        present_students = [self.students[id] for id in self.attendance_list]
        absent_students = [student for student in self.students.values() if student not in present_students]

        self.attendance_text.insert("1.0", "Present Students:\n")
        for student in present_students:
            self.attendance_text.insert("end", f"- {student}\n")

        self.attendance_text.insert("end", "\nAbsent Students:\n")
        for student in absent_students:
            self.attendance_text.insert("end", f"- {student}\n")

        self.attendance_text.configure(state="disabled")

if __name__ == "__main__":  # Fixed if condition
    root = customtkinter.CTk()
    app = ClassroomAttendanceSystem(root)
    root.mainloop()
