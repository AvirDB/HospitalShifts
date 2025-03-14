# מערכת שיבוץ משמרות לבית חולים - גרסה פשוטה

מערכת לניהול ושיבוץ משמרות אוטומטי עבור מחלקות בית החולים, תוך התחשבות בכל הכללים והמגבלות הנדרשים.
גרסה זו משתמשת רק בספריות הבסיסיות של Python, ללא צורך בהתקנת חבילות נוספות.

## דרישות מערכת

- Python 3.8 ומעלה (ללא צורך בחבילות נוספות)

## שימוש

1. הרץ את הסקריפט:
```bash
python simple_hospital_shifts.py
```

2. הסקריפט ייצור שני קבצי CSV:
   - `hospital_shifts_december_2024.csv`: טבלת המשמרות החודשית
   - `hospital_shifts_summary_december_2024.csv`: טבלת סיכום לכל עובד

## מאפייני המערכת

- שיבוץ אוטומטי תוך שמירה על כל כללי השיבוץ
- התחשבות במגבלות סופי שבוע
- מעקב אחר כמות משמרות לעובד
- תמיכה מלאה בעברית
- סיכום סטטיסטי לכל עובד

## כללי שיבוץ

1. מגבלות משמרות:
   - מקסימום 6-7 משמרות בחודש לעובד
   - מקסימום משמרת אחת בסוף שבוע (במקרים חריגים עד 2)
   - אין משמרות רצופות

2. מגבלות עובדים:
   - עובדים מתחילים לא יכולים לעבוד במקביל
   - שמירה על איזון בכמות המשמרות בין העובדים

3. יכולות עבודה:
   - עובדי חדר לידה יכולים לעבוד בכל המחלקות
   - עובדי מיון נשים יכולים לעבוד גם במיון יולדות
   - עובדי מיון יולדות עובדים רק במחלקתם

## פתיחת קבצי CSV
ניתן לפתוח את קבצי ה-CSV באמצעות:
- Microsoft Excel
- Google Sheets
- LibreOffice Calc
- כל תוכנת גיליונות אלקטרוניים אחרת שתומכת ב-CSV

הערה: בעת פתיחת הקבצים ב-Excel, יש לוודא שבחרתם בקידוד UTF-8 כדי שהטקסט בעברית יוצג כראוי. 