import argparse, sys, os, numpy
import cv2 as cv
from PIL import Image, ImageEnhance, ImageFilter, UnidentifiedImageError

VIDEO_FORMAT = [".mp4", ".avi", ".mkv"]
TRANSPOSES = {0: Image.Transpose.FLIP_LEFT_RIGHT, 1: Image.Transpose.FLIP_TOP_BOTTOM}


def main():
    args = parse_args()
    media_type = args.media.lower()
    match media_type:
        case "image":
            create_image(args)
        case "video":
            create_video(args)
        case _:
            sys.exit("Please type in the supported media type either image or video.")


def process_img(args, img):
    if args.brightness:
        img = ImageEnhance.Brightness(img)
        img = img.enhance(args.brightness)
    if args.contrast:
        img = ImageEnhance.Contrast(img)
        img = img.enhance(args.contrast)
    if args.sharpness:
        img = ImageEnhance.Sharpness(img)
        img = img.enhance(args.sharpness)

    color = args.color
    if color != None:
        img = ImageEnhance.Color(img)
        img = img.enhance(color)
    if args.blur != None:
        img = img.filter(ImageFilter.GaussianBlur(args.blur))
    if args.resize != None:
        width, length = img.size
        factor = args.resize[0] / width
        img = img.resize((int(width * factor), int(length * factor)))
    if args.flip != None:
        img = img.transpose(TRANSPOSES[args.flip])
    if args.rotate != None:
        img = img.rotate(args.rotate)
    try:
        if args.crop:
            img = img.crop(tuple(args.crop))
    except SystemError:
        print(
            "Please either check the rectangular box specified for cropping. It may be outside boundary of the processed image"
        )

    return img


def create_image(args):
    try:
        with Image.open(args.inputPath) as img:
            img = process_img(args, img)
            try:
                oFileName = checkFileExist(args.outputFileName)
                img.save(oFileName)
                if args.show:
                    img.show()
            except ValueError:
                _, extension = os.path.splitext(oFileName)
                if extension:
                    sys.exit(
                        f"Output file path ('f{oFileName}') is with an unsupported image extenstion (f{extension})"
                    )
                sys.exit(
                    "Output file name extension is empty. Please provide the right supported image formats"
                )

    except FileNotFoundError:
        sys.exit(
            f"Image Path: '{args.inputPath}' cannot be found. Please type in the right image path"
        )


def create_video(args):
    images = []
    dir_path = args.inputPath
    if os.path.isdir(dir_path):
        for file_path in os.listdir(dir_path):
            full_path = os.path.join(dir_path, file_path)
            if os.path.isfile(full_path):
                try:
                    with Image.open(full_path) as img:
                        processed_img = process_img(args, img)
                        mat_img = numpy.array(processed_img)
                        images.append(cv.cvtColor(mat_img, cv.COLOR_RGB2BGR))
                except UnidentifiedImageError:
                    print(
                        f"'{file_path}' was unenabled to be process because of wrong or unsupported image format"
                    )
        if len(images) == 0:
            sys.exit("No image file found in the specified directory.")
        else:
            path, ext = handleFileFolderCreation(args.outputFileName)
            first_frame = images[0]
            height, width, _ = first_frame.shape
            size = (width, height)
            try:
                vid_out = cv.VideoWriter(path, -1, args.frate, size)
                for img in images:
                    vid_out.write(img)
                vid_out.release()
            except FileExistsError as error:
                print(error)
            if args.show:
                vc = cv.VideoCapture(path)
                while vc.isOpened():
                    ret, frame = vc.read()
                    if ret:
                        cv.imshow(f"{args.outputFileName}", frame)
                        if cv.waitKey(20) & 0xFF == ord("q"):
                            break
                    else:
                        break
    else:
        sys.exit(
            f"'{dir_path}' is not a path to a directory. Please enter the correct path to the directory containing the image sequences."
        )


def range_for_float(arg_type, min, max):
    def range_checker(arg: str):
        try:
            f = float(arg)

            if f >= min and f <= max:
                return f
            else:
                raise argparse.ArgumentTypeError(
                    f"{arg_type} must be between {min} and {max}"
                )
        except ValueError:
            raise argparse.ArgumentTypeError(f"{arg_type} argument must be a float")

    return range_checker


def range_for_int(arg_type, min: int, max: int):
    def range_checker(arg):
        try:
            f = int(arg)

            if f >= min and f <= max:
                return f
            else:
                raise argparse.ArgumentTypeError(
                    f"{arg_type} must be between {min} and {max}"
                )
        except ValueError:
            raise argparse.ArgumentTypeError(f"{arg_type} argument must be an int")

    return range_checker


def parse_args():
    parser = argparse.ArgumentParser(
        description="This is an image and video processing program",
        epilog="This program can add filter, rotate, resize, crop and transpose any image. It can also take image sequences, add effects to it and output it in any video format.",
    )

    parser.add_argument(
        "media", help="Select the supported media type either image or video"
    )

    parser.add_argument(
        "inputPath",
        help="the input path to the single image for images processing or to a directory containing the image sequences for video processing",
    )

    parser.add_argument(
        "outputFileName",
        help="the output name of the image or video in their supported formats",
    )

    parser.add_argument(
        "--crop", help="crop only the image", type=int, nargs=4, metavar="px"
    )

    parser.add_argument(
        "--resize",
        help="resizes the image or video",
        nargs=1,
        type=range_for_int("Resize", 1, float("inf")),
        metavar="px",
    )

    parser.add_argument(
        "--rotate",
        help="rotate the image or video",
        type=float,
        metavar="angleInDegrees",
        default=None,
    )

    parser.add_argument(
        "--flip",
        help="Flips the image or video. Input should be 0 for flipping horizontally and 1 for vertically",
        type=int,
        choices=range(2),
        default=None,
    )

    parser.add_argument(
        "--blur",
        help="adjusts the image or video blur by a factor",
        type=range_for_float("Blur", 0, 2),
        default=None,
    )

    parser.add_argument(
        "--contrast",
        help="adjust the image or video contrast by a factor",
        type=float,
        default=None,
    )

    parser.add_argument(
        "--color",
        help="adjust the image or video color balance by a factor",
        type=range_for_float("Color", 0, 2),
        metavar="saturation",
        default=None,
    )

    parser.add_argument(
        "--brightness",
        help="adjust the image or video brightness by a factor",
        type=range_for_float("Brightness", 0, 5),
        default=None,
    )

    parser.add_argument(
        "--sharpness",
        help="adjust the image or video sharpness by a factor",
        type=range_for_float("Sharpness", 0, 5),
        default=None,
    )

    parser.add_argument(
        "--frate", help="the frame rate of the video output", type=int, default=24
    )

    parser.add_argument(
        "--show",
        help="to immediately show the saved image or video",
        action="store_true",
    )

    return parser.parse_args()


def checkFileExist(path: str):
    while True:
        if os.path.isfile(path):
            prompt = (
                input("Do you want to overwrite the exiting file? [Y]es [N]o: ")
                .strip()
                .lower()
            )
            match prompt:
                case "y" | "yes":
                    break
                case "n" | "no":
                    path = input("New output file path: ").strip()
                    break
                case _:
                    print("Nothing or invalid input.")
                    pass
        else:
            break
    return path


def handleFileFolderCreation(path: str):
    if path == "":
        sys.exit(f"{path} is not a valid path. Please provide the right output file.")

    path = checkFileExist(path)
    _, ext = os.path.splitext(path)
    if ext in VIDEO_FORMAT:
        if os.path.split(path)[0] != "":
            os.makedirs(os.path.split(path)[0], exist_ok=True)
        return path, ext
    else:
        sys.exit("Please provide a right video extension for video.")


if __name__ == "__main__":
    main()
