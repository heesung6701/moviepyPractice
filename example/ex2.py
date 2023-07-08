"""
# Practice for Moviepy
# Example 2. A reconstitution of 15th century dancing
# References: https://zulko.github.io/moviepy/examples/dancing_knights.html
# Dependencies
# 1. youtube-dl (brew install youtube-dl)
"""

from moviepy.audio.tools.cuts import find_audio_period
from moviepy.editor import *
from moviepy.video.tools.cuts import find_video_period


def main():
    input_path = '../input'
    if not os.path.exists(input_path):
        os.makedirs(input_path)
    input_knights_file_path = os.path.join(input_path, 'knights.mp4')
    if not os.path.exists(input_knights_file_path):
        os.system("youtube-dl zvCvOC2VwDc -o {}".format(input_knights_file_path))

    input_frontier_file_path = os.path.join(input_path, 'frontier.mp4.webm')
    if not os.path.exists(input_frontier_file_path):
        print(input_frontier_file_path)
        print("youtube-dl lkY3Ek9VPtg -o {}".format(input_frontier_file_path))
        os.system("youtube-dl lkY3Ek9VPtg -o {}".format(input_frontier_file_path))

    audio = (
        AudioFileClip(filename=input_frontier_file_path)
        .subclip((4, 7), (4, 18))
        .audio_fadein(1)
        .audio_fadeout(1)
    )

    audio_period = find_audio_period(audio)
    print('Analyzed the audio, found a period of %.02f seconds' % audio_period)

    clip = (
        VideoFileClip(input_knights_file_path, audio=False)
        # .subclip((1, 24.15), (1, 26))
        .subclip((1, 29), (1, 30.75))
        # .crop(x1=332, x2=910, y2=686)
        .crop(x1=571, x2=1249, y1=97, y2=983)
    )

    # video_period = find_video_period(clip, tmin=0.3)
    # print('Analyzed the video, found a period of %.02f seconds' % video_period)

    edited_right = (
        clip
        .speedx(final_duration=2 * audio_period)
        # .subclip(.25)
    )
    edited_right = concatenate_videoclips(
        [
            edited_right,
            edited_right.fx(vfx.time_mirror)
        ]
    )
    edited_right = edited_right.fx(vfx.loop, duration=audio.duration)

    edited_left = edited_right.fx(vfx.mirror_x)

    dancing_knights = (
        clips_array([[edited_left, edited_left]])
        .fadein(1).fadeout(1).set_audio(audio).subclip(.3)
    )

    txt_title = (
        TextClip(
            "15th century dancing\n(hypothetical)",
            fontsize=70,
            font="Century-Schoolbook-Roman",
            color="white"
        )
        .margin(top=15, opacity=0)
        .set_position(("center", "top"))
    )

    title = (
        CompositeVideoClip([dancing_knights.to_ImageClip(), txt_title])
        .fadein(.5)
        .set_duration(3.5)
    )

    txt_credits = """
    CREDITS

    Video excerpt: Le combat en armure au XVe siècle
    By J. Donzé, D. Jaquet, T. Schmuziger,
    Université de Genève, Musée National de Moyen Age

    Music: "Frontier", by DOCTOR VOX
    Under licence Creative Commons
    https://www.youtube.com/user/DOCTORVOXofficial

    Video editing © Zulko 2014
     Licence Creative Commons (CC BY 4.0)
    Edited with MoviePy: http://zulko.github.io/moviepy/
    """

    credits = (
        TextClip(
            txt_credits,
            color="white",
            font="Century-Schoolbook-Roman",
            fontsize=35,
            kerning=-2,
            interline=-1,
            bg_color="black",
            size=title.size
        )
        .set_duration(2.5)
        .fadein(.5)
        .fadeout(.5)
    )

    final = concatenate_videoclips([title, dancing_knights, credits])

    output_path = '../output'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    final.write_videofile(
        os.path.join(output_path, "ex2_dancing_knights.mp4"),
        fps=clip.fps,
        audio_bitrate="1000k",
        bitrate="4000k"
    )


if __name__ == '__main__':
    main()
