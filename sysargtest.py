import os
import sys

usage_hint = """
    that might not have worked properly, just keep testing some sys.argv stuff :D
"""


if __name__ == "__main__":
    print(sys.argv)
    try:
        # parse arguments
        if len(sys.argv) < 4:
            print(usage_hint)
            sys.exit(0)

        input_video = sys.argv[1]
        start_time = sys.argv[2]
        end_time = sys.argv[3]
        output_filename = os.path.splitext(os.path.basename(input_video))[0] + "_clip.mp4"
        output_dir = os.path.dirname(input_video)

        if len(sys.argv) > 4 and sys.argv[4] != "-o":
            output_filename = os.path.splitext(os.path.basename(sys.argv[4]))[0]

        if len(sys.argv) > 5 and "-o" in sys.argv:
            if sys.argv[5] == "-o":
                output_dir = sys.argv[6]
            elif sys.argv[4] == "-o":
                output_dir = sys.argv[5]
    
    except Exception as e:
        print(e)
        print(usage_hint)
        exit(1)
    
    print(input_video, start_time, end_time, output_filename, output_dir)