# subtips3 (SUBTItles for PS3)
a tool to create videos with subtitles compatible with playstation 3

Sony's Playstation 3 embeds a video player that supports subtitles, as long as they are embedded in the video file in the form of  a `xsub` stream: side-car subtitle files such as `srt` files are not supported. Also, video containers that support embedded subtitles in the form of text such as `mkv` files are not supported either by Playstation 3 media player. 

One solution to get subtitles on video files is to 'burn' them into the video: the subtitles become part of the images. As a result, the media player doesn't even know that the video file contains subtitles. This solution is not great as:
- it's impossible to turn off subtitles (or even to remove them, as they are hardcoded into the video frames)
- as the media player has no way to know that there are subtitles
	- Playstation 3 media player's subtitle menu is disabled (greyed out)
	- the file doesn't contain subtitle metadata, which prevents media players from using it for searches (eg list all video files that have japanese subtitles)
- it's impossible to add more than one subtitle track (for example for multiple languages) on the same file

So, the most suitable solution for Playstation 3 media server is to embed subtitles as an `xsub` stream. Unfortunately, this has quite a fair amount of drawbacks too:
1. `xsub` streams are not always supported by popular media players (at the time of writing, vlc player doesn't handle them; mplayer is supposed to support them but there seems to be a bug that causes them to not display)
2. because `xsub` streams store subtitles as bitmaps that get overlaid on the image:
	- their storage is far from efficient compared to text-based subtitles such as `srt` files
	- the resolution, size, color or font of the subtitles can't be changed by the viewer. This often results in ugly, hard-to-read subtitles when a low resolution movie is viewed on a high resolution device.

The goal of `subtips3` is to create a Playstation 3-friendly video file from a video file and one or more subtitle files in popular format (eg `srt` files). The playsyation 3-friendly video file can then be played on Playstation 3 media player, regardless it is stored on a local drive or streamed from a pnp media server.

Note: this tool can also be used simply to encode a non PS3 compatible video file (eg `mkv` container, or codecs unsupported by Playstation 3) into a PS3-compatible one.

Note: this tool requires that ffmpeg command line ([https://www.ffmpeg.org/]) is installed and in the current path.

# usage

the following command line creates  the Playstation 3 compatible video `~/Videos/myps3vidwithsubs.avi` from the video `~/Videos/myvideo.mp4` and the `vobsub` subtitle `~/myvideo.fre.idx` (also implicitely requires `~/myvideo.fre.sub`, which is the other file of the `idx/sub` pair that constitutes a `vobsub` subtitle) :
```bash
./src/subtips3.py --input-video ~/Videos/myvideo.mp4  --input-subtitles ~/myvideo.fre.idx --output-resolution simple-def --output-video ~/Videos/myps3vidwithsubs.avi
```
