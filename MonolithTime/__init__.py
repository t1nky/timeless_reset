class MonolithTime:
    def __init__(self, minute: int, seconds: int) -> None:
        self.minute = minute
        self.seconds = seconds

    def __str__(self) -> str:
        return f"{self.minute:02}:{self.seconds:02}"

    def __eq__(self, time2) -> bool:
        return self.minute == time2.minute and self.seconds == time2.seconds

    def __gt__(self, time2) -> bool:
        return self.minute > time2.minute or (
            self.minute == time2.minute and self.seconds > time2.seconds
        )

    def __ge__(self, time2) -> bool:
        return self.minute > time2.minute or (
            self.minute == time2.minute and self.seconds >= time2.seconds
        )

    def __lt__(self, time2) -> bool:
        return time2.minute > self.minute or (
            self.minute == time2.minute and time2.seconds > self.seconds
        )

    def __le__(self, time2) -> bool:
        return time2.minute > self.minute or (
            self.minute == time2.minute and time2.seconds >= self.seconds
        )

    def __calc_next_reset(self):
        nextSecondsDiff = (
            self.seconds - 5
            if self.minute == 5 and self.seconds == 14
            else self.seconds - 8
        )

        nextSeconds = 60 + nextSecondsDiff if nextSecondsDiff < 0 else nextSecondsDiff
        nextMinute = self.minute - 1 if nextSecondsDiff < 0 else self.minute
        return MonolithTime(nextMinute, nextSeconds)

    def _tick(self):
        nextSecondsDiff = self.seconds - 1

        nextSeconds = 60 + nextSecondsDiff if nextSecondsDiff < 0 else nextSecondsDiff
        nextMinute = self.minute - 1 if nextSecondsDiff < 0 else self.minute
        return MonolithTime(nextMinute, nextSeconds)

    def isStarted(self):
        return self.minute > 0 or (self.minute == 0 and self.seconds > 0)

    def Zero():
        return MonolithTime(0, 0)

    def getNextReset(self):
        nextResetTime = MonolithTime(5, 14)
        while nextResetTime >= self:
            nextResetTime = nextResetTime.__calc_next_reset()
        return nextResetTime
