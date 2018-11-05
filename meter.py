#!/usr/bin/python
from argparse import ArgumentParser
from os import walk, path
import json


is_logging = False


def log(message):
    """Print given message if is_logging is True"""
    if is_logging:
        print(message)


def is_line_public(line):
    """Check if line has `public` or `open` keywords."""

    return 'public' in line or 'open' in line


def list_swift_files(directory_name):
    """Recursively list all .swift files in a directory."""
    
    if not path.exists(path.dirname(directory_name)):
        raise ValueError('{0} is not a valid directory'.format(directory_name))

    log('Looking for swift files in {0}'.format(directory_name))

    names = []
    for (directory, _, files) in walk(directory_name):
        for f in files:
            if not isinstance(f, str):
                continue
            if not f.endswith('.swift'):
                continue

            file_path = path.join(directory, f)
            if not path.exists(file_path):
                continue
            
            names.append(file_path)

    log('Found {0} swift files'.format(len(names)))
    return names


def file_stats(file_name):
    """Get code statistics for a swift file."""

    if not path.isfile(file_name):
        raise ValueError('{0} is not a valid file path'.format(file_name))

    if not file_name.endswith('.swift'):
        raise ValueError('{0} is not a valid swift file'.format(file_name))

    log('Analyzing {}'.format(file_name))

    lines = 0
    comments = 0
    enums = 0
    classes = 0
    structs = 0
    extensions = 0
    functions = 0
    static_functions = 0
    variables = 0
    static_variables = 0
    ib_inspectables = 0
    initializers = 0
    failable_initializers = 0
    operators = 0

    with open(file_name) as swift_file:
        for index, line in enumerate(swift_file):
            stripped = line.strip()
            
            if not stripped: # empty line
                continue
            
            if stripped.startswith('//'): # comment
                comments += 1
                continue
            else: # line
                lines += 1

            if not is_line_public(stripped): # inner line or private unit
                if 'operator' in stripped:
                    operators += 1

            if 'enum' in stripped: # enums
                enums += 1

            if 'class' in stripped and not 'func' in stripped: # class
                classes += 1

            if 'struct' in stripped: # struct
                structs += 1

            if 'extension' in stripped: # extension
                extensions += 1

            if 'func' in stripped: # function
                if 'static' in stripped or 'class' in stripped: # static func
                    static_functions += 1
                else: # function
                    functions += 1

            if 'var' in stripped or 'let' in stripped: # var or let
                if 'static' in stripped: # static var or static let
                    static_variables += 1
                else: # var or let
                    variables += 1

            if '@IBInspectable' in stripped: # @IBInspectable
                ib_inspectables += 1

            if 'init(' in stripped: # initializer
                initializers += 1

            if 'init?(' in stripped: # failable initializer
                failable_initializers += 1

    none_static = functions + variables + initializers + failable_initializers
    static = static_functions + static_variables
    total = none_static + static

    results_dict = {}
    results_dict['total_lines'] = index + 1
    results_dict['code_lines'] = lines
    results_dict['enums'] = enums
    results_dict['classes'] = classes
    results_dict['structs'] = structs
    results_dict['extensions'] = extensions
    results_dict['functions'] = functions
    results_dict['static_functions'] = static_functions
    results_dict['variables'] = variables
    results_dict['static_variables'] = static_variables
    results_dict['ib_inspectables'] = ib_inspectables
    results_dict['initializers'] = initializers
    results_dict['failable_initializers'] = failable_initializers
    results_dict['operators'] = operators
    results_dict['total_non_static_units'] = none_static
    results_dict['total_static_units'] = static
    results_dict['total_units'] = total

    return results_dict


def directory_stats(directory_name):
    """Recursively get code statistics for all swift files in a directory."""

    files = list_swift_files(directory_name)

    stats_dict = {}
    stats_list = [file_stats(f) for f in files]
    stats_dict['swift_files'] = len(stats_list)

    for stat_item in stats_list:
        for key in stat_item:
            if key in stats_dict:
                stats_dict[key] = stats_dict[key] + stat_item[key]
            else:
                stats_dict[key] = stat_item[key]

    return stats_dict


def badge_url(key, value, color='green'):
    """Creates a custom shields.io badge for given key and value."""

    base_url = 'https://img.shields.io/badge/{0}-{1}-{2}.svg'
    return base_url.format(key, value, color)


def dict_badge_urls(stats_dict):
    """Custom shields.io badge urls dictionary for statistics dictionary."""

    if not isinstance(stats_dict, dict):
        raise ValueError('{0} is not a valid dictionary'.format(stats_dict))

    badges_dict = {}
    for key, value in stats_dict.items():
        badges_dict[key] = badge_url(key, value)
    return badges_dict


def output_full_path(output_file_path):
    if output_file_path is not None:
        if path.isdir(output_file_path):
            output_file_path = path.join(output_file_path, 'report.txt')
        if path.isabs(output_file_path): 
            return output_file_path
        else: 
            current_dir = path.dirname(__file__)
            return path.join(current_dir, output_file_path)
    return None


def export_to_file(report, file_path):
    with open(file_path, 'a') as f:
        f.write(report)


if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('-d', '--directory', dest='sources',
                        help='Code statistics for all .swift files in a directory')

    parser.add_argument('-f', '--file', dest='file',
                        help='Code statistics for a swift file')

    parser.add_argument('-b', '--badges', action='store_true',
                        help='README badges from shields.io')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Log verbose data')

    parser.add_argument('-o', '--output',
                        help='The output file path where the results will be exported')

    args = parser.parse_args()

    file_name = args.file
    sources_dir = args.sources
    badges = args.badges
    is_logging = args.verbose
    out_file = args.output

    str_report = ""
    if file_name: # Show file stats
        str_report += '=' * 80 + '\n'
        str_report += 'Swift codebase statistics:\n'
        stats_dict = file_stats(file_name)
        str_report += json.dumps(stats_dict, indent=4) + '\n'

        if badges: # show badges
            str_report += '\n'
            str_report += 'Shields.io badges:\n' 
            str_report += json.dumps(dict_badge_urls(STATS_DICT), indent=4) + '\n'
        str_report += '=' * 80 + '\n'

    if sources_dir: # Show directory stats
        str_report += '=' * 80 + '\n'
        str_report += 'Swift codebase statistics:\n' 
        stats_dict = directory_stats(sources_dir) 
        str_report += json.dumps(stats_dict, indent=4) + '\n'

        if badges: # show badges
            str_report += '\n'
            str_report += 'Shields.io badges:\n'
            str_report += json.dumps(dict_badge_urls(stats_dict), indent=4) + '\n'
        str_report += '=' * 80 + '\n'

    print(str_report)

    output_path = output_full_path(out_file)

    if output_path is not None:
        export_to_file(str_report, output_path)
