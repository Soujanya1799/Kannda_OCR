import os
from ultralytics import YOLO
import multiprocessing

def main():
    base_path = r"C:\Users\SAMSUNG\C_Drive\Capstone_Project\dataset\nali_kali\data"
    output_txt_file = "output.txt"  # Output text file to save detected class names
    folders = os.listdir(base_path)

    with open(output_txt_file, 'w', encoding='utf-8') as f_out:
        for folder_ in folders:
            folder_path = os.path.join(base_path, folder_)
            
            # Check if folder path exists
            if not os.path.exists(folder_path):
                print(f"Path {folder_path} does not exist. Skipping...")
                continue
            
            # Initialize the YOLO model
            model = YOLO("yolov8/v8_10000_150.pt", 'detect')
            
            try:
                # Perform prediction
                results = model.predict(source=folder_path, conf=0.7, save=True, save_conf=True)
                
                for result in results:
                    if result.boxes is None or len(result.boxes) == 0:
                        print(f"No objects detected in {folder_path}.")
                        continue
                    
                    # Extract and sort boxes by y-coordinate and then by x-coordinate
                    boxes_sorted = []
                    for box in result.boxes:
                        try:
                            if box.xyxy.ndim == 2 and box.xyxy.shape[1] == 4:
                                x1, y1, x2, y2 = box.xyxy[0].tolist()
                                detected_class = model.names[int(box.cls)]
                                boxes_sorted.append((x1, y1, x2, y2, detected_class))
                            else:
                                print(f"Unexpected box shape: {box.xyxy.shape}")
                        except Exception as e:
                            print(f"Error processing box: {e}")

                    # Sort boxes by y-coordinate (top to bottom), then x-coordinate (left to right)
                    boxes_sorted = sorted(boxes_sorted, key=lambda b: (b[1], b[0]))

                    lines = []
                    current_line = []
                    last_y = None
                    threshold = 15  # Adjust this threshold based on your image layout
                    
                    # Group boxes into lines based on proximity of their y-coordinates
                    for x1, y1, x2, y2, detected_class in boxes_sorted:
                        if last_y is None or y1 < last_y + threshold:
                            current_line.append((x1, detected_class))  # Keep x1 for sorting within the line
                            last_y = y1
                        else:
                            # Sort the current line by x-coordinate (left to right) before appending to lines
                            current_line_sorted = sorted(current_line, key=lambda b: b[0])
                            lines.append([cls for _, cls in current_line_sorted])
                            current_line = [(x1, detected_class)]
                            last_y = y1
                    
                    if current_line:
                        current_line_sorted = sorted(current_line, key=lambda b: b[0])
                        lines.append([cls for _, cls in current_line_sorted])
                    
                    # Write detected classes to output file in the order they appear
                    f_out.write(f"Image: {folder_}\n")
                    for line in lines:
                        f_out.write(' '.join(line) + '\n')
                    f_out.write('\n')

            except Exception as e:
                print(f"An error occurred while processing {folder_path}: {e}")

if __name__ == '__main__':
    # Add freeze_support() to handle multiprocessing in Windows
    multiprocessing.freeze_support()
    
    main()
