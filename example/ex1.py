"""
# Practice for Moviepy
# Example 1. Text with moving letters
# References https://zulko.github.io/moviepy/examples/moving_letters.html
# Dependencies
# 1. python-scipy (pip install scipy)
"""
import numpy as np

from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects


def main():
    screensize = (720, 460)
    txtClip = TextClip('Cool effect', color='white', font='Amiri-Bold',
                       kerning=5, fontsize=100)

    cvc = CompositeVideoClip([txtClip.set_pos('center')], size=screensize)

    rotMatrix = lambda a: np.array(
        [
            [np.cos(a), np.sin(a)],
            [-np.sin(a), np.cos(a)]
        ]
    )

    def vortex(screenpos, i, nletters):
        d = lambda t: 1.0 / (0.3 + t ** 8)  # damping
        a = i * np.pi / nletters  # angle of movement
        v = rotMatrix(a).dot([-1.0, 0])
        if i % 2: v[1] = -v[1]
        return lambda t: screenpos + 400 * d(t) * rotMatrix(0.5 * d(t) * a).dot(v)

    def cascade(screenpos, i, nletters):
        v = np.array([0, -1])
        d = lambda t: 1 if t < 0 else abs(np.sinc(t) / (1 + t ** 4))
        return lambda t: screenpos - 400 * v * d(t - 0.15 * i)

    def arrive(screenpos, i, nletters):
        v = np.array([0, -1])
        d = lambda t: max(0, 3 * (1 - t))
        return lambda t: screenpos - 400 * v * d(t - 0.2 * i)

    def vortexout(screenpos, i, nletters):
        d = lambda t: max(0, t)
        a = i * np.pi / nletters
        v = rotMatrix(a).dot([-1, 0])
        if i % 2: v[1] = -v[1]
        return lambda t: screenpos + 400 * d(t - 0.1 * i) * rotMatrix(-0.2 * d(t) * a).dot(v)

    letters = findObjects(cvc)

    def moveLetters(letters, funcpos):
        return [
            letter.set_pos(funcpos(letter.screenpos, i, len(letters)))
            for i, letter in enumerate(letters)
        ]

    clips = [
        CompositeVideoClip(
            moveLetters(letters, funcpos),
            size=screensize
        ).subclip(0, 5)
        for funcpos in [vortex, cascade, arrive, vortexout]]

    final_clip = concatenate_videoclips(clips)
    output_path = '../output'
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    final_clip.write_videofile('{}/ex1_coolTextEffects.mp4'.format(output_path), fps=25, codec='mpeg4')


if __name__ == '__main__':
    main()
