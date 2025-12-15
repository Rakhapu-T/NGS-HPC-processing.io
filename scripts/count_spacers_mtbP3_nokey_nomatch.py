from Bio import SeqIO
import csv
from collections import OrderedDict, defaultdict
import numpy as np
import sys
import argparse
import os
import glob
import gzip
from multiprocessing import Pool, cpu_count, Manager, Lock


def count_spacers(input_file, fastq_file, guide_g):
	"""
	Counts guide sequences from a FASTQ file and matches them against a library.
	
	Reads a FASTQ file (or gzipped FASTQ), extracts sequences, and counts how many times
	each guide appears. Matches guides against a reference library and calculates various
	statistics including match rates, coverage, and distribution skew.
	
	Parameters:
	----------
	input_file : str
		Path to the CSV file containing the reference library sequences (one sequence per row).
	fastq_file : str
		Path to the FASTQ file to process. Can be .fastq or .fastq.gz format.
	guide_g : bool
		Indicates whether there is a guanine base before the spacer sequence.
	
	Returns:
	-------
	tuple
		(dict_sorted, nons_dict, stats) where:
		- dict_sorted: OrderedDict of guide sequences with their counts
		- nons_dict: dict of non-matching sequences with their counts
		- stats: list containing [perfect_matches, non_perfect_matches, num_reads, 
		         percent_matched, percent_no_reads, skew_ratio, guides_with_reads, guides_no_reads]
	"""

	num_reads = 0 #total number of reads processed
	perfect_matches = 0 # guides with perfect match to library
	non_perfect_matches = 0 #number of guides without a perfect match to the library

	# open library sequences and initiate dictionary of read counts for ealich guide
	try:
		with open(input_file, newline='') as infile:
			reader = csv.reader(infile)
			dictionary = {rows[0]:0 for rows in reader}
	except:
		print('could not open', input_file)
	  
	# open fastq file
	try:
		if fastq_file.endswith('.gz'):
			handle = gzip.open(fastq_file, 'rt')
		else:
			handle = open(fastq_file, 'r')
	except:
		print("could not find fastq file")
		return

	# process reads in fastq file
	readiter = SeqIO.parse(handle, "fastq")
	nons_dict = defaultdict(int)
	for record in readiter: #contains the seq and Qscore etc.
		num_reads += 1
		guide = str.upper(str(record.seq))
          
		if guide in dictionary:
			dictionary[guide] += 1
			perfect_matches += 1
		else:
			nons_dict[guide] += 1
			non_perfect_matches += 1

	# create ordered dictionary with guides and respective counts and output as a csv file                      
	dict_sorted = OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))

	# percentage of guides that matched perfectly
	percent_matched = round(perfect_matches/float(perfect_matches + non_perfect_matches) * 100, 1)
	# percentage of undetected guides with no read counts
	guides_with_reads = np.count_nonzero(list(dictionary.values()))
	guides_no_reads = len(dictionary.values()) - guides_with_reads
	percent_no_reads = round(guides_no_reads/float(len(dictionary.values())) * 100, 1)
	# skew ratio of top 10% to bottom 10% of guide counts
	top_10 = np.percentile(list(dictionary.values()), 90)
	bottom_10 = np.percentile(list(dictionary.values()), 10)
	if top_10 != 0 and bottom_10 != 0:
		skew_ratio = top_10/bottom_10
	else:
		skew_ratio = 'Not enough perfect matches to determine skew ratio'

	stats = [perfect_matches, non_perfect_matches, num_reads, percent_matched, percent_no_reads, skew_ratio, guides_with_reads, guides_no_reads]


	handle.close()           
	return dict_sorted, nons_dict, stats


def process_single_file(args_tuple):
	"""
	Wrapper function to process a single FASTQ file in parallel.
	
	This function is called by the multiprocessing Pool to process each FASTQ file
	independently. It handles the complete workflow for one file: counting spacers,
	printing results, and updating the progress counter.
	
	Parameters:
	----------
	args_tuple : tuple
		Tuple containing (input_file, fastq_file, guide_g, results_dir, counter, lock, total):
		- input_file: Path to reference library CSV
		- fastq_file: Path to FASTQ file to process
		- guide_g: Boolean for guanine presence
		- results_dir: Directory to save results
		- counter: Shared multiprocessing counter for progress tracking
		- lock: Multiprocessing lock for thread-safe counter updates
		- total: Total number of files to process
	
	Returns:
	-------
	tuple
		(fastq_file, success, stats) where:
		- fastq_file: Name of the processed file
		- success: Boolean indicating if processing succeeded
		- stats: List of statistics (or None if failed)
	"""
	input_file, fastq_file, guide_g, results_dir, counter, lock, total = args_tuple
	try:
		dict_sorted, nons_dict, stats = count_spacers(input_file, fastq_file, guide_g)
		print_results(fastq_file, results_dir, dict_sorted, nons_dict, stats)
		
		# Increment counter and print progress
		with lock:
			counter.value += 1
			print(f"Processed {fastq_file}. [{counter.value}/{total}]")
		
		return (fastq_file, True, stats)
	except Exception as e:
		print(f"Error processing {fastq_file}: {str(e)}")
		return (fastq_file, False, None)


def write_overall_statistics(results_dir, all_stats, file_count):
	"""
	Calculates and writes aggregate statistics from all processed files to the top of statistics.txt.
	
	This function aggregates statistics from all successfully processed FASTQ files,
	calculates overall metrics, and prepends them to the statistics file while preserving
	individual file statistics already written.
	
	Parameters:
	----------
	results_dir : str
		Path to the directory where the statistics.txt file is located.
	all_stats : list of list
		List of statistics lists from all successfully processed files. Each stats list contains:
		[perfect_matches, non_perfect_matches, num_reads, percent_matched, percent_no_reads, 
		 skew_ratio, guides_with_reads, guides_no_reads]
	file_count : int
		Number of files that were successfully processed.
	
	Returns:
	-------
	None
		Writes directly to statistics.txt file.
	"""
	# Calculate aggregate statistics
	total_perfect = sum(s[0] for s in all_stats)
	total_nonperfect = sum(s[1] for s in all_stats)
	total_reads = sum(s[2] for s in all_stats)
	total_guides_with_reads = sum(s[6] for s in all_stats)
	total_guides_no_reads = sum(s[7] for s in all_stats)
	
	percent_matched = round(total_perfect/float(total_perfect + total_nonperfect) * 100, 1)
	percent_no_reads = round(total_guides_no_reads/float(total_guides_with_reads + total_guides_no_reads) * 100, 1)
	
	# Calculate average skew ratio (excluding non-numeric values)
	skew_ratios = [s[5] for s in all_stats if isinstance(s[5], (int, float))]
	avg_skew_ratio = np.mean(skew_ratios) if skew_ratios else 'N/A'
	
	# Read existing file content
	stats_file_path = os.path.join(results_dir, 'statistics.txt')
	existing_content = ""
	if os.path.exists(stats_file_path):
		with open(stats_file_path, 'r') as f:
			existing_content = f.read()
	
	# Write overall statistics at top, then append existing content
	with open(stats_file_path, 'w') as f:
		f.write('=================================================================\n')
		f.write('OVERALL STATISTICS (Aggregate from {} files)\n'.format(file_count))
		f.write('=================================================================\n')
		f.write('Total perfect guide matches: ' + str(total_perfect) + '\n')
		f.write('Total nonperfect guide matches: ' + str(total_nonperfect) + '\n')
		f.write('Total reads processed: ' + str(total_reads) + '\n')
		f.write('Percentage of guides that matched perfectly: ' + str(round(percent_matched, 1)) + '\n')
		f.write('Percentage of undetected guides: ' + str(round(percent_no_reads, 1)) + '\n')
		if isinstance(avg_skew_ratio, (int, float)):
			f.write('Average skew ratio of top 10% to bottom 10%: ' + str(round(avg_skew_ratio, 2)) + '\n')
		else:
			f.write('Average skew ratio of top 10% to bottom 10%: ' + str(avg_skew_ratio) + '\n')
		f.write('=================================================================\n\n')
		f.write(existing_content)


def print_results(fastq_file, results_dir, dict_sorted, nons_dict, stats):
	"""
	Writes analysis results for a single FASTQ file to output CSV and statistics files.
	
	This function appends results to three output files:
	1. guide_counts.csv - All guide sequences and their counts
	2. noMatch_counts.csv - Sequences that didn't match the library
	3. statistics.txt - Detailed statistics for this specific file
	
	Parameters:
	----------
	fastq_file : str
		Name of the FASTQ file being processed (used as identifier in output).
	results_dir : str
		Path to the directory where output files should be written.
	dict_sorted : OrderedDict
		Ordered dictionary of guide sequences (keys) and their counts (values).
	nons_dict : dict
		Dictionary of non-matching sequences (keys) and their counts (values).
	stats : list
		List containing statistics: [perfect_matches, non_perfect_matches, num_reads,
		                              percent_matched, percent_no_reads, skew_ratio,
		                              guides_with_reads, guides_no_reads]
	
	Returns:
	-------
	None
		Writes directly to output files in results_dir.
	"""
	
	# write guide counts to output file
	with open(os.path.join(results_dir, "guide_counts.csv"), 'a') as csvfile:
		mywriter = csv.writer(csvfile, delimiter=',')
		for guide in dict_sorted:
			count = dict_sorted[guide]
			mywriter.writerow([fastq_file,guide,count])

	nomatch_out_file_name = os.path.join(results_dir, "noMatch_counts.csv")

	# write non-matching guides and their counts to a separate file
	with open(nomatch_out_file_name, "a") as fw_nomatch:
		for oligo_nomatch, count_nomatch in nons_dict.items():
			fw_nomatch.write("{}, {}, {}\n".format(fastq_file, oligo_nomatch, count_nomatch))

	# write analysis statistics to statistics.txt
	with open(os.path.join(results_dir, 'statistics.txt'), 'a') as infile:
		infile.write('-----------------------------------------------------------------\n')
		infile.write('Results for file: ' + str(fastq_file) + '\n')
		infile.write('Number of perfect guide matches: ' + str(stats[0]) + '\n')
		infile.write('Number of nonperfect guide matches: ' + str(stats[1]) + '\n')
		infile.write('Number of reads processed: ' + str(stats[2]) + '\n')
		infile.write('Percentage of guides that matched perfectly: ' + str(stats[3]) + '\n')
		infile.write('Percentage of undetected guides: ' + str(stats[4]) + '\n')
		infile.write('Skew ratio of top 10% to bottom 10%: ' + str(stats[5])+ '\n')
		infile.write('-----------------------------------------------------------------\n\n')
		infile.close()
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='Analyze sequencing data for sgRNA library distribution')
	parser.add_argument('-f', '--fastq', type=str, dest='fastq_file',
						help='fastq file name')
	parser.add_argument('-o', '--output', type=str, dest='output_file',
						help='output file name', default='library_count.csv')
	parser.add_argument('-i', '--input', type=str, dest='input_file',
						help='input file name', default='library_sequences.csv')
	parser.add_argument('-no-g', dest='guide_g', help='presence of guanine before spacer', action='store_false')
	parser.add_argument('-p', '--processes', type=int, dest='num_processes',
						help='number of parallel processes (default: all CPUs)', default=cpu_count())
	parser.set_defaults(guide_g=False)
	args = parser.parse_args()

	if not args.fastq_file:
		# Find all .fastq and .fastq.gz files in current directory
		fastq_files = glob.glob("*.fastq")
		fastq_gz_files = glob.glob("*.fastq.gz")

		# Combine both lists
		all_fastq_files = fastq_files + fastq_gz_files

	else:
		all_fastq_files = [args.fastq_file]

	# Create results directory with incremental numbering if it exists
	results_dir = "results"
	counter = 2
	while os.path.exists(results_dir):
		results_dir = f"results_{counter}"
		counter += 1
	os.makedirs(results_dir, exist_ok=True)

	file_count = len(all_fastq_files)
	if file_count == 0:
		print("No FASTQ files found to process. Exiting.")
		sys.exit(0)

	# Create shared counter and lock for progress tracking
	with Manager() as manager:
		counter = manager.Value('i', 0)
		lock = manager.Lock()
		
		# Prepare arguments for parallel processing
		process_args = [(args.input_file, fastq_file, args.guide_g, results_dir, counter, lock, file_count) for fastq_file in all_fastq_files]

		# Process files in parallel
		print(f"Processing {file_count} files using {args.num_processes} processes...")
		with Pool(processes=args.num_processes) as pool:
			results = pool.map(process_single_file, process_args)
		
		successful = sum(1 for _, success, _ in results if success)
		
		# Collect all stats from successful runs
		all_stats = [stats for _, success, stats in results if success and stats is not None]
		
		# Write overall statistics at the top of the file
		if all_stats:
			write_overall_statistics(results_dir, all_stats, len(all_stats))
		
		print(f"\nCompleted! Successfully processed {successful}/{file_count} files.")
 