import sys
from subtitle import Subtitle

def main(argv):
    if len(argv) != 4:
        print 'usage:'
        print '    python subtitle.py input-video.mp4 input-subtitle.srt output-video.avi'
        return

    input_video_fname = argv[1]
    input_subt_fname = argv[2]
    output_video_fname = argv[3]

    subt = Subtitle()
    subt.render(input_video_fname, input_subt_fname, output_video_fname)

if __name__ == '__main__':
    main(sys.argv)


