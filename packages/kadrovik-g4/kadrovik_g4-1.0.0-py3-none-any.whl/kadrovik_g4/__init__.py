import ffmpeg


class Kadrovik:

    def __init__(self, video: str = '', frameN: int = 5, outPath: str = 'frame_%d.png'):
        """
        :param video: Input video
        :param frameN: Extract frame number
        :param outPath: Path to output frames
        """

        self.video = video
        self.frameN = frameN
        self.outPath = outPath

    def process(self, video: str = ''):
        """
        Process video
        :param video: Input video
        :return: None
        """

        if video != '':
            self.video = video
        if self.video != '':
            ffmpeg.input(
                self.video
            ).filter(
                'select',
                'not(mod(n,' + str(self.frameN) + '))',
            ).output(
                self.outPath,
                vsync='vfr'
            ).overwrite_output(
            ).run(quiet = True)

    @property
    def video(self):
        return self.__video

    @video.setter
    def video(self, video: str):
        self.__video = video

    @property
    def frameN(self):
        return self.__frameN

    @frameN.setter
    def frameN(self, frameN: int):
        self.__frameN = frameN

    @property
    def outPath(self):
        return self.__outPath

    @outPath.setter
    def outPath(self, outPath: str):
        self.__outPath = outPath

    def __str__(self):
        """Overrides the default implementation"""
        return self.video + ' => ' + self.outPath + ' (' + str(self.frameN) + ')'
