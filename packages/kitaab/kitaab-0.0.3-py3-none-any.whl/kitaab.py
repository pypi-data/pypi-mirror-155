import os
import sys

from datetime import datetime
from rich.console import Console



import sqlite3

from typing import List
import os
from github import Github

from rich.console import Console
import os

from rich.console import Console
from rich.columns import Columns
from rich import box, print
from rich.panel import Panel
from rich.table import Table

console = Console()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def error():
    console.print("oops! invalid input 😓", style="orchid2")
    console.print("type 1 to Create a new note", style="orchid2")
    console.print("type 2 to Edit note", style="orchid2")
    console.print("type 3 to Edit note content", style="orchid2")
    console.print("type 4 to Delete note", style="orchid2")


def menu():
    print("\n")
    console.print(" 1 --> New note", style="orchid2")
    console.print(" 2 --> Edit name", style="pale_violet_red1")
    console.print(" 3 --> Edit content", style="light_coral")
    console.print(" 4 --> Delete note", style="red3")


def Help():
    console.print(
        " type add-token --> setup github integration ", style="red3")
    console.print(" type board --> view notes as board ", style="light_coral")
    console.print(" type quit or q -->  to exit ", style="pale_violet_red1")


def printTable():
    # Creating table using Rich
    table = Table(title="Al-kitaab", title_style="indian_red1",
                  style="indian_red1", box=box.ROUNDED)

    table.add_column("🌵", style="orange3")
    table.add_column("Name", style="orchid1", header_style="orange3")
    table.add_column("Content", style="medium_spring_green",
                     header_style="orange3")
    table.add_column("Last Modified", style="yellow1",
                     justify="center", header_style="orange3")

    # get all notes from database
    notes = get_all_notes()
    for idx, note in enumerate(notes, start=1):
        table.add_row(str(idx), note.name, note.content[:30], note.date_Added)
    console.print(table)


# BOARD VIEW
# getting content for board view
def get_content(user):
    content = user["content"]
    name = user["title"]
    return f"[medium_spring_green]{content}\n[orchid1]{name}"


# build board with Rich
def printBoard():
    console = Console()
    users = get_dict()
    if users == []:
        console.print("notebook is empty", style='yellow3')
    else:
        user_renderables = [Panel(get_content(
            user), expand=True,  border_style="indian_red1")for user in users]
        console.print(Columns(user_renderables))



class Note:
    def __init__(self, idx, name, content, date_Added):
        self.idx = idx
        self.name = name
        self.content = content
        self.date_Added = date_Added

    def __repr__(self) -> str:
        return f"({self.idx},{self.name}, {self.content}, {self.date_Added})"

# connect to database
conn = sqlite3.connect('notes.db')

# create a cursor
c = conn.cursor()

# create a table


def createTable():
    c.execute(""" CREATE TABLE IF NOT EXISTS notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title text,
            content text,
            dateAdded text
        )""")


createTable()


def tokenTable():
    c.execute(""" CREATE TABLE IF NOT EXISTS Token(
            token text
        )""")


tokenTable()


def dropToken():
    with conn:
        c.execute(""" DROP TABLE IF EXISTS Token """)
        conn.commit()


def addToken(mytoken: str):
    dropToken()
    tokenTable()
    with conn:
        c.execute("INSERT INTO Token(token) VALUES(:token)",
                  {'token': mytoken})
        conn.commit()


def showToken():
    tokenTable()
    with conn:
        c.execute("SELECT token from Token")
        tokens = None
        tokens = c.fetchone()
        if tokens != None:
            for token in tokens:
                return token
        else:
            return tokens


def createNote(note: Note):
    with conn:
        c.execute("INSERT INTO notes(title, content, dateAdded) VALUES( :title, :content, :dateAdded)", {
                  'title': note.name, 'content': note.content, 'dateAdded': note.date_Added})
        conn.commit()


# to access specific note content
def getNote(new_name: str):
    with conn:
        c.execute('''SELECT content from notes WHERE title LIKE ?''', (new_name,))
        rows = c.fetchone()
        for row in rows:
            return row


def updateNote(noteName: str, newName: str, newDate: str):
    with conn:
        c.execute('''UPDATE notes SET title = ? WHERE title LIKE ? ''',
                  (newName, noteName,))
        conn.commit()
    with conn:
        c.execute(
            '''UPDATE notes SET dateAdded = ? WHERE title LIKE ? ''', (newDate, newName,))
        conn.commit()


def updateContent(noteName: str, newContent: str, newDate: str):
    with conn:
        c.execute('''UPDATE notes SET content = ? WHERE title LIKE ? ''',
                  (newContent, noteName,))
        conn.commit()
    with conn:
        c.execute(
            '''UPDATE notes SET dateAdded = ? WHERE title LIKE ? ''', (newDate, noteName,))
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


def get_dict():
    with conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute("SELECT * FROM notes")
        rows = curs.fetchall()
        Dict = []
        for row in rows:
            Dict.append(dict(row))
        return Dict


# Token
key = showToken()
token = os.getenv('GITHUB_TOKEN', key)
g = Github(token)
user = g.get_user()

# checking if token entered by user is valid or not


def checkTokenValidity():
    token_valid = "false"
    key = showToken()
    token = os.getenv('GITHUB_TOKEN', key)
    g = Github(token)
    user = g.get_user()
    try:
        if key != None:
            console.print(
                f"your github account is [yellow3]{user.login}[/]", style="red")
            token_valid = "true"
            return token_valid
    except:
        return token_valid


# checking if kitaab repository exists
def checkRepoExist():
    exist = "false"
    try:
        repo = user.get_repo("My-Kitaab")
        exist = "true"
        return exist
    except:
        return exist


repoExist = checkRepoExist()


# create note
def createGithubNote(noteName: str, noteContent: str):
    if key != None:
        repo = user.get_repo("My-Kitaab")
        repo.create_file(noteName, "added new note", noteContent)


# create repo
def createGithubRepo():
    if key != None and repoExist == 'false':
        print("please wait...")
        repo = user.create_repo("My-Kitaab")
        repo.create_file("readme.md", "add readme",
                         "## This repository is auto created by a note-taking app named kitaab.<br/>learn more https://github.com/Fareed-Ahmad7/Kitaab")
        notes = get_all_notes()
        for note in notes:
            createGithubNote(note.name, note.content)


createGithubRepo()


# edit note name
def editGithubNoteName(noteName: str, newName: str):
    if key != None:
        repo = user.get_repo("My-Kitaab")
        file = repo.get_contents(noteName)
        repo.delete_file(file.path, "deleted note", file.sha)
        noteContent = getNote(newName)
        createGithubNote(newName, noteContent)


# edit note content
def editGithubNoteContent(noteName, newContent):
    if key != None:
        repo = user.get_repo("My-Kitaab")
        file = repo.get_contents(noteName)
        repo.update_file(file.path, "edited note content",
                         newContent, file.sha)


# delete note
def deleteGithubNote(noteName: str):
    if key != None:
        repo = user.get_repo("My-Kitaab")
        file = repo.get_contents(noteName)
        repo.delete_file(file.path, "deleted note", file.sha)



def loop():

    response = input("🦄 ")

    try:
        # Help
        if response == 'help':
            Help()
            loop()

        # Quit
        elif response == 'quit' or response == 'q':
            console.print("exited successfully!", style="orchid1")
            os._exit(0)

        # Board
        elif response == 'board':
            printBoard()
            loop()

        # Add Token
        elif response == 'add-token':
            console.print("Adding token requires restart!", style="yellow3")
            token = input("Enter github personal access token: ")
            addToken(token)
            tokenValid = checkTokenValidity()
            if tokenValid == "false":
                dropToken()
                console.print("[red]Invalid token[/] -- please check your token or add a new one", style="light_coral")

        # Create Note
        elif int(response) == 1:
            idx = 0
            note_name = input("Name: ")
            note_content = input("Content: ")
            date = datetime.today().strftime('%d/%b/%H:%M')
            note = Note(idx, note_name, note_content, date)
            createNote(note)
            createGithubNote(note_name, note_content)
            clear()
            app()

        # Update Note Name
        elif int(response) == 2:
            note_name = str(input("Note name: "))
            new_name = str(input("New name: "))
            date = datetime.today().strftime('%d/%b/%H:%M')
            updateNote(note_name, new_name, date)
            editGithubNoteName(note_name, new_name)
            clear()
            app()

        # Update Note Content
        elif int(response) == 3:
            note_name = str(input("Note name: "))
            new_content = str(input("New content: "))
            date = datetime.today().strftime('%d/%b/%H:%M')
            updateContent(note_name, new_content, date)
            editGithubNoteContent(note_name, new_content)
            clear()
            app()

        # Delete Note
        elif int(response) == 4:
            note_name = str(input("Note name: "))
            deleteNote(note_name)
            deleteGithubNote(note_name)
            clear()
            app()

        else:
            error()
            loop()
    except:
        console.print("oops! invalid text input 😓", style="orchid2")
        console.print("use [orchid2]help[/] to list all existing input", style="indian_red1")
        loop()


def app():
    clear()
    printTable()
    menu()
    loop()


if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        clear()
        sys.exit(0)
