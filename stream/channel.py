class Channel:
    def __init__(self):
        self.channels = []

    def add_channel(self, name, channel_url, video_file):
        stream_channel = {'name': name, 'channel_url': channel_url, 'video_file': video_file}
        self.channels.append(stream_channel)

    def get_channels(self):
        return self.channels
