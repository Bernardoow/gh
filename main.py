# -*- coding: utf-8 -*-
import argparse

from src.app import Handler


parser = argparse.ArgumentParser(description='GH Crawler')
parser.add_argument('path_output_folder', metavar='path_output_folder', type=str,
                    help='path_output_folder')
parser.add_argument('path_input_file', metavar='path_input_file', type=str,
                    help='path_input_file')
parser.add_argument('path_output_csv_file', metavar='path_output_csv_file', type=str,
                    help='path_output_csv_file')
args = parser.parse_args()

handler = Handler()
#     handler.do_test('./output', './src/input.txt', './result.csv')

handler.do_job(args.path_output_folder, args.path_input_file, args.path_output_csv_file)
