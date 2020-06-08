import random

class Descriptions():

    def __init__(self, value):
        self.value = value
        self.godly = "Photo is so good, this means the training data must be biased."

        self.praise = [(f"It is quite difficult to photograph something worth of a {self.value:.2f}."),
                         "The bot thinks I can take beautiful photos!",
                         "Going to post this photo on Reddit for karma",
                         "Don't steal this photo please"]

        self.magnificant = ["This is a pretty good photo....",
                         "You should rack up a few more followers now!",
                         "Not half bad there buddy",
                         "you did it, somehow!"]
        
        self.better =   [(f"With a score of {self.value:.2f}, there's potential."),
                        "could be a bit better",
                        "honestly I could do better",
                        "keep trying",
                        "not your best effort, but not the worst"]

        self.average = (f"Photo isn't great or bad, pretty average. {self.value:.2f} stars.")

        self.insult = ["god this photo makes me feel like the photographer can't use a camera",
                      "your photography dreams are doomed, just quit now",
                      "*cringe*",
                      "bad bad bad nightmare nightmare nightmare",
                      "try stealing from google images haHAA",
                      "this photo sucks, I hate it",
                      "loserboy",
                      "stop taking pictures, shitterton",
                      "photo is such ratshit, it should not exist",
                        "nightmare bot uploaded a shitty photo please shame me",
                        "a fucking nokia can do so much better than this photo",
                        "composition sucks.",
                        (f"{self.value:.2f}, higher than my GPA!"),
                        (f"i will never post to instagram again. having a {self.value:.2f} makes me believe i'm not good enough")]

        self.nightmare = (f"this photo deserves the death sentence, how the fuck did you do so badly to get a {self.value:.2f}?")


    def getDescrption(self):
        if (self.value >= 9.16): return self.godly
        if (6.06 <= self.value < 9.16): return random.choice(self.praise)
        if (4.51 < self.value < 6.06): return random.choice(self.magnificant)
        if (2.96 < self.value <= 4.51): return random.choice(self.better)
        if (self.value == 2.96): return self.average
        if (-3.24 < self.value < 2.96): return random.choice(self.insult)
        if (self.value <= -3.24): return self.nightmare
