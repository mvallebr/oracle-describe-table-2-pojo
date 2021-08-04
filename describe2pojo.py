
import os
import re

TYPE_MAP = {
    r"TIMESTAMP.*": ("import java.time.LocalDateTime", "LocalDateTime"),
    r"VARCHAR2.*": ("import java.lang.String", "String"),
    r"NUMBER\s*\(\d+\)": ("import java.lang.Long", "Long"),
    r"NUMBER\s*\(\d+,\d+\)": ("import java.lang.Float", "Float"),
}


def underscore_2_camel_case(underscore_file_name, first_lower=False):
    return ''.join(
        (x.capitalize() if i != 0 or not first_lower else x)
        or '_'
        for i, x in enumerate(underscore_file_name.split('_'))
    )


def field_list(describe_table_text):
    lines = describe_table_text.split("\n")
    separators = [lines[1].find(" ")]
    separators.append(lines[1].find(" ", separators[-1]+1))
    result = []
    for line in lines[2:]:
        field_name = line[0:separators[0]]
        nullable = line[separators[0]+1:separators[1]]
        field_type = line[separators[1]+1:]
        result.append((field_name, nullable, field_type))
    return result


def to_java_type(oracle_type_str):
    for reg_ex, (import_stmt, java_type) in TYPE_MAP.items():
        if re.match(reg_ex, oracle_type_str):
            return import_stmt, java_type
    raise Exception(
        f"Could not find a matching java type for oracle type '{oracle_type_str}")


def convert_to_pojo(describe_table_text, class_name):
    oracle_field_list = field_list(describe_table_text)
    java_field_list = [
        (
            underscore_2_camel_case(
                field_name.lower(), first_lower=True
            ).strip(),
            to_java_type(oracle_type)
        )
        for field_name, _, oracle_type in oracle_field_list
    ]
    import_list = "\n".join(
        sorted(set([f"{import_stmt};" for (_, (import_stmt, _)) in java_field_list])))
    java_field_list_declarations = "\n".join([f"    private {java_type} {field_name};" for (
        field_name, (_, java_type)) in java_field_list])

    return f"""
{import_list}

public class {class_name} {{
{java_field_list_declarations}
}}
"""


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(
        description="""Oracle Describe table 2 pojo""")
    parser.add_argument('input_file_name', type=str,
                        help='The file containing oracle describe table output')
    parser.add_argument('output_folder', type=str,
                        help='The place where we will save the pojo file')
    parser.add_argument('--overwrite', default=False, action='store_true')
    return parser.parse_args()


def main(input_file_name, output_folder, overwrite):
    with open(input_file_name, "r") as f:
        describe_table_text = f.read()

    class_name = underscore_2_camel_case(
        os.path.splitext(os.path.basename(input_file_name))[0])

    output_file_name = os.path.join(output_folder, f"{class_name}.java")
    if os.path.exists(output_file_name) and (not overwrite or os.path.isdir(output_file_name)):
        raise Exception(
            f"{output_file_name} either exists and overwrite flag wasn't set, or it's a folder.")

    pojo_text = convert_to_pojo(describe_table_text, class_name)

    with open(output_file_name, "w") as f:
        f.write(pojo_text)


if __name__ == '__main__':
    args = parse_arguments()
    main(args.input_file_name, args.output_file_name, args.overwrite)
