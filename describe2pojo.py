
import os


def underscore_2_camel_case(underscore_file_name):
    return ''.join(x.capitalize() or '_' for x in underscore_file_name.split('_'))


def convert_to_pojo(describe_table_text, class_name):
    return f"""public class {class_name} {{

        }}
        """


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(
        description="""Oracle Describe table 2 pojo""")
    parser.add_argument('input_file_name', type=str,
                        help='The file containing oracle describe table output')
    parser.add_argument('output_file_name', type=str,
                        help='The place where we will save the pojo file')
    parser.add_argument('--overwrite', default=False, action='store_true')
    return parser.parse_args()


def main(input_file_name, output_file_name, overwrite):
    with open(input_file_name, "r") as f:
        describe_table_text = f.read()

    if os.path.exists(output_file_name) and (not overwrite or os.path.isdir(output_file_name)):
        raise Exception(
            "Either output file exists and overwrite flag wasn't set, or it's a folder.")

    class_name = underscore_2_camel_case(
        os.path.splitext(os.path.basename(output_file_name))[0])

    pojo_text = convert_to_pojo(describe_table_text, class_name)

    with open(output_file_name, "w") as f:
        f.write(pojo_text)


if __name__ == '__main__':
    args = parse_arguments()
    main(args.input_file_name, args.output_file_name, args.overwrite)
