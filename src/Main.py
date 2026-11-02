import sys

from ShapeFactory import ShapeFactory
from ProjectionEngine import ProjectionEngine
from OpenCvVideoWriter import OpenCvVideoWriter
from NrrdReader import NrrdReader


def main():
    if len(sys.argv) < 4:
        print("Usage: python main.py <file.nrrd> <file.csv> <file.mp4>")
        sys.exit(1)

    nrrd_file = sys.argv[1]
    csv_file = sys.argv[2]
    mp4_file = sys.argv[3]

    # 1. טעינת הנתונים (Volume Manager)
    volume = NrrdReader.load(nrrd_file)

    # 2. פיענוח ה-CSV (Geometry Factory)
    planes = []
    print(f"[Facade] Parsing shapes from {csv_file}...")
    with open(csv_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            try:
                # פיצול השורה למחרוזות
                raw_parts = line.split(',')

                # אם יש שורות ריקות בסוף ה-CSV מהאקסל, נדלג עליהן
                if len(raw_parts) < 10:
                    continue

                # המרה למספרים (יזרוק ValueError בשורת הכותרת ויתפס ב-except)
                parts = [float(x) for x in raw_parts if x.strip() != '']

                # עמודה ראשונה היא כמות הנקודות (3 או 4)
                num_points = int(parts[0])

                # חיתוך הרשימה כך שתכיל רק את הקואורדינטות (בלי העמודה הראשונה)
                if num_points == 3:
                    coords = parts[1:10]  # שולף 9 קואורדינטות
                elif num_points == 4:
                    coords = parts[1:13]  # שולף 12 קואורדינטות
                else:
                    print(f"[Warning] Unknown number of points ({num_points}) on row {line_num}")
                    continue

                # יצירת הצורה והוספתה לרשימה
                shape = ShapeFactory.create_shape(coords)
                planes.append(shape)

            except ValueError:
                # תפיסה אלגנטית של שורת הכותרת (טקסט לא יכול להפוך ל-float)
                print(f"[Facade] Skipping header text on row {line_num}")
            except Exception as e:
                # תפיסה של צורות לא חוקיות גיאומטרית
                print(f"[Warning] Skipping invalid shape on row {line_num}: {e}")

    if not planes:
        print("[Facade] No valid planes parsed. Exiting.")
        sys.exit(1)

    # מציאת הממדים המקסימליים לקנבס הוידאו
    max_w = max([p.W for p in planes])
    max_h = max([p.H for p in planes])
    if max_w % 2 != 0: max_w += 1
    if max_h % 2 != 0: max_h += 1

    # 3. אתחול מחוללי האלגוריתם והוידאו (Engine & Video Exporter)
    engine = ProjectionEngine()
    video_exporter = OpenCvVideoWriter(mp4_file, max_w, max_h)

    # 4. תזמור (Orchestration): רץ על המישורים, מעבד ושומר
    print(f"[Facade] Processing {len(planes)} shapes...")
    for i, plane in enumerate(planes, 1):
        # הקסם קורה כאן - הפעלת האלגוריתם המהיר
        projected_frame = engine.project(volume, plane)

        # שמירה לוידאו
        video_exporter.add_frame(projected_frame, duration_sec=3)
        print(f" -> Processed plane {i}/{len(planes)}")

    video_exporter.release()
    print(f"Done! Video saved to: {mp4_file}")


if __name__ == "__main__":
    main()