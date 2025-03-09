import csv
from datetime import datetime, timedelta
import calendar
import os

# Define departments and workers
DEPARTMENTS = {
    'מיון יולדות': ['עמית', 'גלינה', 'אורים', 'יוני כהן'],
    'מיון נשים': ['גל כהן', 'קוצוק', 'אבוגנים', 'ליבובץ', 'לוין', 'קרטס'],
    'חדר לידה': ['חריש', 'טרסוב', 'מזרחי', 'קציר', 'זמיר', 'אברהמי', 'רביב', 'זומרפרוינד']
}

BEGINNERS = ['עמית', 'גלינה', 'אורים', 'זומרפרוינד']

# Worker capabilities
WORKER_CAPABILITIES = {}

# Initialize capabilities for all workers
for dept, workers in DEPARTMENTS.items():
    for worker in workers:
        if worker not in WORKER_CAPABILITIES:
            WORKER_CAPABILITIES[worker] = []
        WORKER_CAPABILITIES[worker].append(dept)
        
        # Workers from חדר לידה can work everywhere
        if dept == 'חדר לידה':
            WORKER_CAPABILITIES[worker].extend(['מיון יולדות', 'מיון נשים'])
        # Workers from מיון נשים can also work in מיון יולדות
        elif dept == 'מיון נשים':
            WORKER_CAPABILITIES[worker].append('מיון יולדות')

# Remove duplicates from capabilities
for worker in WORKER_CAPABILITIES:
    WORKER_CAPABILITIES[worker] = list(set(WORKER_CAPABILITIES[worker]))

class ShiftScheduler:
    def __init__(self):
        self.shifts = {}  # date -> {department -> worker}
        self.worker_shifts_count = {worker: 0 for dept in DEPARTMENTS.values() for worker in dept}
        self.worker_weekend_shifts = {worker: 0 for dept in DEPARTMENTS.values() for worker in dept}
        self.last_shift_date = {worker: None for dept in DEPARTMENTS.values() for worker in dept}
    
    def can_assign_shift(self, worker, date, department):
        # Check if worker can work in this department
        if department not in WORKER_CAPABILITIES[worker]:
            return False
            
        # Check if worker already has a shift on this date
        if date in self.shifts and any(worker == assigned_worker 
                                     for dept, assigned_worker in self.shifts[date].items()):
            return False
            
        # Check if worker had a shift yesterday
        yesterday = date - timedelta(days=1)
        if yesterday in self.shifts and any(worker == assigned_worker 
                                          for dept, assigned_worker in self.shifts[yesterday].items()):
            return False
            
        # Check monthly shift limit (6-7 shifts)
        if self.worker_shifts_count[worker] >= 7:
            return False
            
        # Check weekend shift limit (max 2)
        is_weekend = date.weekday() in [4, 5]  # Friday = 4, Saturday = 5
        if is_weekend and self.worker_weekend_shifts[worker] >= 2:
            return False
            
        # Check beginners constraint
        if worker in BEGINNERS:
            if date in self.shifts:
                for dept, assigned_worker in self.shifts[date].items():
                    if assigned_worker in BEGINNERS:
                        return False
        
        return True
    
    def assign_shift(self, date, department):
        available_workers = [
            worker for worker in WORKER_CAPABILITIES.keys()
            if self.can_assign_shift(worker, date, department)
        ]
        
        if not available_workers:
            return None
            
        # Sort workers by shift count to maintain balance
        available_workers.sort(key=lambda w: (self.worker_shifts_count[w], self.worker_weekend_shifts[w]))
        worker = available_workers[0]
        
        if date not in self.shifts:
            self.shifts[date] = {}
        
        self.shifts[date][department] = worker
        self.worker_shifts_count[worker] += 1
        if date.weekday() in [4, 5]:  # Friday = 4, Saturday = 5
            self.worker_weekend_shifts[worker] += 1
        self.last_shift_date[worker] = date
        
        return worker

def create_shifts_schedule():
    # Create a date range for December 2024
    start_date = datetime(2024, 12, 1)
    dates = []
    current_date = start_date
    while current_date.month == 12:
        dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Initialize scheduler
    scheduler = ShiftScheduler()
    
    # Assign shifts for each date
    for date in dates:
        for department in ['מיון יולדות', 'מיון נשים', 'חדר לידה']:
            scheduler.assign_shift(date, department)
    
    # Create shifts CSV file
    with open('hospital_shifts_december_2024.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # Write headers
        writer.writerow(['תאריך', 'יום', 'מיון יולדות', 'מיון נשים', 'חדר לידה'])
        
        # Hebrew days mapping
        hebrew_days = {
            0: 'שני',
            1: 'שלישי',
            2: 'רביעי',
            3: 'חמישי',
            4: 'שישי',
            5: 'שבת',
            6: 'ראשון'
        }
        
        # Write shifts data
        for date in dates:
            row = [
                date.strftime('%d/%m/%Y'),
                hebrew_days[date.weekday()],
                scheduler.shifts[date].get('מיון יולדות', ''),
                scheduler.shifts[date].get('מיון נשים', ''),
                scheduler.shifts[date].get('חדר לידה', '')
            ]
            writer.writerow(row)
    
    # Create summary CSV file
    with open('hospital_shifts_summary_december_2024.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        
        # Write headers
        writer.writerow(['שם העובד', 'מחלקה', 'סה"כ משמרות', 'משמרות סופ"ש'])
        
        # Write summary data
        for dept, workers in DEPARTMENTS.items():
            for worker in workers:
                writer.writerow([
                    worker,
                    dept,
                    scheduler.worker_shifts_count[worker],
                    scheduler.worker_weekend_shifts[worker]
                ])

    print("קבצי השיבוץ נוצרו בהצלחה:")
    print("1. hospital_shifts_december_2024.csv - טבלת המשמרות")
    print("2. hospital_shifts_summary_december_2024.csv - טבלת סיכום")

if __name__ == "__main__":
    create_shifts_schedule() 