from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error

@dataclass
class Reminder:
    EMAIL = "email"
    SYSTEM = "system"
    
    date_time: datetime
    type:str = EMAIL

    def __str__(self) ->str:
        return f"Reminder on {self.date_time} of type {type}"

@dataclass
class Event:
    title: str
    description: str
    date_: datetime.date
    start_at: datetime.time
    end_at: datetime.time
    id: str = field(default_factory=generate_unique_id)
    reminders: list['Reminder'] = field(default_factory=list)

    def __str__(self) -> str:
        return f"ID: {self.id}\nEvent title: {self.title}\nDescription: {self.description}\nTime: {self.start_at} - {self.end_at}"

    def add_reminder(self, date_time: datetime, type_: str = Reminder.EMAIL) -> None:
        reminder = Reminder(date_time, type_)
        self.reminders.append(reminder)

    def delete_reminder(self, reminder_index: int) -> None:
        if 0 <= reminder_index < len(self.reminders):
            self.reminders.pop(reminder_index)
        else:
            reminder_not_found_error()

class Day:
    def __init__(self, date_: datetime.date):
        self.date_ = date_
        self.slots: dict[datetime.time, str | None] = {}
        self._init_slots()

    def _init_slots(self) -> None:
        for hour in range(24):
            for minute in range(0, 60, 15):
                self.slots[time(hour, minute)] = None

    def add_event(self, event_id: str, start_at: datetime.time, end_at: datetime.time) -> None:
        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id

    def delete_event(self, event_id: str) -> None:
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: datetime.time, end_at: datetime.time) -> None:
        for slot in self.slots:
            if self.slots[slot] == event_id:
                self.slots[slot] = None

        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot]:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id
