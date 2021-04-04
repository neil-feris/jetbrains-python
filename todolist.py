from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///todo.db?check_same_thread=False")
Base = declarative_base()


class Table(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_row(task, deadline=datetime.today()):
    row = Table(
        task=task,
        deadline=deadline
    )
    session.add(row)


def todays_tasks(deadline=datetime.today()):
    rows = session.query(Table).filter(Table.deadline == deadline.date()).all()
    print(f"Today {deadline.day} {deadline:%b}:")
    if not rows:
        print('Nothing to do!\n')
    for i, row in enumerate(rows, 1):
        print(f'{i}. {row.task}')
    print()


def weeks_tasks(deadline=datetime.today()):
    days = [datetime.today() + timedelta(i) for i in range(7)]
    for day in days:
        rows = session.query(Table).filter(Table.deadline == day.date()).all()
        print(f"{day:%A} {day.day} {day:%b}:")
        if not rows:
            print('Nothing to do!\n')
        for i, row in enumerate(rows, 1):
            print(f'{i}. {row.task}')
        print()


def all_tasks(deadline=datetime.today()):
    rows = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    if not rows:
        print('Nothing to do!\n')
    for i, row in enumerate(rows, 1):
        print(f'{i}. {row.task}. {row.deadline.day} {row.deadline:%b}')
    print('')


def missed_tasks(deadline=datetime.today()):
    print('Missed tasks:')
    rows = session.query(Table).filter(Table.deadline < deadline.date()).order_by(Table.deadline).all()
    if not rows:
        print('Nothing is missed')
    else:
        for i, row in enumerate(rows, 1):
            print(f'{i}. {row.task}. {row.deadline.day} {row.deadline:%b}')
    print()

def delete_task():
    rows = session.query(Table).all()
    for i, row in enumerate(rows, 1):
        print(f'{i}. {row.task}. {row.deadline.day} {row.deadline:%b}')
    row_num = int(input('Choose the number of the task you want to delete:'))
    row = list(enumerate(rows, 1))[row_num-1][1]
    session.delete(row)
    print('The task has been deleted!\n')
    session.commit()



def add_task():
    task = input('Enter task \n>')
    task_deadline = input('Enter the date YYYY-MM-DD')
    task_datetime = datetime.strptime(task_deadline, '%Y-%m-%d')
    add_row(task, task_datetime)
    print('Task added')
    session.commit()



def print_menu():
    print(
        """1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
"""
    )


selection = '1'
while int(selection) != 0:
    print_menu()
    selection = int(input())
    if selection == 1:
        todays_tasks()
    elif selection == 2:
        weeks_tasks()
    elif selection == 3:
        all_tasks()
    elif selection == 4:
        missed_tasks()
    elif selection == 5:
        add_task()
    elif selection == 6:
        delete_task()
print('Bye!')
