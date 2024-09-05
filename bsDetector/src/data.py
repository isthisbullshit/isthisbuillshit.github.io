import numpy as np

data = [
    ("Earth is flat", 0),
    ("The moon landing was fake", 0),
    ("Vaccines actually save lives", 1),
    ("Nasa controls the weather", 0),
    ("The US government eats children", 0),
    ("Nazi's killed millions of Jews", 1),
    ("The sky is blue", 1),
    ("Water is wet", 1),
    ("Ice is cold", 1),
    ("Elvis is alive", 0),
    ("Vaccines kill", 0),
    ("Clouds are white", 1),
    ("Cows can fly", 0),
    ("Guns kill people", 1),
    ("Pigs can fly", 0),
    ("9/11 was an inside job", 0),
    ("tide pods are great for eating", 0),
    ("The High-Frequency Active Auroral Research Program is a weapon", 0),
    ("Haarp can change weather patterns or cause natural disasters", 0),
    ("Humans Only Use 10% of Their Brains", 0),
    ("Humans Only Use 10% of Their Brains", 0),
    ("Sugar Causes Hyperactivity in Children", 0),
    ("Bats Are Blind", 0),
    ("Goldfish Have a Three-Second Memory", 0),
    ("Cracking Knuckles Causes Arthritis", 0),
    ("Hair and Nails Grow After Death", 0),
    ("Dropping a Penny from a Tall Building Can Kill Someone", 0),
    ("You Should Wait 30 Minutes After Eating Before Swimming", 0),
    ("Vikings Wore Horned Helmets", 0),
    ("Shaving Makes Hair Grow Back Thicker", 0),
    ("You Can See the Great Wall of China from Space", 0),
    ("Chameleons Change Color to Match Their Surroundings", 0),
    ("The Coriolis Effect Determines the Direction Water Drains", 0),
    ("Mount Everest Is the Tallest Mountain", 0),
    ("Ostriches Bury Their Heads in the Sand", 0),
    ("Lightning Never Strikes the Same Place Twice", 0),
    ("Alcohol Warms You Up", 0),
    ("Toads Cause Warts", 0),
    ("Black Belts Mean Expertise", 0),
    ("Milk Increases Mucus Production", 0),
    ("Water is wet", 1),
    ("Fire is hot", 1),
    ("The Earth is round", 1),
    ("The sun rises in the east and sets in the west", 1),
    ("Gravity pulls objects towards the center of the Earth", 1),
    ("Eating a balanced diet is important for health", 1),
    ("Regular exercise benefits physical and mental health", 1),
    ("Smoking is harmful to health", 1),
    ("Washing hands helps prevent the spread of germs", 1),
    ("Wearing a seatbelt reduces injury in car accidents", 1),
    ("Drinking water is essential for survival", 1),
    ("Sleep is necessary for health", 1),
    ("Honesty is generally the best policy", 1),
    ("Looking both ways before crossing the street can prevent accidents", 1),
    ("Saving money is important for financial stability", 1),
    ("Not eating and drinking for a day is good for you", 0),
    ("wild rabbits mate for life", 0),
]

split = np.random.choice([0, 1], len(data))
