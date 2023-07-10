"""
# Practice for Moviepy
# Example 4. An example with sound
# References: https://zulko.github.io/moviepy/examples/example_with_sound.html
#             https://github.com/Zulko/moviepy/blob/v2.0.0.dev2/examples/example_with_sound.py
# Dependencies
# 1. some video files
# 2. moviepy 2.0.0-dev2 (because of https://github.com/Zulko/moviepy/issues/1205)
"""

from moviepy.editor import *
from moviepy.video.tools.drawing import color_split


def main():
    duration = 6

    main_clip = VideoFileClip("../input/frontier.mp4.webm")
    W, H = main_clip.size

    # Bug of 1.0.3, this is fixed on dev(2.0.0-dev2) version
    # Issue: https://github.com/Zulko/moviepy/issues/1205
    # PR: https://github.com/Zulko/moviepy/pull/1212
    mask = color_split(
        (2 * int(W / 3), H),
        p1=(int(W / 3), H),
        p2=(2 * int(W / 3), 0),
        col1=1,
        col2=0,
        grad_width=2
    )

    mask_clip = ImageClip(
        mask,
        ismask=True
    )

    # issue with VideoFileClip::coreader https://github.com/Zulko/moviepy/issues/915 <- 2.0.0-dev2 에 반영 안되어 있음...
    # coreader는 최신
    # coreader is added on https://github.com/Zulko/moviepy/commit/21fff157858eee4e9e9b77a73d862f38e520299d
    # coreader is removed on https://github.com/Zulko/moviepy/commit/cc0258701807a4cd685fa6433fd5ecacb4136747
    clip_left = (
        main_clip
        .subclip(0, duration)
        .crop(x1=60, x2=60 + int(2 * W / 3))
        .set_mask(mask_clip)
    )

    mask = color_split(
        (2 * int(W / 3), H),
        p1=(2, H),
        p2=(int(W / 3) + 2, 0),
        col1=0,
        col2=1,
        grad_width=2
    )

    mask_clip = ImageClip(mask, ismask=True)

    clip_right = (
        main_clip
        .subclip(21, 21 + duration)
        .crop(x1=70, x2=70 + 2 * int(W / 3))
        .set_mask(mask_clip)
    )

    cc = CompositeVideoClip(
        [
            clip_right.set_position("right").volumex(0.4),
            clip_left.set_position("left").volumex(0.4)
        ],
        size=(W, H)
    )

    cc.write_videofile(
        "../output/ex4_biphone3.mp4",
        fps=24,
        codec="mpeg4",
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )


if __name__ == "__main__":
    main()
