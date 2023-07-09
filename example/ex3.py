"""
# Practice for Moviepy
# Example 3. a Simple music video
# References: https://zulko.github.io/moviepy/examples/ukulele_concerto.html
# Dependencies
# some video files
"""

from moviepy.editor import *


def main():
    # ukulele = VideoFileClip("../input/moi_ukulele.MOV", audio=False). \
    ukulele = VideoFileClip("../input/frontier.mp4.webm", audio=False). \
        subclip(60 + 33, 60 + 50). \
        crop(486, 180, 1196, 570)

    w, h = moviesize = ukulele.size

    piano = (
        VideoFileClip(
            # "../../videos/douceamb.mp4", audio=False
            "../input/knights.mp4", audio=False
        )
        .subclip(30, 50)
        # use pillow 9.5.0 rather than 10.0.0 because Image.ANTIALIAS was removed since 10.0.0
        # moviepy's patch is waiting
        # https://github.com/Zulko/moviepy/pull/2003
        .resize((w / 3, h / 3))
        .margin(6, color=(255, 255, 255))
        .margin(bottom=20, right=20, opacity=0)
        .set_pos(("right", "bottom"))
    )

    txt = TextClip(
        "V. Zulkoninov - Ukulele Sonata",
        font="Amiri-regular",
        color="white",
        fontsize=24
    )

    txt_col = txt.on_color(
        size=(ukulele.w + txt.w, txt.h - 10),
        color=(0, 0, 0),
        pos=(6, "center"),
        col_opacity=0.6
    )

    txt_mov = txt_col.set_pos(lambda t: (max(w / 30, int(w - 0.5 * w * t)), max(5 * h / 6, int(100 * t))))

    final = CompositeVideoClip([ukulele, txt_mov, piano])

    output_path = '../output'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    final.subclip(0, 5).write_videofile(
        os.path.join(output_path, "ex3_ukulele.mp4"),
        fps=24,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True
    )


if __name__ == '__main__':
    main()
