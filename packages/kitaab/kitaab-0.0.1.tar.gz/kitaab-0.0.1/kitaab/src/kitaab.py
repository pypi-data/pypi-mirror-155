import os
import sys
import sqlite3
from rich import box
from typing import List
from rich.table import Table
from datetime import datetime
from rich.console import Console

console = Console()
date = datetime.today().strftime('%d/%m/%Y')

# Model class
class Note:
    def __init__(self, idx, name, content, date_Added):
        self.idx = idx
        self.name = name
        self.content = content
        self.date_Added = date_Added

    def __repr__(self) -> str:
        return f"({self.idx},{self.name}, {self.content}, {self.date_Added})"

conn = sqlite3.connect('notes.db')

c = conn.cursor()

def createTable():
    c.execute(""" CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title text,
            content text,
            dateAdded text
        )""")


createTable()


def createNote(note: Note):
    with conn:
        c.execute("INSERT INTO notes(title, content, dateAdded) VALUES( :title, :content, :dateAdded)", {
                  'title': note.name, 'content': note.content, 'dateAdded': note.date_Added})
        conn.commit()


def showNote():
    c.execute("SELECT  * from notes")
    rows = c.fetchall()
    for row in rows:
        print(row)


def updateNote(noteName: str, newName: str):
    with conn:
        c.execute('''UPDATE notes SET title = ? WHERE title LIKE ? ''',
                  (newName, noteName,))
        conn.commit()


def updateContent(noteName: str, newContent: str):
    with conn:
        c.execute('''UPDATE notes SET content = ? WHERE title LIKE ? ''',
                  (newContent, noteName,))
        conn.commit()


def deleteNote(noteName: str):
    with conn:
        c.execute('''DELETE FROM notes WHERE title LIKE ? ''', (noteName,))
        conn.commit()


def get_all_notes() -> List[Note]:
    c.execute("SELECT * from notes")
    results = c.fetchall()
    notes = []
    for result in results:
        notes.append(Note(*result))
    return notes


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    console.print(" 1 --> New note", style="orchid2")
    console.print(" 2 --> Edit note", style="pale_violet_red1")
    console.print(" 3 --> Edit content", style="light_coral")
    console.print(" 4 --> Delete note", style="red3")

def App():
    clear()
    # Creating table using Rich
    table = Table(title="Al-Kitaab", title_style="indian_red1", style="indian_red1", box=box.ROUNDED)
    
    table.add_column("🌵", style="orange3")
    table.add_column("Name", style="orchid1", header_style="orange3")
    table.add_column("Content", style="medium_spring_green",header_style="orange3")
    table.add_column("Date", style="yellow1",justify="center", header_style="orange3")
    
    # query all notes from database
    Notes = get_all_notes()
    for idx, task in enumerate(Notes, start=1):
        table.add_row(str(idx), task.name, task.content[:30], task.date_Added)
    console.print(table)
    
    print("\n")
    menu()
    
    response = input(" 🦄 ")
    
    if int(response) == 1:
        idx = 0
        NoteName = input(" Name: ")
        NoteContent = input(" Content: ")
        note = Note(idx, NoteName, NoteContent, date)
        createNote(note)
        clear()
        App()
    elif int(response) == 2:
        name_input = str(input(" Note name:"))
        etc = '%'
        note_name = name_input+etc
        new_name = str(input(" New name: "))
        updateNote(note_name, new_name)
        clear()
        App()
    elif int(response) == 3:
        name_input = str(input(" Note name:"))
        etc = '%'
        note_name = name_input+etc
        new_content = str(input(" New content: "))
        updateContent(note_name, new_content)
        clear()
        App()
    elif int(response) == 4:
        name_input = str(input(" Note name:"))
        etc = '%'
        note_name = name_input+etc
        deleteNote(note_name)
        clear()
        App()
    else:
        print("\n")
        console.print("oops! invalid input 😓", style="orchid2")
        console.print("type 1 to Create a new note", style="orchid2")
        console.print("type 2 to Edit note", style="orchid2")
        console.print("type 3 to Edit note content", style="orchid2")
        console.print("type 4 to Delete note", style="orchid2")


if __name__ == "__main__":
    try:
        App()
    except KeyboardInterrupt:
        clear()
        sys.exit(0)
