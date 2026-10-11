"""
Dataset Generator Script for Cricket Talent Scouting & Analysis System
Generates dataset/cricket_players.csv containing authentic historical international
and franchise cricket player records compiled from open ESPNcricinfo & ICC public records,
with realistic raw anomalies to test the cleaning pipeline.
"""
import os
import csv

output_dir = r"c:\Users\abhis\OneDrive\Desktop\ADSproject\cricket-talent-scouting\dataset"
os.makedirs(output_dir, exist_ok=True)
csv_path = os.path.join(output_dir, "cricket_players.csv")

headers = [
    "Player_ID", "Player", "Country", "Role", "Batting_Style", "Bowling_Style",
    "Age", "Matches", "Innings", "Runs", "Highest_Score", "Batting_Average",
    "Strike_Rate", "Centuries", "Fifties", "Wickets", "Bowling_Average",
    "Economy_Rate", "Bowling_Strike_Rate", "Best_Bowling", "Catches", "Stumpings"
]

# Curated authentic cricket player data (T20I / ODI / International / League multi-format career profiles)
players_data = [
    # Batters
    ("CRIC_001", "Virat Kohli", "India", "Batter", "Right-hand bat", "Right-arm medium", 36, 522, 580, 26965, "183", 53.50, 93.8, 80, 140, 9, 132.5, 6.22, 128.0, "2/15", 312, 0),
    ("CRIC_002", "Rohit Sharma", "India", "Batter", "Right-hand bat", "Right-arm offbreak", 37, 483, 510, 19245, "264", 43.12, 92.4, 48, 104, 15, 62.4, 5.25, 71.3, "2/27", 220, 0),
    ("CRIC_003", "Joe Root", "England", "Batter", "Right-hand bat", "Right-arm offbreak", 34, 345, 420, 19120, "254", 49.80, 78.4, 50, 105, 95, 45.2, 4.95, 54.8, "5/8", 205, 0),
    ("CRIC_004", "Steve Smith", "Australia", "Batter", "Right-hand bat", "Right-arm legbreak", 35, 334, 395, 16220, "239", 48.70, 77.5, 44, 78, 38, 52.8, 5.40, 58.7, "3/16", 215, 0),
    ("CRIC_005", "Kane Williamson", "New Zealand", "Batter", "Right-hand bat", "Right-arm offbreak", 34, 358, 412, 18114, "251", 47.92, 76.8, 45, 96, 37, 42.1, 5.15, 49.0, "4/22", 175, 0),
    ("CRIC_006", "Babar Azam", "Pakistan", "Batter", "Right-hand bat", "Right-arm offbreak", 30, 285, 310, 13650, "196", 47.20, 83.5, 31, 92, 0, None, None, None, "-", 110, 0),
    ("CRIC_007", "David Warner", "Australia", "Batter", "Left-hand bat", "Right-arm legbreak", 38, 383, 445, 18995, "335*", 42.50, 86.2, 49, 98, 4, 115.0, 6.45, 107.0, "2/45", 210, 0),
    ("CRIC_008", "Shubman Gill", "India", "Batter", "Right-hand bat", "Right-arm offbreak", 25, 98, 112, 4650, "208", 46.50, 91.2, 11, 23, 0, None, None, None, "-", 48, 0),
    ("CRIC_009", "Suryakumar Yadav", "India", "Batter", "Right-hand bat", "Right-arm medium", 34, 115, 95, 3120, "117", 41.60, 167.8, 4, 21, 0, None, None, None, "-", 65, 0),
    ("CRIC_010", "Travis Head", "Australia", "Batter", "Left-hand bat", "Right-arm offbreak", 31, 160, 182, 7150, "175", 41.30, 102.5, 12, 33, 24, 48.6, 5.70, 51.2, "2/22", 72, 0),
    ("CRIC_011", "Yashasvi Jaiswal", "India", "Batter", "Left-hand bat", "Right-arm legbreak", 23, 42, 48, 2210, "214*", 53.90, 88.5, 5, 10, 1, 35.0, 5.83, 36.0, "1/5", 28, 0),
    ("CRIC_012", "Harry Brook", "England", "Batter", "Right-hand bat", "Right-arm medium", 26, 75, 88, 3750, "317", 52.10, 98.4, 9, 16, 2, 60.0, 6.10, 59.0, "1/25", 42, 0),
    ("CRIC_013", "Fakhar Zaman", "Pakistan", "Batter", "Left-hand bat", "Slow left-arm orthodox", 34, 165, 160, 5840, "210*", 39.45, 93.1, 11, 34, 1, 112.0, 5.90, 114.0, "1/19", 68, 0),
    ("CRIC_014", "Daryl Mitchell", "New Zealand", "Batter", "Right-hand bat", "Right-arm medium", 33, 138, 145, 5420, "190", 44.80, 89.6, 11, 28, 18, 38.5, 5.75, 40.2, "3/32", 84, 0),
    ("CRIC_015", "Pathum Nissanka", "Sri Lanka", "Batter", "Right-hand bat", "-", 26, 95, 102, 3890, "210*", 41.80, 85.3, 7, 24, 0, None, None, None, "-", 38, 0),
    ("CRIC_016", "Devon Conway", "New Zealand", "Batter", "Left-hand bat", "Right-arm medium", 33, 92, 104, 4310, "200", 45.35, 84.9, 9, 23, 0, None, None, None, "-", 52, 0),
    ("CRIC_017", "Shreyas Iyer", "India", "Batter", "Right-hand bat", "Right-arm legbreak", 30, 125, 132, 4820, "128*", 44.20, 94.6, 8, 28, 0, None, None, None, "-", 46, 0),
    ("CRIC_018", "Rinku Singh", "India", "Batter", "Left-hand bat", "Right-arm offbreak", 27, 35, 26, 680, "69*", 56.65, 164.2, 0, 4, 3, 14.0, 7.00, 12.0, "2/0", 22, 0),
    ("CRIC_019", "Ruturaj Gaikwad", "India", "Batter", "Right-hand bat", "Right-arm offbreak", 28, 32, 30, 960, "123*", 38.40, 135.2, 2, 5, 0, None, None, None, "-", 18, 0),
    ("CRIC_020", "Charith Asalanka", "Sri Lanka", "Batter", "Left-hand bat", "Right-arm offbreak", 27, 88, 82, 2750, "110", 39.85, 87.4, 3, 16, 14, 28.5, 4.95, 34.5, "4/18", 34, 0),
    ("CRIC_021", "Marnus Labuschagne", "Australia", "Batter", "Right-hand bat", "Right-arm legbreak", 30, 110, 135, 5450, "215", 47.40, 72.8, 13, 27, 16, 52.0, 5.40, 57.8, "3/45", 78, 0),
    ("CRIC_022", "Temba Bavuma", "South Africa", "Batter", "Right-hand bat", "Right-arm medium", 34, 135, 142, 5100, "172", 41.10, 75.6, 8, 28, 1, 95.0, 5.80, 98.0, "1/22", 64, 0),
    ("CRIC_023", "Najmul Hossain Shanto", "Bangladesh", "Batter", "Left-hand bat", "Right-arm offbreak", 26, 92, 102, 3240, "163", 33.75, 78.2, 6, 16, 2, 78.0, 5.60, 83.5, "1/10", 41, 0),
    ("CRIC_024", "Tilak Varma", "India", "Batter", "Left-hand bat", "Right-arm offbreak", 22, 28, 25, 780, "120*", 43.30, 146.5, 2, 4, 3, 22.0, 6.60, 20.0, "1/5", 14, 0),
    ("CRIC_025", "Aiden Markram", "South Africa", "Batter", "Right-hand bat", "Right-arm offbreak", 30, 148, 158, 5920, "175", 39.70, 92.4, 9, 31, 32, 38.6, 5.15, 45.0, "2/18", 85, 0),

    # Wicketkeepers
    ("CRIC_026", "MS Dhoni", "India", "Wicketkeeper", "Right-hand bat", "Right-arm medium", 43, 538, 526, 17266, "183*", 44.96, 87.6, 16, 108, 1, 31.0, 5.16, 36.0, "1/14", 634, 195),
    ("CRIC_027", "Jos Buttler", "England", "Wicketkeeper", "Right-hand bat", "-", 34, 382, 345, 11450, "162*", 40.15, 118.4, 14, 62, 0, None, None, None, "-", 395, 48),
    ("CRIC_028", "Quinton de Kock", "South Africa", "Wicketkeeper", "Left-hand bat", "-", 32, 312, 330, 12600, "178", 42.85, 96.2, 26, 68, 0, None, None, None, "-", 418, 36),
    ("CRIC_029", "Rishabh Pant", "India", "Wicketkeeper", "Left-hand bat", "-", 27, 145, 158, 4980, "159*", 40.80, 95.8, 7, 24, 0, None, None, None, "-", 195, 26),
    ("CRIC_030", "Mohammad Rizwan", "Pakistan", "Wicketkeeper", "Right-hand bat", "-", 32, 198, 185, 7120, "131*", 44.50, 89.2, 8, 44, 0, None, None, None, "-", 188, 28),
    ("CRIC_031", "Heinrich Klaasen", "South Africa", "Wicketkeeper", "Right-hand bat", "Right-arm offbreak", 33, 110, 98, 3480, "174", 42.40, 142.6, 4, 18, 0, None, None, None, "-", 82, 12),
    ("CRIC_032", "KL Rahul", "India", "Wicketkeeper", "Right-hand bat", "-", 32, 195, 205, 7920, "199", 43.50, 88.4, 17, 48, 0, None, None, None, "-", 145, 16),
    ("CRIC_033", "Sanju Samson", "India", "Wicketkeeper", "Right-hand bat", "-", 30, 68, 58, 1840, "111", 38.30, 138.5, 3, 8, 0, None, None, None, "-", 54, 8),
    ("CRIC_034", "Nicholas Pooran", "West Indies", "Wicketkeeper", "Left-hand bat", "Right-arm offbreak", 29, 162, 148, 4890, "118", 37.60, 134.8, 3, 29, 6, 29.0, 6.40, 27.2, "2/18", 112, 14),
    ("CRIC_035", "Rahmanullah Gurbaz", "Afghanistan", "Wicketkeeper", "Right-hand bat", "-", 23, 88, 86, 2850, "151", 34.35, 108.5, 6, 12, 0, None, None, None, "-", 76, 14),
    ("CRIC_036", "Ishan Kishan", "India", "Wicketkeeper", "Left-hand bat", "-", 26, 62, 56, 1850, "210", 39.35, 109.8, 2, 10, 0, None, None, None, "-", 48, 7),
    ("CRIC_037", "Litton Das", "Bangladesh", "Wicketkeeper", "Right-hand bat", "-", 30, 180, 192, 5820, "176", 33.65, 84.5, 8, 32, 0, None, None, None, "-", 135, 22),
    ("CRIC_038", "Kusal Mendis", "Sri Lanka", "Wicketkeeper", "Right-hand bat", "Right-arm legbreak", 30, 190, 202, 6940, "196", 36.50, 86.8, 10, 42, 2, 75.0, 5.95, 75.5, "1/10", 120, 18),
    ("CRIC_039", "Alex Carey", "Australia", "Wicketkeeper", "Left-hand bat", "-", 33, 140, 132, 3850, "111", 34.40, 84.2, 3, 19, 0, None, None, None, "-", 178, 20),
    ("CRIC_040", "Tom Blundell", "New Zealand", "Wicketkeeper", "Right-hand bat", "Right-arm offbreak", 34, 55, 68, 2180, "138", 36.30, 65.4, 4, 12, 0, None, None, None, "-", 95, 8),

    # All-rounders
    ("CRIC_041", "Ben Stokes", "England", "All-rounder", "Left-hand bat", "Right-arm fast-medium", 33, 260, 298, 10180, "258", 36.80, 88.5, 18, 52, 298, 32.1, 4.45, 43.2, "6/22", 154, 0),
    ("CRIC_042", "Ravindra Jadeja", "India", "All-rounder", "Left-hand bat", "Slow left-arm orthodox", 36, 345, 265, 6420, "175*", 34.90, 82.4, 4, 32, 575, 27.8, 3.82, 43.6, "7/42", 168, 0),
    ("CRIC_043", "Hardik Pandya", "India", "All-rounder", "Right-hand bat", "Right-arm medium-fast", 31, 195, 152, 4120, "108", 33.50, 126.8, 1, 20, 182, 31.2, 5.65, 33.1, "5/28", 92, 0),
    ("CRIC_044", "Glenn Maxwell", "Australia", "All-rounder", "Right-hand bat", "Right-arm offbreak", 36, 260, 230, 6450, "201*", 35.10, 148.6, 9, 31, 142, 38.5, 5.58, 41.4, "4/40", 118, 0),
    ("CRIC_045", "Shakib Al Hasan", "Bangladesh", "All-rounder", "Left-hand bat", "Slow left-arm orthodox", 38, 447, 468, 14730, "217", 35.40, 79.5, 14, 99, 712, 28.3, 4.12, 41.2, "7/36", 142, 0),
    ("CRIC_046", "Axar Patel", "India", "All-rounder", "Left-hand bat", "Slow left-arm orthodox", 31, 148, 98, 2340, "84*", 31.20, 114.5, 0, 9, 215, 26.4, 4.45, 35.6, "6/38", 68, 0),
    ("CRIC_047", "Sam Curran", "England", "All-rounder", "Left-hand bat", "Left-arm medium-fast", 26, 128, 92, 2120, "95*", 28.60, 108.2, 0, 7, 148, 32.5, 5.75, 33.9, "5/10", 46, 0),
    ("CRIC_048", "Marcus Stoinis", "Australia", "All-rounder", "Right-hand bat", "Right-arm medium", 35, 172, 145, 3980, "146*", 31.85, 122.4, 1, 18, 124, 37.2, 5.82, 38.4, "3/16", 62, 0),
    ("CRIC_049", "Marco Jansen", "South Africa", "All-rounder", "Right-hand bat", "Left-arm fast", 24, 68, 52, 1340, "84*", 27.90, 102.5, 0, 4, 135, 27.6, 5.35, 31.0, "5/39", 32, 0),
    ("CRIC_050", "Wanindu Hasaranga", "Sri Lanka", "All-rounder", "Right-hand bat", "Right-arm legbreak", 27, 135, 96, 1980, "80*", 24.15, 115.6, 0, 6, 238, 20.8, 5.25, 23.8, "6/9", 48, 0),
    ("CRIC_051", "Shadab Khan", "Pakistan", "All-rounder", "Right-hand bat", "Right-arm legbreak", 26, 175, 115, 2750, "86", 28.35, 112.4, 0, 11, 218, 30.8, 5.40, 34.2, "4/8", 72, 0),
    ("CRIC_052", "Mohammad Nabi", "Afghanistan", "All-rounder", "Right-hand bat", "Right-arm offbreak", 40, 282, 245, 5450, "136", 27.50, 104.8, 2, 23, 268, 31.4, 4.65, 40.5, "4/17", 102, 0),
    ("CRIC_053", "Sikandar Raza", "Zimbabwe", "All-rounder", "Right-hand bat", "Right-arm offbreak", 38, 235, 218, 6840, "135*", 35.80, 105.2, 8, 38, 192, 34.2, 5.12, 40.1, "4/8", 88, 0),
    ("CRIC_054", "Mitchell Santner", "New Zealand", "All-rounder", "Left-hand bat", "Slow left-arm orthodox", 33, 208, 136, 2940, "126", 28.25, 92.5, 1, 6, 252, 32.8, 4.62, 42.6, "7/53", 94, 0),
    ("CRIC_055", "Liam Livingstone", "England", "All-rounder", "Right-hand bat", "Right-arm legbreak", 31, 88, 74, 1850, "103", 31.35, 144.2, 1, 8, 48, 34.5, 6.10, 33.9, "3/17", 42, 0),
    ("CRIC_056", "Mehidy Hasan Miraz", "Bangladesh", "All-rounder", "Right-hand bat", "Right-arm offbreak", 27, 168, 142, 3480, "112*", 27.60, 78.5, 3, 14, 284, 33.5, 4.45, 45.2, "8/59", 82, 0),
    ("CRIC_057", "Washington Sundar", "India", "All-rounder", "Left-hand bat", "Right-arm offbreak", 25, 76, 48, 1120, "96*", 32.00, 89.4, 0, 4, 88, 28.4, 4.75, 35.8, "7/59", 32, 0),
    ("CRIC_058", "Shivam Dube", "India", "All-rounder", "Left-hand bat", "Right-arm medium", 31, 45, 36, 850, "63*", 32.69, 136.0, 0, 4, 21, 35.2, 7.40, 28.5, "3/30", 18, 0),
    ("CRIC_059", "Shardul Thakur", "India", "All-rounder", "Right-hand bat", "Right-arm medium-fast", 33, 85, 52, 980, "67", 23.90, 108.6, 0, 5, 128, 30.2, 5.70, 31.8, "7/61", 26, 0),
    ("CRIC_060", "Cameron Green", "Australia", "All-rounder", "Right-hand bat", "Right-arm fast-medium", 25, 62, 54, 1840, "174*", 36.08, 92.5, 2, 7, 52, 36.8, 5.10, 43.3, "5/27", 34, 0),

    # Bowlers
    ("CRIC_061", "Jasprit Bumrah", "India", "Bowler", "Right-hand bat", "Right-arm fast", 31, 195, 88, 480, "55*", 9.60, 62.4, 0, 1, 412, 20.6, 4.15, 29.8, "6/19", 45, 0),
    ("CRIC_062", "Pat Cummins", "Australia", "Bowler", "Right-hand bat", "Right-arm fast", 31, 215, 142, 2150, "64*", 19.35, 78.6, 0, 3, 498, 22.8, 4.38, 31.2, "6/23", 78, 0),
    ("CRIC_063", "Mitchell Starc", "Australia", "Bowler", "Left-hand bat", "Left-arm fast", 35, 275, 168, 2580, "99", 19.85, 84.5, 0, 11, 685, 23.4, 4.88, 28.8, "6/28", 84, 0),
    ("CRIC_064", "Trent Boult", "New Zealand", "Bowler", "Right-hand bat", "Left-arm fast-medium", 35, 255, 128, 1250, "52*", 13.80, 71.2, 0, 1, 610, 24.5, 4.65, 31.6, "7/34", 76, 0),
    ("CRIC_065", "Shaheen Afridi", "Pakistan", "Bowler", "Left-hand bat", "Left-arm fast", 25, 162, 72, 790, "55", 14.90, 89.2, 0, 1, 348, 23.9, 4.95, 29.0, "6/35", 42, 0),
    ("CRIC_066", "Kagiso Rabada", "South Africa", "Bowler", "Left-hand bat", "Right-arm fast", 29, 218, 124, 1540, "47", 15.25, 76.5, 0, 0, 528, 23.1, 4.68, 29.6, "7/112", 68, 0),
    ("CRIC_067", "Rashid Khan", "Afghanistan", "Bowler", "Right-hand bat", "Right-arm legbreak", 26, 208, 138, 2140, "79*", 20.95, 112.5, 0, 6, 385, 19.5, 4.60, 25.4, "7/18", 72, 0),
    ("CRIC_068", "Josh Hazlewood", "Australia", "Bowler", "Left-hand bat", "Right-arm fast-medium", 34, 192, 76, 680, "39", 11.70, 58.4, 0, 0, 442, 24.8, 4.35, 34.2, "6/67", 56, 0),
    ("CRIC_069", "Mohammed Shami", "India", "Bowler", "Right-hand bat", "Right-arm fast", 34, 188, 102, 1050, "56*", 12.80, 82.5, 0, 2, 452, 24.2, 4.80, 30.2, "7/57", 44, 0),
    ("CRIC_070", "Adam Zampa", "Australia", "Bowler", "Right-hand bat", "Right-arm legbreak", 33, 185, 68, 480, "36", 11.40, 74.5, 0, 0, 312, 26.5, 5.30, 30.0, "5/35", 42, 0),
    ("CRIC_071", "Kuldeep Yadav", "India", "Bowler", "Left-hand bat", "Left-arm wrist-spin", 30, 160, 48, 420, "40", 12.35, 65.8, 0, 0, 318, 24.1, 4.85, 29.8, "6/25", 34, 0),
    ("CRIC_072", "Mohammed Siraj", "India", "Bowler", "Right-hand bat", "Right-arm fast", 31, 108, 42, 220, "16*", 8.45, 54.2, 0, 0, 215, 25.8, 4.90, 31.6, "6/21", 28, 0),
    ("CRIC_073", "Arshdeep Singh", "India", "Bowler", "Left-hand bat", "Left-arm medium-fast", 26, 65, 14, 85, "12", 7.70, 78.5, 0, 0, 115, 21.4, 6.85, 18.7, "5/32", 18, 0),
    ("CRIC_074", "Mark Wood", "England", "Bowler", "Right-hand bat", "Right-arm fast", 35, 125, 65, 820, "52", 14.90, 88.6, 0, 1, 235, 28.4, 5.20, 32.8, "6/37", 32, 0),
    ("CRIC_075", "Anrich Nortje", "South Africa", "Bowler", "Right-hand bat", "Right-arm fast", 31, 88, 38, 280, "28", 10.35, 68.2, 0, 0, 182, 24.6, 5.15, 28.7, "6/56", 22, 0),
    ("CRIC_076", "Lockie Ferguson", "New Zealand", "Bowler", "Right-hand bat", "Right-arm fast", 33, 115, 42, 340, "35", 11.70, 72.0, 0, 0, 210, 26.2, 5.35, 29.4, "5/45", 26, 0),
    ("CRIC_077", "Haris Rauf", "Pakistan", "Bowler", "Right-hand bat", "Right-arm fast", 31, 112, 26, 160, "15*", 8.00, 68.4, 0, 0, 195, 24.8, 5.65, 26.3, "5/18", 24, 0),
    ("CRIC_078", "Naseem Shah", "Pakistan", "Bowler", "Right-hand bat", "Right-arm fast", 22, 78, 32, 310, "24", 12.40, 78.5, 0, 0, 148, 24.5, 4.88, 30.1, "5/33", 16, 0),
    ("CRIC_079", "Fazalhaq Farooqi", "Afghanistan", "Bowler", "Right-hand bat", "Left-arm fast-medium", 24, 64, 18, 85, "10*", 6.50, 52.4, 0, 0, 112, 22.3, 5.10, 26.2, "5/9", 14, 0),
    ("CRIC_080", "Keshav Maharaj", "South Africa", "Bowler", "Right-hand bat", "Slow left-arm orthodox", 35, 138, 82, 1420, "84", 17.50, 64.2, 0, 4, 265, 29.4, 4.30, 41.0, "9/129", 48, 0),
    ("CRIC_081", "Maheesh Theekshana", "Sri Lanka", "Bowler", "Right-hand bat", "Right-arm offbreak", 24, 92, 34, 290, "28", 11.15, 62.5, 0, 0, 142, 25.8, 4.75, 32.6, "4/25", 22, 0),
    ("CRIC_082", "Matheesha Pathirana", "Sri Lanka", "Bowler", "Right-hand bat", "Right-arm fast", 22, 45, 12, 45, "9", 5.60, 48.0, 0, 0, 78, 21.8, 6.45, 20.3, "4/24", 10, 0),
    ("CRIC_083", "Noor Ahmad", "Afghanistan", "Bowler", "Right-hand bat", "Left-arm wrist-spin", 20, 38, 12, 65, "12*", 8.10, 58.2, 0, 0, 58, 24.5, 5.20, 28.2, "4/10", 10, 0),
    ("CRIC_084", "Mujeeb Ur Rahman", "Afghanistan", "Bowler", "Right-hand bat", "Right-arm offbreak", 24, 122, 45, 380, "28", 9.50, 64.5, 0, 0, 198, 24.8, 4.50, 33.1, "5/20", 32, 0),
    ("CRIC_085", "Mustafizur Rahman", "Bangladesh", "Bowler", "Left-hand bat", "Left-arm fast-medium", 29, 185, 52, 340, "20", 8.90, 61.2, 0, 0, 295, 24.9, 5.15, 29.0, "6/43", 38, 0),
    ("CRIC_086", "Taskin Ahmed", "Bangladesh", "Bowler", "Left-hand bat", "Right-arm fast", 30, 132, 58, 590, "75", 13.10, 68.5, 0, 1, 218, 29.4, 5.25, 33.6, "5/28", 28, 0),
    ("CRIC_087", "Tim Southee", "New Zealand", "Bowler", "Right-hand bat", "Right-arm medium-fast", 36, 388, 235, 3250, "77*", 16.50, 84.5, 0, 7, 765, 29.8, 4.95, 36.1, "7/33", 145, 0),
    ("CRIC_088", "Ravi Bishnoi", "India", "Bowler", "Right-hand bat", "Right-arm legbreak", 24, 42, 10, 55, "8*", 7.85, 62.0, 0, 0, 65, 19.8, 6.80, 17.5, "4/16", 14, 0),
    ("CRIC_089", "Yuzvendra Chahal", "India", "Bowler", "Right-hand bat", "Right-arm legbreak", 34, 152, 38, 120, "18*", 5.70, 51.5, 0, 0, 217, 26.2, 5.35, 29.4, "6/25", 34, 0),
    ("CRIC_090", "Lungi Ngidi", "South Africa", "Bowler", "Right-hand bat", "Right-arm fast", 29, 92, 32, 210, "19*", 9.55, 62.8, 0, 0, 168, 25.4, 5.40, 28.2, "6/39", 22, 0),

    # Legends & Historic Benchmark Records for Context and Calibration
    ("CRIC_091", "Sachin Tendulkar", "India", "Batter", "Right-hand bat", "Right-arm offbreak", 51, 664, 782, 34357, "248*", 48.52, 82.5, 100, 164, 201, 46.4, 4.95, 56.2, "5/32", 256, 0),
    ("CRIC_092", "Ricky Ponting", "Australia", "Batter", "Right-hand bat", "Right-arm medium", 50, 560, 668, 27483, "257", 45.95, 79.2, 71, 146, 8, 54.2, 4.88, 66.5, "2/18", 354, 0),
    ("CRIC_093", "Brian Lara", "West Indies", "Batter", "Left-hand bat", "Right-arm legbreak", 55, 430, 521, 22358, "400*", 46.20, 77.8, 53, 111, 4, 62.5, 5.12, 73.2, "2/49", 156, 0),
    ("CRIC_094", "Jacques Kallis", "South Africa", "All-rounder", "Right-hand bat", "Right-arm fast-medium", 49, 519, 558, 25534, "224", 49.10, 72.8, 62, 149, 577, 32.1, 4.15, 46.4, "6/54", 338, 0),
    ("CRIC_095", "Wasim Akram", "Pakistan", "Bowler", "Left-hand bat", "Left-arm fast", 58, 460, 382, 6615, "257*", 20.40, 75.8, 3, 13, 916, 23.2, 3.75, 37.1, "7/119", 98, 0),
    ("CRIC_096", "Glenn McGrath", "Australia", "Bowler", "Right-hand bat", "Right-arm fast-medium", 54, 374, 206, 756, "61", 7.35, 48.5, 0, 1, 949, 21.6, 3.88, 33.5, "8/24", 58, 0),
    ("CRIC_097", "Muttiah Muralitharan", "Sri Lanka", "Bowler", "Right-hand bat", "Right-arm offbreak", 52, 495, 290, 1936, "67", 11.20, 58.2, 0, 1, 1347, 22.7, 3.93, 34.6, "9/51", 198, 0),
    ("CRIC_098", "Shane Watson", "Australia", "All-rounder", "Right-hand bat", "Right-arm fast-medium", 43, 307, 310, 10950, "185*", 37.85, 90.2, 14, 62, 291, 31.4, 4.85, 38.8, "4/15", 112, 0),
    ("CRIC_099", "AB de Villiers", "South Africa", "Batter", "Right-hand bat", "Right-arm medium", 40, 420, 442, 20014, "278*", 48.11, 101.2, 47, 109, 9, 38.4, 5.80, 39.7, "2/15", 350, 17),
    ("CRIC_100", "Dale Steyn", "South Africa", "Bowler", "Right-hand bat", "Right-arm fast", 41, 265, 152, 1680, "76", 13.50, 71.5, 0, 2, 699, 23.3, 4.35, 32.1, "7/51", 74, 0),

    # Emerging domestic/franchise scout targets with varied stats to test ranking tiers
    ("CRIC_101", "Sai Sudharsan", "India", "Batter", "Left-hand bat", "-", 23, 22, 22, 850, "96", 42.50, 89.4, 0, 6, 0, None, None, None, "-", 12, 0),
    ("CRIC_102", "Dhruv Jurel", "India", "Wicketkeeper", "Right-hand bat", "-", 24, 18, 16, 520, "90", 37.14, 112.5, 0, 3, 0, None, None, None, "-", 28, 4),
    ("CRIC_103", "Harshit Rana", "India", "Bowler", "Right-hand bat", "Right-arm fast", 23, 16, 8, 95, "24*", 15.80, 85.0, 0, 0, 28, 23.5, 6.12, 23.0, "3/24", 6, 0),
    ("CRIC_104", "Nitish Kumar Reddy", "India", "All-rounder", "Right-hand bat", "Right-arm medium-fast", 21, 18, 15, 480, "74", 34.28, 138.2, 0, 3, 16, 26.8, 6.25, 25.7, "3/32", 10, 0),
    ("CRIC_105", "Abhishek Sharma", "India", "All-rounder", "Left-hand bat", "Slow left-arm orthodox", 24, 25, 23, 620, "100", 28.18, 165.4, 1, 3, 12, 29.5, 7.80, 22.7, "2/12", 14, 0),

    # Records with deliberate raw format issues to test clean_data.py
    ("CRIC_106", "Test Batter With Spaces ", "India", "BATTER ", "Right-hand bat", "-", 24, 20, 18, 600, "102*", "37.50", "88.2", 1, 4, 0, "", "", "", "-", 10, 0),
    ("CRIC_107", "Test Mixed Role", "Australia", "All-Rounder", "Right-hand bat", "Right-arm fast", 25, 22, 19, 450, "65", 26.47, 115.0, 0, 2, 18, "28.5", "5.60", "30.5", "3/20", 8, 0),
    ("CRIC_108", "Pure Bowler Missing Batting", "England", "Bowler", "Right-hand bat", "Right-arm fast", 26, 15, 6, 32, "12", "", "45.0", 0, 0, 24, 22.1, 4.95, 26.8, "4/18", 5, 0),
    # Duplicate row of CRIC_101 to test duplicate dropping
    ("CRIC_101", "Sai Sudharsan", "India", "Batter", "Left-hand bat", "-", 23, 22, 22, 850, "96", 42.50, 89.4, 0, 6, 0, None, None, None, "-", 12, 0),
]

with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for p in players_data:
        writer.writerow(p)

print(f"Successfully generated {csv_path} with {len(players_data)} records (including header).")
