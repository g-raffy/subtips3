#!/usr/bin/env python3

import argparse
from subprocess import Popen
from pathlib import Path
import typing

OUTPUT_RESOLUTION_PROFILES = ['original', 'simple-def', 'full-hd']
Resolution = typing.Literal[tuple(OUTPUT_RESOLUTION_PROFILES)]


def get_idx_file_path(subtitle_file_path: Path) -> Path:
    supported_subtitle_formats = ['idx']
    extension = subtitle_file_path.suffix[1:]
    if extension not in supported_subtitle_formats:
        raise Exception('subtitle format %s is not yet supported. You need to convert it manually (hopefully it will be done automatically at some point) into an idx/sub file pair (vobsub format) using Subtitle Edit (https://github.com/SubtitleEdit/subtitleedit) for example, then provide the path to the idx file instead of the %s file. If you use Subtitle Edit to generate your vobsub idx/sub pair, make sure that the bottom margin is big enough (around 20%) otherwise the subtitles would be off screen. Also make sure that the subtitle resolution matches the resolution of the output video file.' % (extension, extension))
    return subtitle_file_path


def make_ps3_video(src_video: Path, dst_video: Path, input_subtitles: typing.List[Path], output_resolution: Resolution):
    print(input_subtitles)
    ps3_supported_encoders = [
        'mpeg4',
        'libxvid'
    ]
    ffmpeg_exe = 'ffmpeg'
    try:
        process = Popen([ffmpeg_exe, '-version'])
    except FileNotFoundError:
        raise Exception('unable to find the required external program %s. Make sure that it\'s installed and that it\'s in your path' % ffmpeg_exe)

    ffmpeg_command = [ffmpeg_exe]
    ffmpeg_command += ['-i', src_video]
    for input_subtitle_file_path in input_subtitles:
        ffmpeg_command += ['-i', get_idx_file_path(input_subtitle_file_path)]
    ffmpeg_command += ['-t', '30']  # restrict output movie duration to 30 seconds

    # define the output video encoding that is handled by Playstation 3
    output_video_encoder = 'mpeg4'
    if output_video_encoder not in ps3_supported_encoders:
        raise Exception('encoder %s is not supported by Playsation 3 (Playstation 3 supported encoders : %s)' % (output_video_encoder, ps3_supported_encoders))
    ffmpeg_command += ['-c:v', output_video_encoder]

    # define the output video quality
    output_video_quality = 5
    best_video_quality = 1
    lowest_video_quality = 31
    if output_video_quality not in range(best_video_quality, lowest_video_quality + 1):
        raise Exception('the output video quality is expected to be in the range [%d;%d]' % (best_video_quality, lowest_video_quality))
    ffmpeg_command += ['-q:v', str(output_video_quality)]

    # set the video tag to xvid (doesn't seem necessary for ps3 media player but it doesn't hurt)
    ffmpeg_command += ['-vtag', 'xvid']

    # ensure the subtitles are encoded in xsub format (the only subtitle format supported by playstation 3 media player)
    ffmpeg_command += ['-scodec', 'xsub']

    if output_resolution == 'simple-def':
        ffmpeg_command += ['-vf', 'scale=720:576']
    elif output_resolution == 'full-hd':
        ffmpeg_command += ['-vf', 'scale=1920:1080']

    ffmpeg_command += [dst_video]

    process = Popen(ffmpeg_command)
    (stdout, stderr) = process.communicate()
    if process.returncode != 0:
        raise Exception('the command %s failed with error code %d' % (ffmpeg_command, process.returncode))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='creates a playstation 3 compatible video file')
    parser.add_argument('-iv', '--input-video', type=Path, required=True, help='the input video file path')
    parser.add_argument('-is', '--input-subtitles', type=Path, nargs='+', help='the input subtitle files path (srt, idx)')
    parser.add_argument('-ov', '--output-video', type=Path, required=True, help='the ps3 compatible output video file path')
    parser.add_argument('-or', '--output-resolution', type=str, choices=OUTPUT_RESOLUTION_PROFILES, default='original', help='the wanted resolution for the output video')
    args = parser.parse_args()
    print(dir(args))
    make_ps3_video(args.input_video, args.output_video, args.input_subtitles, args.output_resolution)
