from singleton_decorator import singleton

@singleton
class SignalsStore:
    def __init__(self):
        self._signals = []

    def addChannel(self, channel):
        if isinstance(channel, tuple):
            self._signals.append(channel)
            return len(self._signals)-1
        else:
            print("NOT A DICT")
            return False

    def getChannel(self, channel_num):
        if(channel_num>=0 and channel_num < len(self._signals)):
            return self._signals[channel_num]
        else: return (None,None)

    def getNumChannels(self):
        return len(self._signals)

    def getChannelsNames(self):
        return [channel[0] for channel in self._signals]
