from dataclasses import dataclass, field
from datetime import datetime, date, time
from app.services.util import generate_unique_id, reminder_not_found_error, slot_not_available_error, \
    event_not_found_error, date_lower_than_today_error

@dataclass
class Reminder:
    EMAIL = "email"
    SYSTEM = "system"

    date_time: datetime
    type: str = field(default=EMAIL)

    def __str__(self):
        return f"Reminder on {self.date_time} of type {self.type}"

@dataclass
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: list[Reminder] = field(default_factory=list)
    id: str = field(default_factory=generate_unique_id)

    def add_reminder(self, date_time: datetime, type_: str = Reminder.EMAIL):
        self.reminders.append(Reminder(date_time, type_))

    def delete_reminder(self, reminder_index: int):
        if 0 <= reminder_index < len(self.reminders):
            del self.reminders[reminder_index]
        else:
            reminder_not_found_error()

class Day:
    def __init__(self, date_: date):
        self.date_ = date_
        self.slots: dict[time, str | None] = {}
        self._init_slots()

    def _init_slots(self):
        current_time = time(0, 0)
        end_time = time(23, 45)
        while current_time <= end_time:
            self.slots[current_time] = None
            hours = current_time.hour
            minutes = current_time.minute + 15
            if minutes >= 60:
                hours += 1
                minutes -= 60
            current_time = time(hours, minutes)

    def add_event(self, event_id: str, start_at: time, end_at: time):
        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot] is not None:
                    slot_not_available_error()
                else:
                    self.slots[slot] = event_id





